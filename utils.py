#!/usr/bin/env python3

###########################################################################
#
#    Copyright 2024 Google LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#            https://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
###########################################################################

"""Utils Module for generic functions"""

import argparse
import textwrap
from configuration import Configuration


BRAND_COLLAB_ABCD_FEATURE_IDS = [
    # Attract
    "a_dynamic_start",
    "a_quick_pacing",
    "a_quick_pacing_1st_5_secs",
    "a_supers",
    "a_supers_with_audio",
    # Brand
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
    # Connect
    "c_presence_of_people",
    "c_presence_of_people_1st_5_secs",
    "c_visible_face",
    "c_visible_face_close_up",
    # Direct
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


def build_abcd_params_config(args: any) -> Configuration:
  """Builds ABCD configuration with all the required parameters.

  Args:
      args: The parser arguments.
  Returns:
      config: The parameter configuration for ABCD.

  """
  config = Configuration()

  # Custom preset: brand-collab analysis = selected ABCD + all content-intelligence,
  # defaults to LLM-first; annotations remain optional and can be enabled via -uan.
  if getattr(args, "brand_collab_preset", False):
    extract_brand_metadata = True
    # Keep annotations opt-in: default False, user can override with -uan.
    use_annotations = args.use_annotations
    use_llms = True  # implied by preset
    run_long_form_abcd = True
    run_shorts = True
    run_content_quality = True
    features_to_evaluate = BRAND_COLLAB_ABCD_FEATURE_IDS + CONTENT_QUALITY_FEATURE_IDS
    creative_provider_type = args.creative_provider_type or "GCS"
  else:
    extract_brand_metadata = args.extract_brand_metadata
    use_annotations = args.use_annotations
    use_llms = args.use_llms
    run_long_form_abcd = args.run_long_form_abcd
    run_shorts = args.run_shorts
    run_content_quality = args.run_content_quality
    creative_provider_type = args.creative_provider_type
    features_to_evaluate = (
        [f.strip() for f in args.features_to_evaluate.split(",") if f.strip()]
        if args.features_to_evaluate
        else []
    )

  config.set_parameters(
      project_id=args.project_id,
      project_zone=args.project_zone,
      bucket_name=args.bucket_name,
      knowledge_graph_api_key=args.knowledge_graph_api_key,
      bigquery_dataset=args.bigquery_dataset,
      bigquery_table=args.bigquery_table,
      assessment_file=args.assessment_file,
      extract_brand_metadata=extract_brand_metadata,
      use_annotations=use_annotations,
      use_llms=use_llms,
      run_long_form_abcd=run_long_form_abcd,
      run_shorts=run_shorts,
      run_content_quality=run_content_quality,
      features_to_evaluate=features_to_evaluate,
      creative_provider_type=creative_provider_type,
      verbose=args.verbose,
  )
  config.set_videos(args.video_uris)
  config.set_brand_details(
      brand_name=args.brand_name,
      brand_variations=args.brand_variations,
      products=args.branded_products,
      products_categories=args.branded_products_categories,
      call_to_actions=args.branded_call_to_actions,
  )

  # LLM params are optional; keep defaults when not provided.
  if (
      args.llm_name is not None
      or args.llm_location is not None
      or args.max_output_tokens is not None
      or args.temperature is not None
      or args.top_p is not None
  ):
    config.set_llm_params(
        llm_name=args.llm_name or config.llm_params.model_name,
        location=args.llm_location or config.llm_params.location,
        max_output_tokens=args.max_output_tokens
        or config.llm_params.generation_config.get("max_output_tokens"),
        temperature=args.temperature
        or config.llm_params.generation_config.get("temperature"),
        top_p=args.top_p or config.llm_params.generation_config.get("top_p"),
    )

  return config


def invalid_brand_metadata(config: Configuration):
  # Brand metadata is only required when running ABCD or Shorts features.
  # Content-quality-only runs do not need brand information.
  requires_brand = config.run_long_form_abcd or config.run_shorts
  return requires_brand and not config.extract_brand_metadata and (
      not config.brand_name
      or len(config.brand_variations) == 0
      or len(config.branded_products) == 0
      or len(config.branded_products_categories) == 0
  )


def parse_args(arg_list: list[str] | None = None) -> None:
  """Parses command line arguments"""

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
        Command line to execute ABCD detector with parameters.

        This loads the minimal parameters needed to configure the tool.
        See the configuration.py file for additional parameters.

        Example: python main.py -pi my_project -pz "us-central1" \
        -bn "my_bucket" -vu "gs://my_bucket/Google/videos/" -ua -ul -v
    """),
  )

  parser.add_argument("-project_id", "-pi", help="Google Cloud Project ID.")
  parser.add_argument("-project_zone", "-pz", help="Google Cloud Project Zone.")
  parser.add_argument(
      "-bucket_name", "-bn", help="Google Cloud Project Bucket Name (not url)."
  )
  parser.add_argument(
      "-video_uris",
      "-vu",
      help="Comma delimited string of video or folder URIs.",
  )
  parser.add_argument(
      "-brand_name", "-brn", help="The name of the brand.", default=None
  )
  parser.add_argument(
      "-brand_variations",
      "-brv",
      help="The list of brand name variations.",
      default=None,
  )
  parser.add_argument(
      "-branded_products",
      "-brprs",
      help="The list of branded products.",
      default=None,
  )
  parser.add_argument(
      "-branded_products_categories",
      "-brprscts",
      help="The list of branded product categories",
      default=None,
  )
  parser.add_argument(
      "-branded_call_to_actions",
      "-brcallacts",
      help="The list of branded call to actions",
      default=None,
  )
  parser.add_argument(
      "-knowledge_graph_api_key",
      "-kgak",
      help="Knowledge Graph Key for API.",
      default=None,
  )
  parser.add_argument(
      "-bigquery_dataset",
      "-bd",
      help="Name of BigQuery dataset to write to",
      default=None,
  )
  parser.add_argument(
      "-bigquery_table",
      "-bt",
      help="Name of BigQuery table to write to",
      default=None,
  )
  parser.add_argument(
      "-assessment_file",
      "-af",
      help="Local file path to write results to",
      default=None,
  )
  parser.add_argument(
      "-llm_name",
      "-llmn",
      help="LLM name",
      default=None,
  )
  parser.add_argument(
      "-llm_location",
      "-llml",
      help="LLM location",
      default=None,
  )
  parser.add_argument(
      "-max_output_tokens",
      "-mxotk",
      help="Max output tokens",
      default=None,
  )
  parser.add_argument(
      "-temperature",
      "-temp",
      help="Temperature parameter",
      default=None,
  )
  parser.add_argument(
      "-top_p",
      "-tpp",
      help="Top P parameter",
      default=None,
  )
  parser.add_argument(
      "-features_to_evaluate",
      "-fteval",
      help="List of features to evaluate",
      default=None,
  )
  parser.add_argument(
      "-creative_provider_type",
      "-crpt",
      help="Creative provider type where the creatives are coming from",
      default=None,
  )
  parser.add_argument(
      "-extract_brand_metadata",
      "-extvn",
      help="Extract video metadata to get brand information",
      action="store_true",
      default=False,
  )
  parser.add_argument(
      "-use_annotations",
      "-uan",
      help="Use Annotations for the evaluation",
      action="store_true",
      default=False,
  )
  parser.add_argument(
      "-use_llms",
      "-ull",
      help="Use LLMs for the evaluation",
      action="store_true",
      default=False,
  )
  parser.add_argument(
      "-run_long_form_abcd",
      "-rfa",
      help="Run evaluation for Full ABCD features",
      action="store_true",
      default=False,
  )
  parser.add_argument(
      "-run_shorts",
      "-rs",
      help="Run evaluation for Shorts features",
      action="store_true",
      default=False,
  )
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
  parser.add_argument(
      "-verbose",
      "-v",
      help="Print all the steps as they happen.",
      action="store_true",
      default=False,
  )

  args = parser.parse_args(arg_list)

  return args
