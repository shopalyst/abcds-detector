"""Assessment export, scoring, and BQ helpers (fork)."""

import datetime
import json
import os

import models
from configuration import Configuration
from gcp_api_services import gcs_api_service
from helpers import generic_helpers

# Features where detected=True means a problem (inverse pass/fail for scoring).
RISK_FEATURE_IDS = frozenset({
    "misinformation_risk",
    "clickbait_detection",
    "negativity_hate_speech",
    "brand_safety",
})


def feature_passed(eval_feature: models.FeatureEvaluation) -> bool:
  """True when the creative passes this feature (risk-aware)."""
  is_risk = eval_feature.feature.id in RISK_FEATURE_IDS
  if is_risk:
    return not eval_feature.detected
  return bool(eval_feature.detected)


def calculate_score(evaluated_features: list[models.FeatureEvaluation]) -> float:
  """Content-intelligence score (% passed, risk-aware)."""
  total_features = len(evaluated_features)
  passed_features_count = sum(
      1 for feature in evaluated_features if feature_passed(feature)
  )
  return (
      ((passed_features_count * 100) / total_features)
      if total_features > 0
      else 0
  )


def print_abcd_assessment(
    brand_name: str,
    video_uri: str,
    evaluated_features: list[models.FeatureEvaluation],
) -> None:
  """Print assessment with risk-aware scoring (content intelligence)."""
  print(f"***** ABCD Assessment for brand {brand_name} ***** \n")
  print(f"Asset name: {video_uri} \n")
  _print_score_details(evaluated_features)


def _print_score_details(
    evaluated_features: list[models.FeatureEvaluation],
) -> None:
  total_features = len(evaluated_features)
  passed_count = sum(1 for f in evaluated_features if feature_passed(f))
  score = calculate_score(evaluated_features)
  print(
      f"Video score: {round(score, 2)}%, adherence ({passed_count}/{total_features})\n"
  )
  if score >= 80:
    print("Asset result: ✅ Excellent \n")
  elif score >= 65:
    print("Asset result: ⚠ Might Improve \n")
  else:
    print("Asset result: ❌ Needs Review \n")

  print("Evaluated Features: \n")
  for eval_feature in evaluated_features:
    if feature_passed(eval_feature):
      print(f" * ✅ {eval_feature.feature.name}")
    else:
      print(f" * ❌ {eval_feature.feature.name}")
  print("\n")


def _feature_evaluation_to_dict(
    eval_feature: models.FeatureEvaluation,
    pipeline: str,
) -> dict:
  f = eval_feature.feature
  passed = feature_passed(eval_feature)
  is_risk = f.id in RISK_FEATURE_IDS
  return {
      "pipeline": pipeline,
      "feature_id": f.id,
      "feature_name": f.name,
      "feature_category": getattr(f.category, "value", str(f.category)),
      "feature_sub_category": getattr(f.sub_category, "value", str(f.sub_category)),
      "feature_video_segment": getattr(f.video_segment, "value", str(f.video_segment)),
      "feature_group": getattr(f, "feature_group", "GENERAL"),
      "evaluation_method": getattr(f.evaluation_method, "value", str(f.evaluation_method)),
      "feature_evaluation_criteria": f.evaluation_criteria or "",
      "detected": eval_feature.detected,
      "passed": passed,
      "is_risk_feature": is_risk,
      "confidence_score": eval_feature.confidence_score,
      "value": getattr(eval_feature, "value", "") or "",
      "rationale": eval_feature.rationale or "",
      "evidence": eval_feature.evidence or "",
      "strengths": eval_feature.strengths or "",
      "weaknesses": eval_feature.weaknesses or "",
  }


def write_assessment_to_file(
    config: Configuration,
    video_assessment: models.VideoAssessment,
) -> None:
  """Write full assessment (all pipelines) to a local JSON file."""
  if not config.assessment_file or not config.assessment_file.strip():
    return
  path = config.assessment_file.strip()

  long_form = [
      _feature_evaluation_to_dict(ef, "LONG_FORM_ABCD")
      for ef in video_assessment.long_form_abcd_evaluated_features
  ]
  shorts = [
      _feature_evaluation_to_dict(ef, "SHORTS")
      for ef in video_assessment.shorts_evaluated_features
  ]
  content_quality = [
      _feature_evaluation_to_dict(ef, "CONTENT_INTELLIGENCE")
      for ef in video_assessment.content_quality_evaluated_features
  ]
  all_rows = long_form + shorts + content_quality

  total = len(all_rows)
  passed_count = sum(1 for r in all_rows if r["passed"])
  score = round((passed_count / total * 100) if total else 0, 2)
  result_label = (
      "Excellent" if score >= 80 else "Might Improve" if score >= 65 else "Needs Review"
  )

  payload = {
      "execution_timestamp": datetime.datetime.now().isoformat(),
      "brand_name": video_assessment.brand_name,
      "video_uri": video_assessment.video_uri,
      "brand_metadata": {
          "brand_name": config.brand_name,
          "brand_variations": config.brand_variations,
          "branded_products": config.branded_products,
          "branded_products_categories": config.branded_products_categories,
          "branded_call_to_actions": config.branded_call_to_actions,
      },
      "summary": {
          "score_percent": score,
          "adherence": f"{passed_count}/{total}",
          "result": result_label,
          "feature_count": total,
      },
      "evaluations": {
          "long_form_abcd": long_form,
          "shorts": shorts,
          "content_intelligence": content_quality,
      },
      "features": all_rows,
  }
  parent = os.path.dirname(path)
  if parent:
    os.makedirs(parent, exist_ok=True)
  with open(path, "w", encoding="utf-8") as out:
    json.dump(payload, out, indent=2, ensure_ascii=False)
  print(f"Results written to {path} \n")


