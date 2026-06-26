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
    "COMMUNICATION": "STYLE",
    "FASHION_AESTHETIC": "STYLE",
    "GROOMING": "STYLE",
    "SOCIOECONOMIC": "STYLE",
    "SKIN_CARE_CONSCIOUSNESS": "STYLE",
    "GENRE_LEVELS": "TAXONOMY",
    "CONTENT_TAXONOMY": "TAXONOMY",
    "LANGUAGE": "TAXONOMY",
    "CULTURE": "TAXONOMY",
    "BRAND_INTEGRATION": "BRAND_DISCOVERY",
    "DISCOVERY_SEO": "BRAND_DISCOVERY",
    "CTA": "BRAND_DISCOVERY",
}

# Max parallel Gemini calls for full CI (balanced grouping by feature_group).
CI_LLM_BATCH_MODE = 3

# Balanced LLM batches by feature_group (~12 enabled features per call).
CI_FEATURE_GROUP_LLM_BATCH: dict[str, str] = {
    "TECHNICAL_QUALITY": "CI_TECHNICAL_TRUST_LANGUAGE",
    "TRUST": "CI_TECHNICAL_TRUST_LANGUAGE",
    "LANGUAGE": "CI_TECHNICAL_TRUST_LANGUAGE",
    "VISUAL_STYLE": "CI_VISUAL_STYLE_GENRE",
    "STYLE_CLASSIFICATION": "CI_VISUAL_STYLE_GENRE",
    "GENRE_LEVELS": "CI_VISUAL_STYLE_GENRE",
    "CULTURE": "CI_VISUAL_STYLE_GENRE",
    "GROOMING": "CI_VISUAL_STYLE_GENRE",
    "FASHION_AESTHETIC": "CI_BRAND_LIFESTYLE_DISCOVERY",
    "SOCIOECONOMIC": "CI_BRAND_LIFESTYLE_DISCOVERY",
    "SKIN_CARE_CONSCIOUSNESS": "CI_BRAND_LIFESTYLE_DISCOVERY",
    "CONTENT_TAXONOMY": "CI_BRAND_LIFESTYLE_DISCOVERY",
    "DISCOVERY_SEO": "CI_BRAND_LIFESTYLE_DISCOVERY",
    "BRAND_INTEGRATION": "CI_BRAND_LIFESTYLE_DISCOVERY",
    "COMMUNICATION": "CI_BRAND_LIFESTYLE_DISCOVERY",
    "CTA": "CI_BRAND_LIFESTYLE_DISCOVERY",
    # Disabled today; mapped for even load if re-enabled.
    "QUALITY_CLARITY": "CI_TECHNICAL_TRUST_LANGUAGE",
    "VALUE": "CI_TECHNICAL_TRUST_LANGUAGE",
    "SAFETY": "CI_TECHNICAL_TRUST_LANGUAGE",
}

# Legacy macro collapse (CI_LLM_BATCH_MODE 1 or 2).
CI_LLM_BATCH_FROM_MACRO_3: dict[str, str] = {
    "CORE_QUALITY": "QUALITY_TECH",
    "TECHNICAL": "QUALITY_TECH",
    "SAFETY_TRUST": "SAFETY_TRUST",
    "STYLE": "STYLE_CONTEXT",
    "TAXONOMY": "STYLE_CONTEXT",
    "BRAND_DISCOVERY": "STYLE_CONTEXT",
}

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
  """LLM batch key for grouping CI features into Gemini calls."""
  legacy_group = getattr(feature, "feature_group", None) or "GENERAL"
  if CI_LLM_BATCH_MODE == 3:
    return CI_FEATURE_GROUP_LLM_BATCH.get(legacy_group, legacy_group)
  macro = resolve_ci_macro_group(feature)
  if CI_LLM_BATCH_MODE == 2:
    return CI_LLM_BATCH_FROM_MACRO_2.get(macro, macro)
  if CI_LLM_BATCH_MODE == 1:
    return CI_LLM_BATCH_FROM_MACRO_3.get(macro, macro)
  return CI_FEATURE_GROUP_LLM_BATCH.get(legacy_group, legacy_group)


def group_by_feature_group(feature_configs: list[VideoFeature]) -> dict[str, list[VideoFeature]]:
  """Group CI features into LLM batches."""
  grouped_features: dict[str, list[VideoFeature]] = {}
  for feature in feature_configs:
    group_key = resolve_ci_llm_batch(feature)
    grouped_features.setdefault(group_key, []).append(feature)
  return grouped_features
