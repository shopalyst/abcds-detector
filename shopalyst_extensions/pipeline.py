"""Content intelligence pipeline hooks (fork)."""

import logging

import models
from configuration import Configuration
from evaluation_services import video_evaluation_service
from shopalyst_extensions import assessment


def evaluate_content_quality(
    config: Configuration, video_uri: str
) -> list[models.FeatureEvaluation]:
  """Run content intelligence when enabled."""
  if not config.run_content_quality:
    return []

  if not config.use_llms:
    logging.warning(
        "run_content_quality is enabled but use_llms is false; "
        "content intelligence requires -ull."
    )
  logging.info("Running content intelligence evaluation...")
  results = video_evaluation_service.video_evaluation_service.evaluate_features(
      config=config,
      video_uri=video_uri,
      features_category=models.VideoFeatureCategory.CONTENT_INTELLIGENCE,
  )
  logging.info("Content intelligence: %s feature(s) evaluated.", len(results))
  return results


def print_content_results(
    brand_name: str,
    video_uri: str,
    content_features: list[models.FeatureEvaluation],
) -> None:
  if len(content_features) > 0:
    assessment.print_abcd_assessment(brand_name, video_uri, content_features)
  else:
    logging.info(
        "There are not Content Quality evaluated features results to display."
    )


def persist_results(
    config: Configuration, video_assessment: models.VideoAssessment
) -> None:
  """Write JSON and/or BQ when configured (includes content rows)."""
  if config.assessment_file:
    assessment.write_assessment_to_file(config, video_assessment)
  if config.bq_table_name:
    assessment.store_in_bq(config, video_assessment)
