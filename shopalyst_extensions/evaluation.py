"""Evaluation helpers (fork)."""

import logging

import models
from configuration import Configuration


def filter_by_requested_ids(
    config: Configuration,
    feature_groups: dict[str, list[models.VideoFeature]],
    features_category: models.VideoFeatureCategory,
) -> dict[str, list[models.VideoFeature]]:
  """When features_to_evaluate is set, keep only matching feature IDs."""
  requested_ids = {
      feature_id.strip()
      for feature_id in (config.features_to_evaluate or [])
      if feature_id and str(feature_id).strip()
  }
  if not requested_ids:
    return feature_groups

  filtered_feature_groups: dict[str, list[models.VideoFeature]] = {}
  for group_key, group_feature_configs in feature_groups.items():
    selected = [
        f_config
        for f_config in group_feature_configs
        if f_config.id in requested_ids
    ]
    if selected:
      filtered_feature_groups[group_key] = selected

  if not filtered_feature_groups:
    logging.warning(
        "No features matched features_to_evaluate for category %s."
        " Check IDs or disable filtering.",
        features_category.value,
    )
  return filtered_feature_groups


def sort_feature_evaluations(
    feature_evaluations: list[models.FeatureEvaluation],
    features_category: models.VideoFeatureCategory,
) -> list[models.FeatureEvaluation]:
  """Sort long-form ABCD and content intelligence results for display."""
  if features_category in (
      models.VideoFeatureCategory.LONG_FORM_ABCD,
      models.VideoFeatureCategory.CONTENT_INTELLIGENCE,
  ):
    return sorted(
        feature_evaluations,
        key=lambda feature_eval: (
            feature_eval.feature.category.value,
            feature_eval.feature.id,
        ),
        reverse=False,
    )
  return feature_evaluations
