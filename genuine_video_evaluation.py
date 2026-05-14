#!/usr/bin/env python3

###########################################################################
#
#  Copyright 2025 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

"""Standalone LLM assessment of whether a video appears genuine (not ABCD/Shorts).

This module is intentionally separate from the ABCD and Shorts feature pipelines.
It only uses the video plus a fixed rubric; it does not register with
feature_configs_handler or VideoFeatureCategory.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from configuration import Configuration
from gcp_api_services.gemini_api_service import get_gemini_api_service
from models import LLMParameters, PromptConfig

GENUINE_VIDEO_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "likely_genuine": {
            "type": "boolean",
            "description": (
                "True if the footage appears to be a coherent, authentic "
                "recording of real scenes or people, based only on what is visible."
            ),
        },
        "confidence_score": {
            "type": "number",
            "description": "0.0 (uncertain) to 1.0 (high confidence).",
        },
        "rationale": {
            "type": "string",
            "description": "Short reasoning tied to observations in the video.",
        },
        "evidence": {
            "type": "string",
            "description": "Concrete visual or auditory cues with timestamps when possible.",
        },
        "red_flags": {
            "type": "string",
            "description": (
                "Possible signs of manipulation, heavy CGI, inconsistent physics, "
                "or other issues; empty if none observed."
            ),
        },
        "limitations": {
            "type": "string",
            "description": (
                "What cannot be determined from the video alone (e.g. no forensic proof)."
            ),
        },
    },
    "required": [
        "likely_genuine",
        "confidence_score",
        "rationale",
        "evidence",
        "red_flags",
        "limitations",
    ],
}

_SYSTEM_INSTRUCTIONS = """
You assess whether a video *appears* genuine as a real-world recording, using only
what is visible and audible in the provided file.

- "Genuine" here means: consistent lighting and perspective, plausible motion,
  coherent continuity, and no strong signs the main content is synthetic,
  heavily misleading, or a shallow fake loop misrepresented as candid footage.
- You cannot prove origin or cryptographic authenticity; state limitations clearly.
- If uncertain, set likely_genuine to false and keep confidence_score low.
- Base every claim on specific observations; use timestamps when possible.
- Output must match the requested JSON schema exactly.
"""

_USER_PROMPT = """
Watch the entire video and answer: does this content *appear* to be genuine
real-world footage (as opposed to obvious synthetic generation, inconsistent
compositing, or material clearly staged to deceive about what was captured)?

Return one JSON object with likely_genuine, confidence_score, rationale,
evidence, red_flags, and limitations as defined in the schema.
"""


@dataclass
class GenuineVideoAssessment:
  """Structured result of the genuineness check."""

  likely_genuine: bool
  confidence_score: float
  rationale: str
  evidence: str
  red_flags: str
  limitations: str

  @classmethod
  def from_parsed(cls, parsed: dict | None) -> GenuineVideoAssessment:
    if not parsed or not isinstance(parsed, dict):
      return cls(
          likely_genuine=False,
          confidence_score=0.0,
          rationale="No parseable model response.",
          evidence="",
          red_flags="",
          limitations="Assessment unavailable.",
      )
    return cls(
        likely_genuine=bool(parsed.get("likely_genuine", False)),
        confidence_score=float(parsed.get("confidence_score", 0.0)),
        rationale=str(parsed.get("rationale", "")),
        evidence=str(parsed.get("evidence", "")),
        red_flags=str(parsed.get("red_flags", "")),
        limitations=str(parsed.get("limitations", "")),
    )


def evaluate_video_genuineness(
    config: Configuration, video_uri: str
) -> GenuineVideoAssessment:
  """Runs a single Gemini call with video modality and returns structured output."""
  prompt_config = PromptConfig(
      prompt=_USER_PROMPT,
      system_instructions=_SYSTEM_INSTRUCTIONS,
  )
  llm_params = LLMParameters()
  llm_params.model_name = config.llm_params.model_name
  llm_params.location = config.llm_params.location
  llm_params.generation_config = dict(config.llm_params.generation_config)
  llm_params.set_modality({"type": "video", "video_uri": video_uri})
  llm_params.generation_config["response_schema"] = GENUINE_VIDEO_RESPONSE_SCHEMA

  parsed = get_gemini_api_service(config).execute_gemini_with_genai(
      prompt_config, llm_params
  )
  return GenuineVideoAssessment.from_parsed(parsed)


def print_genuine_video_assessment(brand_name: str, video_uri: str, result: GenuineVideoAssessment) -> None:
  """Logs a human-readable summary."""
  label = brand_name or "(no brand)"
  logging.info(
      "\n--- Genuine video check (%s) ---\n"
      "Video: %s\n"
      "Likely genuine: %s (confidence %.2f)\n"
      "Rationale: %s\n"
      "Evidence: %s\n"
      "Red flags: %s\n"
      "Limitations: %s\n"
      "---\n",
      label,
      video_uri,
      result.likely_genuine,
      result.confidence_score,
      result.rationale,
      result.evidence,
      result.red_flags or "(none noted)",
      result.limitations,
  )
