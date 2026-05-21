"""Feature batching for LLM calls (fork)."""

from models import VideoFeature


def group_by_feature_group(feature_configs: list[VideoFeature]) -> dict[str, list[VideoFeature]]:
  """Group content intelligence features by feature_group for smaller LLM batches."""
  grouped_features: dict[str, list[VideoFeature]] = {}
  for feature in feature_configs:
    group_key = getattr(feature, "feature_group", "GENERAL")
    grouped_features.setdefault(group_key, []).append(feature)
  return grouped_features
