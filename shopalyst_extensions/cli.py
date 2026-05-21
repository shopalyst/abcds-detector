"""CLI presets and argument registration (fork)."""

import argparse

from configuration import Configuration

BRAND_COLLAB_ABCD_FEATURE_IDS = [
    "a_dynamic_start",
    "a_quick_pacing",
    "a_quick_pacing_1st_5_secs",
    "a_supers",
    "a_supers_with_audio",
    "b_brand_visuals",
    "b_brand_visuals_1st_5_secs",
    "b_brand_mention_speech",
    "b_brand_mention_speech_1st_5_secs",
    "b_product_visuals",
    "b_product_visuals_1st_5_secs",
    "b_product_mention_text",
    "b_product_mention_text_1st_5_secs",
    "b_product_mention_speech",
    "b_product_mention_speech_1st_5_secs",
    "c_presence_of_people",
    "c_presence_of_people_1st_5_secs",
    "c_visible_face",
    "c_visible_face_close_up",
    "d_call_to_action_speech",
    "d_call_to_action_text",
    "d_audio_speech_early_1st_5_secs",
]

CONTENT_QUALITY_FEATURE_IDS = [
    "content_clarity_focus",
    "narrative_structure",
    "informational_depth",
    "production_quality",
    "actionable_value",
    "audience_relevance",
    "engagement_potential",
    "low_effort_spam",
    "authenticity_trustworthiness",
    "misinformation_risk",
    "clickbait_detection",
    "negativity_hate_speech",
    "brand_safety",
    "audience_appropriateness",
    "cultural_sensitivity",
    "genuine_vs_ad",
    "shorts_hashtag_strategy",
]


def resolve_run_flags(args: argparse.Namespace) -> dict:
  """Map CLI args to run_long_form_abcd, run_shorts, run_content_quality, etc."""
  if getattr(args, "brand_collab_preset", False):
    return {
        "extract_brand_metadata": True,
        "use_annotations": args.use_annotations,
        "use_llms": True,
        "run_long_form_abcd": True,
        "run_shorts": True,
        "run_content_quality": True,
        "features_to_evaluate": (
            BRAND_COLLAB_ABCD_FEATURE_IDS + CONTENT_QUALITY_FEATURE_IDS
        ),
        "creative_provider_type": args.creative_provider_type or "GCS",
    }

  return {
      "extract_brand_metadata": args.extract_brand_metadata,
      "use_annotations": args.use_annotations,
      "use_llms": args.use_llms,
      "run_long_form_abcd": args.run_long_form_abcd,
      "run_shorts": args.run_shorts,
      "run_content_quality": args.run_content_quality,
      "features_to_evaluate": (
          [f.strip() for f in args.features_to_evaluate.split(",") if f.strip()]
          if args.features_to_evaluate
          else []
      ),
      "creative_provider_type": args.creative_provider_type,
  }


def invalid_brand_metadata(config: Configuration) -> bool:
  """Brand metadata required only for ABCD/Shorts when extract is disabled."""
  requires_brand = config.run_long_form_abcd or config.run_shorts
  return requires_brand and not config.extract_brand_metadata and (
      not config.brand_name
      or len(config.brand_variations) == 0
      or len(config.branded_products) == 0
      or len(config.branded_products_categories) == 0
  )


def register_cli_arguments(parser: argparse.ArgumentParser) -> None:
  """Register Shopalyst-only CLI flags on the shared parser."""
  parser.add_argument(
      "-run_content_quality",
      "-rcq",
      help="Run content quality and safety evaluation (clarity, value, trust, safety)",
      action="store_true",
      default=False,
  )
  parser.add_argument(
      "-brand_collab_preset",
      "-bcp",
      help=(
          "Run brand-collab preset: selected ABCD features + all content-quality "
          "features, LLM-only (no annotations), and auto-extract brand metadata."
      ),
      action="store_true",
      default=False,
  )
