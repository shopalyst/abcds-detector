"""Feature batching for LLM calls (fork)."""

from models import VideoFeature

# Fine taxonomy for export (feature_macro_group). Not used for LLM batch keys.
CI_MACRO_GROUP_MAP: dict[str, str] = {
    "QUALITY_CLARITY": "CORE_QUALITY",
    "VALUE": "CORE_QUALITY",
    "TECHNICAL_QUALITY": "TECHNICAL",
    "SAFETY": "SAFETY_TRUST",
    "TRUST": "SAFETY_TRUST",
    "STYLE_CLASSIFICATION": "STYLE",
    "VISUAL_STYLE": "STYLE",
    "GENRE_LEVELS": "TAXONOMY",
    "CONTENT_TAXONOMY": "TAXONOMY",
    "LANGUAGE": "TAXONOMY",
    "CULTURE": "TAXONOMY",
    "BRAND_INTEGRATION": "BRAND_DISCOVERY",
    "DISCOVERY_SEO": "BRAND_DISCOVERY",
}

# How many Gemini calls for full CI. Set to 2 or 3.
CI_LLM_BATCH_MODE = 3

# Macro taxonomy -> LLM batch (3 calls: ~14 + 8 + 17 features).
CI_LLM_BATCH_FROM_MACRO_3: dict[str, str] = {
    "CORE_QUALITY": "QUALITY_TECH",
    "TECHNICAL": "QUALITY_TECH",
    "SAFETY_TRUST": "SAFETY_TRUST",
    "STYLE": "STYLE_CONTEXT",
    "TAXONOMY": "STYLE_CONTEXT",
    "BRAND_DISCOVERY": "STYLE_CONTEXT",
}

# Macro taxonomy -> LLM batch (2 calls: ~22 + 17 features).
CI_LLM_BATCH_FROM_MACRO_2: dict[str, str] = {
    "CORE_QUALITY": "QUALITY_AND_SAFETY",
    "TECHNICAL": "QUALITY_AND_SAFETY",
    "SAFETY_TRUST": "QUALITY_AND_SAFETY",
    "STYLE": "STYLE_AND_CONTEXT",
    "TAXONOMY": "STYLE_AND_CONTEXT",
    "BRAND_DISCOVERY": "STYLE_AND_CONTEXT",
}


def resolve_ci_macro_group(feature: VideoFeature) -> str:
  """Fine taxonomy label for export (feature_macro_group)."""
  legacy_group = getattr(feature, "feature_group", None) or "GENERAL"
  return CI_MACRO_GROUP_MAP.get(legacy_group, legacy_group)


def resolve_ci_llm_batch(feature: VideoFeature) -> str:
  """LLM batch key (2 or 3 calls for full CI, per CI_LLM_BATCH_MODE)."""
  macro = resolve_ci_macro_group(feature)
  if CI_LLM_BATCH_MODE == 2:
    return CI_LLM_BATCH_FROM_MACRO_2.get(macro, macro)
  return CI_LLM_BATCH_FROM_MACRO_3.get(macro, macro)


def group_by_feature_group(feature_configs: list[VideoFeature]) -> dict[str, list[VideoFeature]]:
  """Group CI features into LLM batches (CI_LLM_BATCH_MODE calls when all features run)."""
  grouped_features: dict[str, list[VideoFeature]] = {}
  for feature in feature_configs:
    group_key = resolve_ci_llm_batch(feature)
    grouped_features.setdefault(group_key, []).append(feature)
  return grouped_features