def build_features_for_bq(
    config: Configuration, video_assessment: models.VideoAssessment
) -> list[dict]:
  """Upstream ABCD/Shorts rows plus content intelligence rows."""
  rows = generic_helpers.build_features_for_bq(config, video_assessment)
  rows.extend(_content_rows_for_bq(config, video_assessment))
  return rows


def _content_rows_for_bq(
    config: Configuration,
    video_assessment: models.VideoAssessment,
) -> list[dict]:
  rows = []
  for eval_feature in video_assessment.content_quality_evaluated_features:
    if config.creative_provider_type == models.CreativeProviderType.GCS:
      video_name = gcs_api_service.gcs_api_service.get_video_name_from_uri(
          video_assessment.video_uri
      )
    else:
      video_name = video_assessment.video_uri

    category = (
        eval_feature.feature.category.value
        if hasattr(eval_feature.feature.category, "value")
        else eval_feature.feature.category
    )
    sub_category = (
        eval_feature.feature.sub_category.value
        if hasattr(eval_feature.feature.sub_category, "value")
        else eval_feature.feature.sub_category
    )

    rows.append({
        "execution_timestamp": datetime.datetime.now(),
        "brand_name": video_assessment.brand_name,
        "video_id": video_assessment.video_uri,
        "video_name": video_name,
        "video_uri": video_assessment.video_uri,
        "feature_id": eval_feature.feature.id,
        "feature_name": eval_feature.feature.name,
        "feature_category": category,
        "feature_sub_category": sub_category,
        "feature_video_segment": eval_feature.feature.video_segment.value,
        "feature_evaluation_criteria": eval_feature.feature.evaluation_criteria,
        "detected": eval_feature.detected,
        "confidence_score": str(eval_feature.confidence_score),
        "evidence": eval_feature.evidence,
        "rationale": eval_feature.rationale,
        "strengths": eval_feature.strengths,
        "weaknesses": eval_feature.weaknesses,
        "brand_metadata": str({
            "brand_name": config.brand_name,
            "brand_variations": ",".join(config.brand_variations),
            "branded_products": ",".join(config.branded_products),
            "branded_product_categories": ",".join(
                config.branded_products_categories
            ),
        }),
        "config": str(config.__dict__),
    })
  return rows


def store_in_bq(
    config: Configuration,
    video_assessment: models.VideoAssessment,
) -> None:
  """Store assessment in BQ including content intelligence rows."""
  print(
      f"Storing ABCD assessment for video {video_assessment.video_uri} in"
      " BigQuery... \n"
  )
  import pandas
  from gcp_api_services import bigquery_api_service

  bq_api_service = bigquery_api_service.BigQueryAPIService(config.project_id)
  assessment_bq = build_features_for_bq(config, video_assessment)

  if len(assessment_bq) == 0:
    print(
        "There are no rows to insert into BQ for video"
        f" {video_assessment.video_uri}. \n"
    )
    return

  columns = generic_helpers.get_table_columns()
  dataframe = pandas.DataFrame(assessment_bq, columns=columns)
  bq_api_service.create_dataset(config.bq_dataset_name, config.project_zone)
  schema = generic_helpers.get_table_schema()
  table_created = bq_api_service.create_table(
      config.bq_dataset_name, config.bq_table_name, schema
  )
  if table_created:
    print(f"Inserting {len(assessment_bq)} rows into BQ... \n")
    bq_api_service.load_table_from_dataframe(
        config.bq_dataset_name,
        config.bq_table_name,
        dataframe,
        schema,
        "WRITE_APPEND",
    )
  else:
    print(
        "Error: ABCD assessments not loaded to table"
        f" {config.bq_dataset_name}.{config.bq_table_name} because the table"
        " could not be created. \n"
    )
