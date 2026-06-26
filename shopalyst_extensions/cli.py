"""CLI presets and argument registration (fork)."""

import argparse

from configuration import Configuration
from shopalyst_extensions.feature_registry import (
    get_content_intelligence_feature_configs,
)


def get_content_quality_feature_ids() -> list[str]:
  """Enabled content-intelligence feature IDs (matches -bcp preset)."""
  return [
      feature.id
      for feature in get_content_intelligence_feature_configs()
      if feature.include_in_evaluation
  ]


def resolve_run_flags(args: argparse.Namespace) -> dict:
  """Map CLI args to run_long_form_abcd, run_shorts, run_content_quality, etc."""
  if getattr(args, "brand_collab_preset", False):
    return {
        "extract_brand_metadata": True,
        "use_annotations": args.use_annotations,
        "use_llms": True,
        "run_long_form_abcd": False,
        "run_shorts": False,
        "run_content_quality": True,
        "features_to_evaluate": get_content_quality_feature_ids(),
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
          "Run brand-collab preset: enabled content-intelligence features only "
          "(no long-form ABCD or Shorts), LLM-only, and auto-extract brand "
          "metadata."
      ),
      action="store_true",
      default=False,
  )
