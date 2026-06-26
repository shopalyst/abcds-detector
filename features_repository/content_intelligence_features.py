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

"""Content intelligence and safety feature configurations.

These features are designed for analysing short-form social content
(Instagram, TikTok, YouTube Shorts) and static images posted by creators.
They evaluate content quality, meaningfulness, trustworthiness, and safety.
All features are LLM-only and work equally on GCS videos, YouTube URLs,
and image URIs.
"""

from models import (
    VideoFeature,
    VideoFeatureCategory,
    VideoSegment,
    EvaluationMethod,
    VideoFeatureSubCategory,
)

# Suggested top-level genre labels (guidance only — not a closed enum).
GENRE_LEVEL_EXAMPLE_LABELS = (
    "travel, unknown, entertainment, beauty, fashion, food, lifestyle,"
    " photography, health and fitness, business, pet, sports, art and craft,"
    " automobile, education, other, parenting, current affairs, games and apps"
)
GENRE_LEVEL_GUIDANCE = (
    "Set primary_genre, secondary_genre, and each entry in other_genres to"
    " short genre labels (lowercase preferred). Common examples include:"
    f" {GENRE_LEVEL_EXAMPLE_LABELS}."
    " These are suggestions only — use the best-fit label or a close synonym;"
    " do not treat this list as a closed enum."
)

BRAND_VISIBILITY_IN_CONTENT_LEVELS = (
    "None", "Incidental", "Prominent", "Featured"
)
BRAND_VISIBILITY_IN_CONTENT_INSTRUCTION = (
    "Brand visibility level must be exactly one of: None, Incidental, Prominent,"
    " Featured. None = no brand visible; Incidental = visible but not emphasized;"
    " Prominent = clearly visible or central; Featured = intentionally showcased."
)

COMMUNICATION_STYLE_LEVELS = (
    "educational",
    "direct",
    "humorous",
    "storytelling",
    "conversational",
    "testimonial",
    "promotional",
    "inspirational",
    "demonstrative",
)
COMMUNICATION_STYLE_INSTRUCTION = (
    "Communication style must be exactly one of:"
    f" {', '.join(COMMUNICATION_STYLE_LEVELS)}."
    " educational = teaches or explains; direct = blunt, clear, to-the-point;"
    " humorous = comedy or playful tone drives delivery; storytelling = narrative"
    " arc carries the message; conversational = casual peer-to-peer chat;"
    " testimonial = personal experience or review; promotional = sell or CTA-forward;"
    " inspirational = motivational or aspirational; demonstrative = show-how demo"
    " or hands-on use."
)

CTA_TYPE_LEVELS = (
    "comment_prompt",
    "purchase_prompt",
    "share_prompt",
    "poll_quiz",
    "link_in_bio",
    "follow_subscribe",
    "save_prompt",
    "learn_more",
    "dm_prompt",
)
CTA_TYPE_INSTRUCTION = (
    "Call-to-action type must be exactly one of:"
    f" {', '.join(CTA_TYPE_LEVELS)}."
    " comment_prompt = ask viewers to comment (e.g. comment a keyword);"
    " purchase_prompt = shop/buy/order or use a discount code;"
    " share_prompt = share, tag, or repost;"
    " poll_quiz = poll, quiz, or choose-between engagement;"
    " link_in_bio = link in bio or tap the link below;"
    " follow_subscribe = follow or subscribe;"
    " save_prompt = save or bookmark the post;"
    " learn_more = soft explore/check-it-out ask without direct purchase;"
    " dm_prompt = DM or message for details or link."
)

FASHION_AESTHETIC_LEVELS = (
    "casual",
    "elegant",
    "ethnic",
    "sporty",
)
FASHION_AESTHETIC_INSTRUCTION = (
    "Fashion aesthetic must be exactly one of:"
    f" {', '.join(FASHION_AESTHETIC_LEVELS)}."
    " casual = relaxed everyday wear or simple street-casual styling;"
    " elegant = refined, polished, formal, glam, or luxury-leaning styling;"
    " ethnic = traditional or cultural dress, regional attire, or heritage"
    " fashion cues (including fusion looks where traditional dress dominates);"
    " sporty = athleisure, activewear, or gym-to-street athletic styling."
)

GROOMING_LEVELS = ("well_groomed", "casual")
GROOMING_INSTRUCTION = (
    "Grooming level must be exactly one of:"
    f" {', '.join(GROOMING_LEVELS)}."
    " well_groomed = neat hair, intentional makeup or skincare, polished personal"
    " presentation;"
    " casual = low-key or natural grooming — minimal makeup, relaxed hair,"
    " everyday upkeep."
)

SOCIOECONOMIC_INDICATOR_LEVELS = ("premium", "mid_tier", "budget")
SOCIOECONOMIC_INDICATOR_INSTRUCTION = (
    "Socioeconomic indicator must be exactly one of:"
    f" {', '.join(SOCIOECONOMIC_INDICATOR_LEVELS)}."
    " premium = luxury or high-end lifestyle cues (upscale setting, premium"
    " products, high-end decor or travel);"
    " mid_tier = mainstream, middle-market, relatable everyday setting and"
    " products;"
    " budget = value-focused, economy-tier products, deals, or basic/minimal"
    " setting cues."
)

SKIN_CARE_CONSCIOUSNESS_LEVELS = (
    "minimal",
    "basic_routine",
    "moderate",
    "high_ingredient_focused",
)
SKIN_CARE_CONSCIOUSNESS_INSTRUCTION = (
    "Skin care consciousness must be exactly one of:"
    f" {', '.join(SKIN_CARE_CONSCIOUSNESS_LEVELS)}."
    " minimal = little or no skincare focus (makeup-only, fashion, or no"
    " regimen cues);"
    " basic_routine = simple routine shown or mentioned (e.g. cleanse,"
    " moisturize, sunscreen);"
    " moderate = clear multi-step skincare routine or regular skin-health"
    " care emphasis;"
    " high_ingredient_focused = strong ingredient, active, or formulation"
    " focus (e.g. retinol, vitamin C, SPF science, actives education)."
)

AUTHENTICITY_FEEL_LEVELS = (
    "relatable",
    "curated",
    "highly_polished",
    "raw_authentic",
)
AUTHENTICITY_FEEL_INSTRUCTION = (
    "Authenticity feel must be exactly one of:"
    f" {', '.join(AUTHENTICITY_FEEL_LEVELS)}."
    " relatable = everyday, audience-connected, down-to-earth creator delivery;"
    " curated = intentional, aesthetic creator style with controlled presentation;"
    " highly_polished = studio-grade, commercial, or heavily produced presentation;"
    " raw_authentic = unfiltered, spontaneous, lo-fi real-moment feel."
)

# Suggested tone labels for emotional_tone (guidance only — value is free text, not an enum).
EMOTIONAL_TONE_EXAMPLE_LABELS = (
    "relatable, energetic, honest, conversational, educational, cultural,"
    " aesthetic, joyful, emotional, aspirational, heartfelt, dramatic,"
    " humorous, playful, witty, informative, bold and confident,"
    " calm and minimalist, reflective, nostalgic, critical, passionate,"
    " spiritual, authoritative, empowering, enthusiastic, raw and vulnerable,"
    " inspirational, celebratory, warm and nurturing, curated"
)
EMOTIONAL_TONE_GUIDANCE = (
    "Set 'value' to a short primary tone label (lowercase preferred)."
    " Common examples include:"
    f" {EMOTIONAL_TONE_EXAMPLE_LABELS}."
    " These are suggestions only — use the best-fit label or a close synonym;"
    " do not treat this list as a closed enum."
)

# Suggested editing-style labels (guidance only — value is free text, not an enum).
EDITING_STYLE_EXAMPLE_LABELS = (
    "Minimal Editing, Raw & Unedited, Trending Template (CapCut / Instagram),"
    " Montage, B-roll Heavy, Transition-Heavy, Speed Ramp / Reverse"
)
EDITING_STYLE_GUIDANCE = (
    "Set 'value' to a comma-separated list of editing-style labels, with the"
    " best-fit or dominant style first. Use one label when a single style"
    " clearly applies."
    " Common examples include:"
    f" {EDITING_STYLE_EXAMPLE_LABELS}."
    " These are suggestions only — use the best-fit labels or close synonyms;"
    " do not treat this list as a closed enum."
)

# Suggested camera-movement labels (guidance only — value is free text, not an enum).
CAMERA_MOVEMENT_EXAMPLE_LABELS = (
    "Selfie-mode, Handheld, Static, POV (Point of View), Cinematic Movement"
)
CAMERA_MOVEMENT_GUIDANCE = (
    "Set 'value' to a comma-separated list of camera-movement or framing"
    " labels, with the best-fit or dominant style first. Use one label when a"
    " single style clearly applies."
    " Common examples include:"
    f" {CAMERA_MOVEMENT_EXAMPLE_LABELS}."
    " These are suggestions only — use the best-fit labels or close synonyms;"
    " do not treat this list as a closed enum."
)

TEXT_OVERLAY_LEVELS = ("none", "light", "medium", "heavy")
TEXT_OVERLAY_INSTRUCTION = (
    "Text overlay density must be exactly one of:"
    f" {', '.join(TEXT_OVERLAY_LEVELS)}."
    " none = no meaningful on-screen text or graphics added in edit;"
    " light = sparse or occasional overlays (brief titles, few labels);"
    " medium = moderate overlay use (regular captions, several text moments);"
    " heavy = frequent or persistent text throughout most of the content."
)

FACE_VISIBILITY_INSTRUCTION = (
    "Set 'value' to a face visibility score from 0 to 100 (string integer,"
    " e.g. '0', '35', '72', '95')."
    " 0 = no human face clearly visible;"
    " 1–25 = brief or incidental face appearances;"
    " 26–50 = face visible but not a main focus;"
    " 51–75 = face clearly visible for a meaningful portion;"
    " 76–100 = close-up face dominates or anchors most of the content."
)

# Suggested color-grade labels (guidance only — value is free text, not an enum).
COLOR_GRADE_EXAMPLE_LABELS = (
    "Warm, Cool, Neutral, High-Contrast, Muted / Desaturated, Vibrant,"
    " Cinematic, Flat / Natural, Vintage / Faded"
)
COLOR_GRADE_GUIDANCE = (
    "Set 'value' to a comma-separated list of color-grade or visual-look"
    " labels, with the best-fit or dominant look first. Use one label when a"
    " single look clearly applies."
    " Common examples include:"
    f" {COLOR_GRADE_EXAMPLE_LABELS}."
    " These are suggestions only — use the best-fit labels or close synonyms;"
    " do not treat this list as a closed enum."
)

LIGHTING_QUALITY_INSTRUCTION = (
    "Set 'value' to a decimal lighting quality score from 0 to 5"
    " (e.g. '0', '2.5', '3.5', '4.2'). Any decimal in that range is valid."
    " 0 = unusable — subject not visible or lighting fails completely;"
    " 1 = very poor — severely under/overexposed, key detail lost;"
    " 2 = poor — notable darkness, glare, or uneven light;"
    " 3 = acceptable — subject visible, minor lighting issues;"
    " 4 = good — even, clear lighting with good subject visibility;"
    " 5 = excellent — flattering, well-balanced, supports fine detail."
)

TECHNICAL_QUALITY_TIER_LEVELS = ("high", "medium", "low")
AUDIO_QUALITY_INSTRUCTION = (
    "Audio quality tier must be exactly one of:"
    f" {', '.join(TECHNICAL_QUALITY_TIER_LEVELS)}."
    " high = clear and intelligible — speech easy to hear, consistent volume,"
    " no distracting noise or distortion;"
    " medium = generally understandable with minor issues — slight background"
    " noise, occasional muffling, or uneven volume that does not block"
    " comprehension;"
    " low = poor — clipping, severe noise, muffled or inconsistent audio that"
    " hinders understanding."
)
VIDEO_QUALITY_INSTRUCTION = (
    "Video quality tier must be exactly one of:"
    f" {', '.join(TECHNICAL_QUALITY_TIER_LEVELS)}."
    " high = sharp, stable, well-framed, comfortable to watch;"
    " medium = watchable with minor issues — slight blur, mild shake,"
    " compression artifacts, or framing quirks that do not seriously distract;"
    " low = poor — excessive blur, severe shake, bad framing, low resolution,"
    " or artifacts that make viewing uncomfortable."
)

AUDIO_TYPE_LEVELS = (
    "background_music_only",
    "original_voice",
    "dialogue_driven",
    "mixed",
)
AUDIO_TYPE_INSTRUCTION = (
    "Audio type must be exactly one of:"
    f" {', '.join(AUDIO_TYPE_LEVELS)}."
    " background_music_only = music or trending sound carries the audio with"
    " no meaningful speech or narration;"
    " original_voice = creator voice-over, narration, or original spoken track"
    " drives the content (speech-led, music optional or absent);"
    " dialogue_driven = on-camera conversation or direct-to-camera speech"
    " drives the content;"
    " mixed = no single type clearly dominates — e.g. equal voice-over and"
    " music, or shifting dialogue and music-led segments."
)

MUSIC_DIALOGUE_BALANCE_LEVELS = (
    "balanced",
    "music_dominant",
    "dialogue_dominant",
)
MUSIC_DIALOGUE_BALANCE_INSTRUCTION = (
    "Music–dialogue balance must be exactly one of:"
    f" {', '.join(MUSIC_DIALOGUE_BALANCE_LEVELS)}."
    " balanced = music and speech coexist at similar perceptual weight and"
    " speech remains intelligible;"
    " music_dominant = music is louder or more prominent, risking or reducing"
    " speech intelligibility;"
    " dialogue_dominant = speech clearly leads and music is subtle, absent, or"
    " clearly in the background."
)

SPEECH_PACE_LEVELS = ("fast", "moderate", "slow")
SPEECH_PACE_INSTRUCTION = (
    "Speech pace must be exactly one of:"
    f" {', '.join(SPEECH_PACE_LEVELS)}."
    " fast = rapid delivery that may feel rushed;"
    " moderate = comfortable, easy-to-follow pace for typical viewers;"
    " slow = deliberately slow or drawn-out delivery."
)

SPEECH_CLARITY_LEVELS = ("clear", "accented_but_clear", "unclear")
SPEECH_CLARITY_INSTRUCTION = (
    "Speech clarity must be exactly one of:"
    f" {', '.join(SPEECH_CLARITY_LEVELS)}."
    " clear = easy to understand with good articulation;"
    " accented_but_clear = noticeable accent or dialect but still easy to"
    " follow;"
    " unclear = mumbled, heavily overlapped, or hard to understand."
)

NARRATION_STYLE_EXAMPLE_LABELS = (
    "First Person Storytelling, Third Person Narration, Direct Address,"
    " Voice-over Exposition, Tutorial / Instructional, Testimonial / Personal"
    " Experience, Interview / Conversation, Dramatic Monologue"
)
NARRATION_STYLE_GUIDANCE = (
    "Set 'value' to a short primary narration-style label describing how"
    " speech is delivered (point of view, format, and narrative mode)."
    " Common examples include:"
    f" {NARRATION_STYLE_EXAMPLE_LABELS}."
    " These are suggestions only — use the best-fit label or a close synonym;"
    " do not treat this list as a closed enum."
)

LANGUAGE_ACCENT_EXAMPLE_LABELS = (
    "Hinglish, Multilingual, Hindi, English (Indian), English (US),"
    " English (UK), Tamil, Telugu, Bengali, Marathi, Spanish (LatAm),"
    " Arabic, French"
)
LANGUAGE_ACCENT_GUIDANCE = (
    "Set 'value' to a short primary language or language-mix label when"
    " speech is present (free text, not an enum)."
    " Common examples include:"
    f" {LANGUAGE_ACCENT_EXAMPLE_LABELS}."
    " Hinglish = Hindi–English code-mixing; Multilingual = two or more"
    " languages used substantially with no single clear primary language."
    " These are suggestions only — use the best-fit label or a close synonym;"
    " do not treat this list as a closed enum."
)

SECONDARY_LANGUAGE_GUIDANCE = (
    "Set 'value' to the secondary spoken language label (free text, not an"
    " enum) when a distinct second language is clearly used — e.g. 'English',"
    " 'Hindi', 'Spanish'. Use empty or omit only if not applicable."
)


def get_content_intelligence_feature_configs() -> list[VideoFeature]:
  """Gets all content intelligence and safety feature configurations."""
  return [
      # ------------------------------------------------------------------ #
      # Group 1 – Quality & Clarity                                         #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="content_clarity_focus",
          name="Content Clarity & Focus",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="QUALITY_CLARITY",
          evaluation_criteria="""
              The content has a single, clear main message that is easy to
              understand. The content does not feel cluttered, contradictory,
              or unfocused with too many unrelated topics.
          """,
          prompt_template="""
              Is the main message of this content clear, focused, and easy
              to understand throughout?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess whether the content stays focused on one main idea"
                  " or topic, or whether it jumps between multiple unrelated"
                  " subjects in a confusing way."
              ),
              (
                  "Return True if and only if the content has a clear,"
                  " focused main message that is easy to follow."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="narrative_structure",
          name="Narrative Structure",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="QUALITY_CLARITY",
          evaluation_criteria="""
              The content follows a coherent structure with a clear beginning
              (setup or hook), a middle (development or explanation), and an
              end (conclusion, payoff, or resolution). The progression feels
              logical and intentional rather than random or abrupt.
          """,
          prompt_template="""
              Does this content have a coherent narrative structure with a
              clear beginning, middle, and end?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Look for a clear setup or hook at the start, meaningful"
                  " development in the middle, and a satisfying conclusion"
                  " or payoff at the end."
              ),
              (
                  "Return True if and only if the content follows a logical,"
                  " coherent structure from start to finish."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="informational_depth",
          name="Informational Depth",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="QUALITY_CLARITY",
          evaluation_criteria="""
              The content provides substantive information, concrete facts,
              useful insights, or clear explanations rather than relying
              solely on vague buzzwords, generic statements, or surface-level
              observations with no real substance.
          """,
          prompt_template="""
              Does this content provide substantive, informative content
              rather than shallow or vague statements?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Look for concrete facts, specific examples, practical"
                  " insights, or clear explanations that add genuine value."
              ),
              (
                  "Return True if and only if the content goes beyond generic"
                  " buzzwords and provides real informational depth."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="production_quality",
          name="Acceptable Production Quality",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria="""
              The visual and audio quality of the content is acceptable for
              its intended platform. The video is not distractingly shaky,
              blurry, or poorly framed, and the audio is not inaudible,
              distorted, or excessively noisy.
          """,
          prompt_template="""
              Is the production quality of this content acceptable — visually
              and audibly clear enough to consume comfortably?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess both visual quality (stability, clarity, framing,"
                  " lighting) and audio quality (clarity, volume, background"
                  " noise)."
              ),
              (
                  "Note: content does not need to be professional-grade;"
                  " it just needs to be watchable and audible without"
                  " significant distraction."
              ),
              (
                  "Return True if and only if the production quality is"
                  " acceptable for comfortable consumption."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      # ------------------------------------------------------------------ #
      # Group 2 – Meaningfulness & Value                                    #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="actionable_value",
          name="Actionable Value",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="VALUE",
          evaluation_criteria="""
              The content gives the viewer something concrete and practical:
              a tip, step, insight, demonstration, or clear takeaway they can
              apply, learn, or do. The content is not purely promotional fluff
              or entertainment with no practical value.
          """,
          prompt_template="""
              Does this content provide the viewer with concrete, actionable
              value — something they can learn, do, or apply?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Look for explicit tips, how-to steps, demonstrations,"
                  " useful information, or a clear lesson or takeaway."
              ),
              (
                  "Return True if and only if the content delivers at least"
                  " one concrete, practical takeaway for the viewer."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="audience_relevance",
          name="Audience Relevance",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="VALUE",
          evaluation_criteria="""
              The content's message, tone, language, and examples feel
              well-matched and relevant to the apparent target audience.
              The viewer the content seems to be aimed at would find it
              applicable and meaningful to their context, interests, or needs.
          """,
          prompt_template="""
              Does this content feel relevant and well-matched to the audience
              it appears to be targeting?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "First, infer the apparent target audience from the content"
                  " itself (e.g. based on topic, tone, language, and examples)."
              ),
              (
                  "Then assess whether the message, examples, and language"
                  " style are genuinely relevant and useful for that audience."
              ),
              (
                  "Return True if and only if the content feels well-matched"
                  " and relevant to its apparent target audience."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="engagement_potential",
          name="Engagement Potential",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="VALUE",
          evaluation_criteria="""
              The content has one or more elements likely to drive viewer
              engagement: a strong hook in the opening, a relatable or
              emotionally resonant moment, a compelling question or challenge,
              a surprising reveal, or a satisfying payoff that would motivate
              viewers to comment, share, or react.
          """,
          prompt_template="""
              Does this content have strong engagement potential — elements
              likely to drive viewer reaction, sharing, or commenting?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Look for a strong hook in the first few seconds, relatable"
                  " or emotionally resonant moments, questions that invite"
                  " responses, surprising content, or a satisfying payoff."
              ),
              (
                  "Return True if and only if the content has clear elements"
                  " that would motivate viewer engagement."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="low_effort_spam",
          name="Not Low-Effort / Spam",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TRUST",
          evaluation_criteria="""
              The content is original and substantive. It is NOT filler
              content, repetitive padding, a repost of existing content
              with no added value, or content clearly generated with no
              effort or creative intent.
          """,
          prompt_template="""
              Is this content original and substantive — not filler, spam,
              or low-effort reposted content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Look for signs of low effort: repetitive content with no"
                  " new angle, obvious filler without purpose, or clearly"
                  " reposted/recycled material with zero original contribution."
              ),
              (
                  "Return True if and only if the content appears original"
                  " and has been created with genuine effort and intent."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      # ------------------------------------------------------------------ #
      # Group 3 – Authenticity & Trust                                      #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="authenticity_feel",
          name="Authenticity Feel",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TRUST",
          evaluation_criteria=f"""
              Classify the dominant authenticity feel of the content — how
              relatable, curated, polished, or raw the creator delivery and
              framing feels (not factual trust or misinformation; see
              misinformation_risk).
              {AUTHENTICITY_FEEL_INSTRUCTION}
          """,
          prompt_template="""
              What is the dominant authenticity feel of this content
              (creator delivery and presentation)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              AUTHENTICITY_FEEL_INSTRUCTION,
              (
                  "Focus on delivery and presentation feel — not whether the"
                  " content is an ad (genuine_vs_ad) or communication style alone."
              ),
              (
                  "relatable vs curated: everyday peer connection vs intentional"
                  " aesthetic creator control."
              ),
              (
                  "raw_authentic vs highly_polished: spontaneous lo-fi moments vs"
                  " studio/commercial production."
              ),
              (
                  "curated vs highly_polished: styled creator content vs"
                  " full commercial-grade polish."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "Return detected=True if and only if authenticity feel is"
                  " clearly inferable from delivery and framing."
              ),
              (
                  "Return detected=False if feel is too neutral or generic"
                  " to classify."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="misinformation_risk",
          name="Misinformation Risk",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="SAFETY",
          evaluation_criteria="""
              The content makes specific factual claims that appear
              unverifiable, scientifically questionable, statistically
              exaggerated, or potentially misleading — particularly in
              sensitive domains such as health, finance, safety, or science.
              Return True if misinformation risk IS present; False if the
              content appears factually responsible.
          """,
          prompt_template="""
              Does this content contain claims that appear unverifiable,
              exaggerated, or potentially misleading (misinformation risk)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Look specifically for absolute, unhedged claims in health,"
                  " finance, science, or safety areas that lack credible"
                  " basis, cite no sources, or contradict established knowledge."
              ),
              (
                  "Do NOT flag personal opinions, cultural views, or mild"
                  " exaggeration as misinformation. Only flag specific factual"
                  " claims that appear genuinely misleading."
              ),
              (
                  "Return True if and only if the content contains specific"
                  " claims that pose a meaningful misinformation risk."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="clickbait_detection",
          name="Clickbait Detection",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="QUALITY_CLARITY",
          evaluation_criteria="""
              The opening, hook, or framing of the content promises something
              (a reveal, answer, outcome, or shocking fact) that the content
              ultimately fails to deliver. The viewer is baited with an
              enticing premise that is never fulfilled or is dramatically
              overstated. Return True if clickbait IS detected.
          """,
          prompt_template="""
              Does this content use clickbait — promising something in the
              hook or opening that the content fails to actually deliver?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess whether the opening hook, title-style text, or"
                  " initial premise makes a promise (a big reveal, shocking"
                  " secret, dramatic answer) that the content ultimately"
                  " does not fulfil or dramatically overstates."
              ),
              (
                  "Return True if and only if there is a clear mismatch"
                  " between what the opening promises and what is delivered."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      # ------------------------------------------------------------------ #
      # Group 4 – Safety & Appropriateness                                  #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="negativity_hate_speech",
          name="Negativity / Hate Speech",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="SAFETY",
          evaluation_criteria="""
              The content contains hateful, harassing, or demeaning language
              or imagery directed at individuals or groups based on
              characteristics such as race, ethnicity, gender, religion,
              sexual orientation, disability, or national origin. This
              includes explicit verbal abuse, sustained targeted harassment,
              or content designed to humiliate. Return True if hate speech
              or strong negativity IS present.
          """,
          prompt_template="""
              Does this content contain hate speech, harassment, or strong
              targeted negativity toward individuals or groups?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Look for language or imagery that demeans, harasses, or"
                  " attacks individuals or groups based on protected"
                  " characteristics."
              ),
              (
                  "Do NOT flag mild criticism, disagreement, debate, satire,"
                  " or general negative sentiment as hate speech. Only flag"
                  " content that is clearly hateful or harassing."
              ),
              (
                  "Return True if and only if the content contains clear"
                  " hate speech, harassment, or targeted demeaning content."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="brand_safety",
          name="Brand Safety Risk",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="SAFETY",
          evaluation_criteria="""
              The content involves sensitive or controversial topics that
              would pose a risk for brand association, including: graphic
              violence, extreme political content, adult or sexually explicit
              material, dangerous or illegal activities, substance abuse, or
              content that glorifies harm. Return True if a brand safety
              risk IS present.
          """,
          prompt_template="""
              Does this content pose a brand safety risk — containing
              sensitive, controversial, or explicit material unsuitable
              for brand association?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess whether the content contains graphic violence,"
                  " adult material, extreme political views, dangerous"
                  " activities, substance abuse, or other categories that"
                  " responsible brands would avoid being associated with."
              ),
              (
                  "Return True if and only if the content poses a meaningful"
                  " brand safety risk."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="audience_appropriateness",
          name="Audience Appropriateness",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="SAFETY",
          evaluation_criteria="""
              The content is suitable for a general, broad audience — it
              does not contain mature, explicit, age-restricted, or
              otherwise inappropriate material that would make it unsuitable
              for general consumption across age groups.
          """,
          prompt_template="""
              Is this content appropriate for a general, broad audience
              across age groups?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess whether the content contains mature language,"
                  " explicit visuals, adult themes, or anything that would"
                  " make it unsuitable for a general audience."
              ),
              (
                  "Return True if and only if the content is appropriate"
                  " for a general, broad audience."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="cultural_sensitivity",
          name="Cultural Sensitivity",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="SAFETY",
          evaluation_criteria="""
              The content respects cultural contexts and does not contain
              cultural appropriation, stereotyping, or material that is
              likely to be perceived as culturally insensitive, offensive,
              or tone-deaf by cultural groups being referenced or depicted.
          """,
          prompt_template="""
              Is this content culturally sensitive — respectful of cultural
              contexts and not culturally appropriative or offensive?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess whether the content handles cultural references,"
                  " traditions, or communities with respect and awareness,"
                  " or whether it risks being culturally insensitive,"
                  " appropriative, or stereotyping."
              ),
              (
                  "Return True if and only if the content is culturally"
                  " sensitive and respectful."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=False,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      # ------------------------------------------------------------------ #
      # Group 5 – Content Diagnostics (LLM-only, boolean + evidence)         #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="genre_levels",
          name="Genre Levels",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="GENRE_LEVELS",
          evaluation_criteria=f"""
              Classify content genre levels ranked by emphasis (most talked about
              or shown first). {GENRE_LEVEL_GUIDANCE}
              Sub-genres are free text that refine a level (e.g. beauty → makeup
              tutorial).
          """,
          prompt_template="""
              Classify this content's genre levels (primary, sub-genre,
              secondary, secondary sub-genres, and other levels by emphasis).
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              GENRE_LEVEL_GUIDANCE,
              (
                  "Set 'value' to a JSON object string with exactly these keys:"
                  " primary_genre, sub_genre, secondary_genre,"
                  " secondary_sub_genres, other_genres."
              ),
              (
                  "primary_genre, secondary_genre: short genre labels ranked by"
                  " emphasis. Use empty string for secondary_genre if N/A."
              ),
              (
                  "other_genres: JSON array of additional genre labels for 3rd"
                  " rank and below, or [] if none."
              ),
              (
                  "sub_genre: free text refining primary_genre, or empty string."
              ),
              (
                  "secondary_sub_genres: free text refining secondary_genre, or"
                  " empty string."
              ),
              (
                  'Example value:'
                  ' {"primary_genre":"beauty","sub_genre":"lipstick review",'
                  '"secondary_genre":"lifestyle","secondary_sub_genres":"",'
                  '"other_genres":["entertainment"]}'
              ),
              (
                  "Return detected=True if and only if primary_genre is set to"
                  " a non-empty genre label."
              ),
              (
                  "Summarize ranking rationale in evidence and rationale."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="emotional_tone",
          name="Emotional Tone",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria=f"""
              The content communicates a clear emotional tone or mood that is
              consistent for most of the content (delivery, visuals, and audio).
              {EMOTIONAL_TONE_GUIDANCE}
          """,
          prompt_template="""
              What is the primary emotional tone of this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              EMOTIONAL_TONE_GUIDANCE,
              (
                  "Tone is mood and emotional feel — not communication format"
                  " (communication_style) or authenticity presentation"
                  " (authenticity_feel)."
              ),
              (
                  "Pick one primary tone label. Use a second tone in evidence"
                  " only if there is a clear shift mid-content."
              ),
              (
                  "Return detected=True if and only if the tone is clearly"
                  " inferable from delivery, visuals, and audio."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="fashion_aesthetic",
          name="Fashion Aesthetic",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="FASHION_AESTHETIC",
          evaluation_criteria=f"""
              Classify the dominant fashion aesthetic shown through outfits,
              styling, and wardrobe cues visible in the content.
              {FASHION_AESTHETIC_INSTRUCTION}
          """,
          prompt_template="""
              What is the dominant fashion aesthetic in this content (outfits
              and styling)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              FASHION_AESTHETIC_INSTRUCTION,
              (
                  "Base the label on clothing, accessories, and styling visible"
                  " on people in frame — not genre (genre_levels) or production"
                  " polish alone."
              ),
              (
                  "casual vs elegant: everyday relaxed wear vs refined, dressy,"
                  " glam, or luxury-leaning presentation."
              ),
              (
                  "ethnic = traditional, cultural, or regional attire is the"
                  " dominant styling signal (include fusion when traditional"
                  " elements clearly lead)."
              ),
              (
                  "sporty vs casual: athletic/activewear-led vs general everyday"
                  " relaxed wear."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase)"
                  " when a fashion aesthetic applies."
              ),
              (
                  "Return detected=True if and only if outfit/fashion styling is"
                  " visible and one label clearly fits."
              ),
              (
                  "Return detected=False if fashion styling is not visible,"
                  " not assessable, or too generic to classify."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="grooming",
          name="Grooming",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="GROOMING",
          evaluation_criteria=f"""
              Classify the dominant personal grooming level visible on people
              in the content — hair, makeup, skin, and overall neatness of
              personal appearance (not clothing; see fashion_aesthetic).
              {GROOMING_INSTRUCTION}
          """,
          prompt_template="""
              What is the dominant grooming level in this content (hair, makeup,
              skin, personal presentation)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              GROOMING_INSTRUCTION,
              (
                  "Assess personal grooming only — not outfits (fashion_aesthetic)"
                  " or video production quality."
              ),
              (
                  "well_groomed vs casual: intentional polished presentation vs"
                  " natural, minimal, or relaxed grooming."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "Return detected=True if and only if a person is visible and"
                  " grooming level is assessable."
              ),
              (
                  "Return detected=False if no person is visible or grooming"
                  " cannot be judged."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="socioeconomic_indicator",
          name="Socioeconomic Indicator",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="SOCIOECONOMIC",
          evaluation_criteria=f"""
              Classify the dominant socioeconomic lifestyle tier suggested by
              visible setting, products, decor, and consumption cues in the
              content — not by inferring identity from people.
              {SOCIOECONOMIC_INDICATOR_INSTRUCTION}
          """,
          prompt_template="""
              What socioeconomic lifestyle tier do the setting and lifestyle
              cues in this content suggest?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              SOCIOECONOMIC_INDICATOR_INSTRUCTION,
              (
                  "Use observable cues only: home/setting quality, product tier,"
                  " brands shown, travel/leisure signals, and decor — not"
                  " ethnicity, body type, or stereotypes about people."
              ),
              (
                  "premium vs mid_tier: clearly upscale/luxury cues vs"
                  " mainstream, everyday, middle-market presentation."
              ),
              (
                  "mid_tier vs budget: ordinary mainstream setting vs explicit"
                  " value/deal focus or economy-tier products and basic setting."
              ),
              (
                  "Do not conflate with fashion_aesthetic elegant or production"
                  " polish alone — focus on lifestyle/setting tier."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "Return detected=True if and only if lifestyle tier cues are"
                  " visible and one label clearly fits."
              ),
              (
                  "Return detected=False if cues are insufficient, generic,"
                  " or not assessable."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="skin_care_consciousness",
          name="Skin Care Consciousness",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="SKIN_CARE_CONSCIOUSNESS",
          evaluation_criteria=f"""
              Classify how strongly the content reflects intentional skincare
              awareness — routines, skin health, and product/regimen focus
              (not general grooming polish alone; see grooming).
              {SKIN_CARE_CONSCIOUSNESS_INSTRUCTION}
          """,
          prompt_template="""
              How skin-care conscious is this content (routine depth, skin
              health, and ingredient focus)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              SKIN_CARE_CONSCIOUSNESS_INSTRUCTION,
              (
                  "Assess skincare as a practice or topic — not just whether"
                  " skin looks good (grooming) or whether genre is beauty"
                  " (genre_levels)."
              ),
              (
                  "minimal vs basic_routine: no regimen cues vs simple cleanse/"
                  " moisturize/SPF routine."
              ),
              (
                  "moderate vs high_ingredient_focused: multi-step care or"
                  " routine emphasis vs detailed actives/ingredient education."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "Return detected=True if and only if beauty/personal-care"
                  " context is present and skincare consciousness is assessable."
              ),
              (
                  "Return detected=False if content is unrelated to beauty/skin"
                  " care or skincare level cannot be judged."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="audio_quality",
          name="Audio Quality",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria=f"""
              Classify overall audio quality: speech (if present) should be
              intelligible, volume consistent, and noise/distortion should not
              hinder understanding.
              {AUDIO_QUALITY_INSTRUCTION}
          """,
          prompt_template="""
              What is the overall audio quality tier of this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              AUDIO_QUALITY_INSTRUCTION,
              (
                  "In evidence, cite concrete audio cues (clarity, volume,"
                  " background noise, distortion, muffling)."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase):"
                  " high, medium, or low."
              ),
              (
                  "Return detected=True if and only if value is 'high' or"
                  " 'medium' (acceptable audio or better)."
              ),
              (
                  "Return detected=False if value is 'low', there is no"
                  " assessable audio, or quality cannot be judged."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="video_quality",
          name="Video Quality",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria=f"""
              Classify overall visual quality: footage should be clear enough
              to comfortably watch — not excessively blurry, pixelated, poorly
              framed, or distracting due to severe shake.
              {VIDEO_QUALITY_INSTRUCTION}
          """,
          prompt_template="""
              What is the overall video quality tier of this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              VIDEO_QUALITY_INSTRUCTION,
              (
                  "In evidence, cite the dominant visual cues (sharpness, shake,"
                  " framing, resolution, compression artifacts)."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase):"
                  " high, medium, or low."
              ),
              (
                  "Return detected=True if and only if value is 'high' or"
                  " 'medium' (watchable quality or better)."
              ),
              (
                  "Return detected=False if value is 'low' or video quality"
                  " cannot be assessed."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="lighting_quality",
          name="Lighting Quality",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria=f"""
              Rate lighting quality on a 0–5 scale. Lighting should support
              viewing: subject(s) visible, exposure balanced, key details not
              lost to glare or severe backlighting.
              {LIGHTING_QUALITY_INSTRUCTION}
          """,
          prompt_template="""
              Rate the lighting quality in this content on a decimal scale of
              0 to 5.
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              LIGHTING_QUALITY_INSTRUCTION,
              (
                  "In evidence, cite concrete lighting cues (exposure, shadows,"
                  " backlight, flicker, natural vs artificial)."
              ),
              (
                  "Return detected=True if and only if the numeric score is"
                  " 3.0 or higher (acceptable lighting or better)."
              ),
              (
                  "Return detected=False if the score is below 3.0 or lighting"
                  " cannot be assessed."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="camera_movement",
          name="Camera Movement",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria=f"""
              Classify the camera movement or framing style(s) — how the camera
              is held, positioned, and moved (or kept still) throughout the
              content. Multiple styles may apply.
              {CAMERA_MOVEMENT_GUIDANCE}
          """,
          prompt_template="""
              What camera movement or framing style(s) appear in this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              CAMERA_MOVEMENT_GUIDANCE,
              (
                  "Selfie-mode = front-facing arm's-length creator shot;"
                  " Handheld = noticeable hand-held motion; Static = fixed or"
                  " tripod-locked frame; POV = first-person viewer perspective;"
                  " Cinematic Movement = deliberate pans, tracking, dolly, or"
                  " stabilized cinematic motion."
              ),
              (
                  "Include multiple labels when clearly present (e.g."
                  " 'Handheld, Selfie-mode'). Order by dominance; list at most"
                  " 3 labels."
              ),
              (
                  "In evidence, cite concrete cues (shake, pan, tracking, fixed"
                  " frame, front-camera angle, POV framing)."
              ),
              (
                  "Return detected=True if and only if at least one camera"
                  " movement or framing style is clearly inferable."
              ),
              (
                  "Return detected=False if movement/framing cannot be assessed"
                  " (e.g. static image with no video motion cues)."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="editing_style",
          name="Editing Style",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria=f"""
              The content demonstrates discernible editing style(s) (cuts, pacing,
              templates, transitions, B-roll, speed effects). Multiple styles
              may apply.
              {EDITING_STYLE_GUIDANCE}
          """,
          prompt_template="""
              What editing style(s) are used in this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              EDITING_STYLE_GUIDANCE,
              (
                  "Include multiple labels when clearly present (e.g."
                  " 'Montage, Transition-Heavy'). Order by dominance; list at"
                  " most 3 labels."
              ),
              (
                  "In evidence, cite 1–2 concrete markers (jump cuts, template"
                  " overlays, beat-synced cuts, speed ramps, B-roll inserts)."
              ),
              (
                  "Return detected=True if and only if at least one editing"
                  " style is clearly inferable from observable cues."
              ),
              (
                  "Return detected=False if editing is not discernible or cannot"
                  " be assessed (e.g. static image with no edit cues)."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="text_overlay",
          name="Text Overlay",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="VISUAL_STYLE",
          evaluation_criteria=f"""
              Classify how much on-screen text overlay is used — burned-in
              captions, titles, product labels, CTAs, stickers, and other
              graphics added in edit (not platform caption metadata).
              {TEXT_OVERLAY_INSTRUCTION}
          """,
          prompt_template="""
              How heavy is the on-screen text overlay usage in this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              TEXT_OVERLAY_INSTRUCTION,
              (
                  "Assess on-screen text/graphics in the video or image — not"
                  " the platform caption/description metadata."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase):"
                  " none, light, medium, or heavy."
              ),
              (
                  "In evidence, cite concrete examples (what text appears, how"
                  " often, placement, persistence)."
              ),
              (
                  "Return detected=True if and only if value is 'light',"
                  " 'medium', or 'heavy' (on-screen overlay is present)."
              ),
              (
                  "Return detected=False if value is 'none' or overlay density"
                  " cannot be assessed."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="face_visibility",
          name="Face Visibility",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="VISUAL_STYLE",
          evaluation_criteria=f"""
              Score how visibly a human face appears across the full content
              from 0 to 100 — presence, prominence, and framing (not eye contact
              or gaze).
              {FACE_VISIBILITY_INSTRUCTION}
          """,
          prompt_template="""
              Score face visibility in this content from 0 to 100.
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              FACE_VISIBILITY_INSTRUCTION,
              (
                  "Assess face visibility across the full video or image — not"
                  " only the first 5 seconds (c_visible_face)."
              ),
              (
                  "Cartoon, animated, or illustrated human faces count as faces."
              ),
              (
                  "In evidence, cite when the face appears, framing (wide vs"
                  " close-up), and how you mapped prominence to the score."
              ),
              (
                  "Return detected=True if and only if the numeric score is"
                  " greater than 0 (a face is visible)."
              ),
              (
                  "Return detected=False if the score is 0 or face visibility"
                  " cannot be assessed."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="color_grade",
          name="Color Grade",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="VISUAL_STYLE",
          evaluation_criteria=f"""
              Classify the overall color grading / visual look of the content.
              Multiple looks may apply across scenes.
              {COLOR_GRADE_GUIDANCE}
          """,
          prompt_template="""
              What color grade or visual look(s) characterize this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              COLOR_GRADE_GUIDANCE,
              (
                  "Include multiple labels when clearly present (e.g."
                  " 'Warm, High-Contrast'). Order by dominance; list at most"
                  " 3 labels."
              ),
              (
                  "In evidence, cite concrete visual cues (white balance, contrast,"
                  " saturation, film-like tone, faded/vintage cast)."
              ),
              (
                  "Return detected=True if and only if at least one color-grade"
                  " or visual look is clearly inferable from the visuals."
              ),
              (
                  "Return detected=False if the look cannot be assessed from"
                  " the available media."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="narration_present",
          name="Narration",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria="""
              The content includes narration or a guiding spoken track that explains,
              describes, or tells the story (voice-over or on-camera narration).
          """,
          prompt_template="""
              Is there narration guiding the viewer through the content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "In evidence, specify whether the narration is voice-over,"
                  " on-camera, or mixed."
              ),
              (
                  "Return True if and only if narration is a meaningful part of how"
                  " the content communicates."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="narration_style",
          name="Narration Style",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria=f"""
              When narration or meaningful speech is present, classify the
              narration style — point of view, narrative mode, and how the
              speaker delivers the story or message.
              Not the same as ad-like feel (genuine_vs_ad) or communication
              format (communication_style).
              {NARRATION_STYLE_GUIDANCE}
          """,
          prompt_template="""
              What is the primary narration style of this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              NARRATION_STYLE_GUIDANCE,
              (
                  "First Person Storytelling = speaker tells their own story"
                  " using I/me; Direct Address = speaks straight to viewer;"
                  " Voice-over Exposition = detached narrator over visuals."
              ),
              (
                  "Assess narration mode only — not whether delivery feels"
                  " scripted vs organic (use evidence for nuance) or whether"
                  " content is an ad (genuine_vs_ad)."
              ),
              (
                  "In evidence, cite POV, narrative structure, and delivery"
                  " cues (I/my story, you/the viewer, step-by-step teaching)."
              ),
              (
                  "Return detected=True if and only if narration or meaningful"
                  " speech is present and a narration style can be described."
              ),
              (
                  "Return detected=False if there is no speech/narration or"
                  " style cannot be judged."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="audio_type",
          name="Audio Type",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria=f"""
              Classify the primary audio format — what drives the sound track.
              {AUDIO_TYPE_INSTRUCTION}
          """,
          prompt_template="""
              What is the primary audio type of this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              AUDIO_TYPE_INSTRUCTION,
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "In evidence, note the dominant audio cues (music, narration,"
                  " on-camera speech, trending sound)."
              ),
              (
                  "Return detected=True if and only if a primary audio type is"
                  " clearly inferable."
              ),
              (
                  "Return detected=False if audio type cannot be assessed"
                  " (e.g. silent content with no audio cues)."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="music_dialogue_balance",
          name="Music–Dialogue Balance",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria=f"""
              When music and speech are both present, classify their relative
              balance in the mix. When only speech is present with little or no
              music, use dialogue_dominant.
              {MUSIC_DIALOGUE_BALANCE_INSTRUCTION}
          """,
          prompt_template="""
              How would you classify the music–dialogue balance in this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              MUSIC_DIALOGUE_BALANCE_INSTRUCTION,
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "In evidence, describe relative volume, masking, and whether"
                  " speech stays intelligible under the music."
              ),
              (
                  "Return detected=True if and only if speech is present and"
                  " balance can be classified."
              ),
              (
                  "Return detected=False if there is no speech or balance cannot"
                  " be assessed."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="speech_pace",
          name="Speech Pace",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria=f"""
              Classify how fast speech is delivered when speech is present.
              {SPEECH_PACE_INSTRUCTION}
          """,
          prompt_template="""
              What is the speech pace in this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              SPEECH_PACE_INSTRUCTION,
              (
                  "Always set 'value' to exactly one allowed label (lowercase):"
                  " fast, moderate, or slow."
              ),
              (
                  "In evidence, cite delivery speed cues (words per moment,"
                  " rushed vs deliberate pacing)."
              ),
              (
                  "Return detected=True if and only if speech is present and"
                  " pace can be assessed."
              ),
              (
                  "Return detected=False if there is no speech or pace cannot"
                  " be judged."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="speech_clarity",
          name="Speech Clarity",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria=f"""
              Classify how clear and intelligible speech is when speech is
              present (articulation and understandability, not pace).
              {SPEECH_CLARITY_INSTRUCTION}
          """,
          prompt_template="""
              How clear is the speech in this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              SPEECH_CLARITY_INSTRUCTION,
              (
                  "Assess clarity and diction only — not pace (speech_pace) or"
                  " music mix (music_dialogue_balance)."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase):"
                  " clear, accented_but_clear, or unclear."
              ),
              (
                  "In evidence, cite articulation, accent, mumbling, or overlap"
                  " issues."
              ),
              (
                  "Return detected=True if and only if value is 'clear' or"
                  " 'accented_but_clear'."
              ),
              (
                  "Return detected=False if value is 'unclear', there is no"
                  " speech, or clarity cannot be assessed."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="keyword_usage_seo_intent",
          name="Keyword Usage (SEO Intent)",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="DISCOVERY_SEO",
          evaluation_criteria="""
              The content intentionally uses specific keywords/phrases that suggest
              search intent or topical targeting (e.g. repeated key terms, explicit
              topic phrases, problem/solution wording).
          """,
          prompt_template="""
              Does this content intentionally use recognizable keywords/phrases that signal topical or search intent?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If True, list 3-8 representative keywords/phrases in evidence."
              ),
              (
                  "If detected=True, set the field 'value' to a comma-separated list"
                  " of 3-8 representative keywords/phrases."
              ),
              (
                  "Return True if and only if keyword usage appears intentional and"
                  " meaningfully tied to the topic."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="language_accent_detection",
          name="Language / Accent",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="LANGUAGE",
          evaluation_criteria=f"""
              Identify the primary spoken language, language mix, or notable
              accent/variety when speech is present.
              {LANGUAGE_ACCENT_GUIDANCE}
          """,
          prompt_template="""
              What is the primary spoken language, mix, or accent in this
              content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              LANGUAGE_ACCENT_GUIDANCE,
              (
                  "Use 'Hinglish' when Hindi and English are blended in speech;"
                  " use 'Multilingual' when multiple languages are used"
                  " substantially without one clear primary language."
              ),
              (
                  "For a single dominant language with regional accent, use"
                  " labels like 'English (Indian)' or 'Hindi' instead."
              ),
              (
                  "In evidence, cite spoken phrases or segments that support"
                  " the language/accent label."
              ),
              (
                  "Return detected=True if and only if speech is present and"
                  " primary language can be identified with reasonable"
                  " confidence."
              ),
              (
                  "Return detected=False if there is no speech or language"
                  " cannot be identified."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="secondary_language",
          name="Secondary Language",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="LANGUAGE",
          evaluation_criteria=f"""
              Detect whether a distinct secondary spoken language is used in
              addition to the primary language. Occasional loanwords or brand
              names do not count.
              {SECONDARY_LANGUAGE_GUIDANCE}
          """,
          prompt_template="""
              Is a secondary spoken language clearly used in this content in
              addition to the primary language?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              SECONDARY_LANGUAGE_GUIDANCE,
              (
                  "Compare against the primary language identified in"
                  " language_accent_detection when possible."
              ),
              (
                  "In evidence, cite segments where the secondary language is"
                  " spoken (not just on-screen text)."
              ),
              (
                  "Return detected=True if and only if a distinct secondary"
                  " language is clearly spoken."
              ),
              (
                  "Return detected=False if only one language is used or a"
                  " secondary language cannot be confirmed."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="content_buckets",
          name="Content Buckets",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="CONTENT_TAXONOMY",
          evaluation_criteria="""
              The content fits one or more recognizable content buckets used for
              social/influencer classification (e.g., tutorial/how-to, review/unboxing,
              lifestyle/vlog, GRWM, haul, testimonial, demo, entertainment/skit,
              behind-the-scenes, challenge, educational explainer, product showcase).
          """,
          prompt_template="""
              Can you assign this content to one or more clear content buckets?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to a comma-separated list"
                  " of bucket labels, with the best-fit bucket first."
              ),
              (
                  "Return True if and only if at least one content bucket clearly"
                  " applies based on what the video/image is doing."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="brand_visibility_in_content",
          name="Brand Visibility In Content",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="BRAND_INTEGRATION",
          evaluation_criteria=f"""
              Classify how visibly the brand or featured product appears in the
              content overall (visual and verbal cues combined). Use the brand
              name {{brand_name}} when known; otherwise assess the featured
              brand/product. {BRAND_VISIBILITY_IN_CONTENT_INSTRUCTION}
          """,
          prompt_template="""
              How visible is the brand {brand_name} or featured product in this
              content overall?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              BRAND_VISIBILITY_IN_CONTENT_INSTRUCTION,
              (
                  "Weigh logo/packaging on screen, product prominence, overlays,"
                  " and spoken brand mentions together for one overall level."
              ),
              (
                  "Always set 'value' to exactly one of:"
                  f" {', '.join(BRAND_VISIBILITY_IN_CONTENT_LEVELS)}."
              ),
              (
                  "Return detected=True if and only if value is Incidental,"
                  " Prominent, or Featured."
              ),
              (
                  "Return detected=False if and only if value is None."
              ),
              (
                  "Summarize visual and verbal evidence in evidence and rationale."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="product_screen_time",
          name="Product Screen Time",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="BRAND_INTEGRATION",
          evaluation_criteria="""
              The product/brand is visually present for a meaningful portion of the
              content (not just a brief flash). Use a best-effort estimate of duration
              or portion of the video.
          """,
          prompt_template="""
              Is the product/brand visually present for a meaningful amount of screen time (not just a brief flash)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If True, estimate the approximate screen time (e.g., seconds or"
                  " rough percentage) in evidence."
              ),
              (
                  "Return True if and only if product/brand visibility appears"
                  " meaningful (not incidental)."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="product_in_hand_seconds",
          name="Product In Hand (seconds)",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="BRAND_INTEGRATION",
          evaluation_criteria="""
              The product is physically held in hand (or clearly handled) by a person
              for a meaningful duration. Estimate approximate seconds and timestamps.
          """,
          prompt_template="""
              Is the product held in hand or clearly handled for a meaningful duration,
              and if so for approximately how many seconds?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to the estimated seconds"
                  " held in hand (e.g., '12' or '12s')."
              ),
              (
                  "In evidence, cite timestamps where the product is in hand and"
                  " explain your duration estimate."
              ),
              (
                  "Return True if and only if the product is held or handled in hand"
                  " for more than a brief incidental moment."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="integration_style",
          name="Integration Style",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="BRAND_INTEGRATION",
          evaluation_criteria="""
              The way the product is integrated can be categorized (e.g., demo,
              mention, lifestyle usage, tutorial integration, testimonial). If there
              is no brand/product integration, return False.
          """,
          prompt_template="""
              Is there clear product integration, and if so can you categorize the integration style (demo/mention/lifestyle/etc.)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to the primary integration"
                  " style label (e.g., 'demo', 'mention', 'lifestyle usage',"
                  " 'tutorial integration', 'testimonial')."
              ),
              (
                  "If True, name the primary integration style in evidence and briefly"
                  " justify it."
              ),
              (
                  "Return True if and only if a primary integration style is clearly"
                  " identifiable."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="cultural_relevance_local_global",
          name="Cultural Relevance (Local vs Global)",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="CULTURE",
          evaluation_criteria="""
              The content includes culturally specific references, context, language,
              or cues that make it clearly local/regional, or it is broadly global/
              culture-neutral. Return True if local/global orientation is identifiable.
          """,
          prompt_template="""
              Can you infer whether the content is culturally local/regional versus broadly global/culture-neutral?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If True, state 'local/regional' or 'global/culture-neutral' in"
                  " evidence, and cite 1-2 cues."
              ),
              (
                  "If detected=True, set the field 'value' to exactly one of:"
                  " 'local/regional' or 'global/culture-neutral'."
              ),
              (
                  "Return True if and only if the local-vs-global orientation is"
                  " clearly inferable from cues in the content."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="creator_archetype",
          name="Creator Archetype",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria="""
              The creator/presenter archetype is identifiable (e.g., influencer,
              expert/educator, entertainer, reviewer, storyteller, comedian).
              Return True if an archetype can be assigned with reasonable confidence.
          """,
          prompt_template="""
              Can you identify a clear creator/presenter archetype for this content (influencer, expert, entertainer, etc.)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If True, state the archetype in evidence and provide 1-2 reasons"
                  " based on observable behavior/content structure."
              ),
              (
                  "If detected=True, set the field 'value' to the archetype label"
                  " (e.g., 'influencer', 'expert/educator', 'entertainer', 'reviewer')."
              ),
              (
                  "Return True if and only if one archetype is clearly the best fit."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="communication_style",
          name="Communication Style",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="COMMUNICATION",
          evaluation_criteria=f"""
              Classify the primary way the content communicates its message
              through speech, on-screen text, and presenter delivery.
              {COMMUNICATION_STYLE_INSTRUCTION}
          """,
          prompt_template="""
              What is the primary communication style of this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              COMMUNICATION_STYLE_INSTRUCTION,
              (
                  "Pick the single best-fit label based on how the message is"
                  " delivered, not creator role (creator_archetype) or emotional"
                  " mood alone (emotional_tone)."
              ),
              (
                  "educational vs demonstrative: explaining/teaching vs showing"
                  " hands-on use step by step."
              ),
              (
                  "storytelling vs conversational: narrative arc vs casual chat"
                  " without a clear story structure."
              ),
              (
                  "humorous vs promotional: comedy drives delivery vs selling or"
                  " CTA-forward pitch."
              ),
              (
                  "direct vs conversational: blunt, no-nonsense clarity vs relaxed"
                  " peer-to-peer tone."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "Return detected=True if and only if a primary communication"
                  " style is clearly inferable from speech, text, or deliberate"
                  " presenter delivery."
              ),
              (
                  "Return detected=False if there is no meaningful communication"
                  " (e.g. music-only montage with no message channel)."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="cta_type",
          name="Call-to-Action Type",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="CTA",
          evaluation_criteria=f"""
              Classify the primary call-to-action (CTA) that asks the viewer to
              take a specific action, in spoken words or on-screen text.
              {CTA_TYPE_INSTRUCTION}
          """,
          prompt_template="""
              What is the primary call-to-action type in this content (speech
              or on-screen text)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              CTA_TYPE_INSTRUCTION,
              (
                  "Consider both spoken CTAs and on-screen text CTAs. Examples"
                  " of common CTA phrases include: {call_to_actions}."
              ),
              (
                  "If multiple CTAs appear, pick the dominant primary ask"
                  " (usually the closing or strongest conversion ask)."
              ),
              (
                  "purchase_prompt vs learn_more: explicit buy/shop/order/code"
                  " vs softer check-it-out or learn-more without purchase."
              ),
              (
                  "comment_prompt vs dm_prompt: public comment keyword vs private"
                  " message/DM request."
              ),
              (
                  "Always set 'value' to exactly one allowed label (lowercase)."
              ),
              (
                  "Return detected=True if and only if a clear primary CTA is"
                  " present in speech or on-screen text."
              ),
              (
                  "Return detected=False if there is no explicit viewer action"
                  " requested."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="genuine_vs_ad",
          name="Genuine Content (Not Advertisement)",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TRUST",
          evaluation_criteria="""
              The content feels organic and genuine rather than a scripted
              advertisement. It does not feel like overt promotional messaging
              with heavy branding, scripted selling, or polished ad framing.
          """,
          prompt_template="""
              Does this content feel genuine and organic, rather than like a
              scripted advertisement?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess whether the creator delivery and framing feel natural"
                  " (UGC/real moment/personal voice) versus polished (promotional,"
                  " scripted, produced commercial intent)."
              ),
              (
                  "Always set 'value' to exactly one of: 'natural' or 'polished'"
                  " — for both detected=True and detected=False responses."
              ),
              (
                  "Use 'natural' for organic creator voice, conversational delivery,"
                  " and content that does not feel like a scripted advertisement."
              ),
              (
                  "Use 'polished' for rehearsed scripts, studio/commercial production,"
                  " overt promotional selling, or ad-like framing."
              ),
              (
                  "Return detected=True if and only if value is 'natural'."
              ),
              (
                  "Return detected=False if value is 'polished'."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_hashtag_strategy",
          name="Hashtag Strategy",
          category=VideoFeatureCategory.CONTENT_INTELLIGENCE,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="DISCOVERY_SEO",
          evaluation_criteria="""
              Hashtags are used deliberately and relevantly, with a sensible
              mix of topical/niche, branded, and/or trending hashtags rather
              than random keyword stuffing.
          """,
          prompt_template="""
              Is hashtag usage in this content deliberate and relevant to the
              topic/audience?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If hashtags are present, list examples and classify them as"
                  " branded, topical/niche, or trending/general in evidence."
              ),
              (
                  "If detected=True, set the field 'value' to a short label like"
                  " 'strategic', 'mixed', or 'spammy/low-signal'."
              ),
              (
                  "Return True if and only if hashtag usage appears intentional"
                  " and contextually relevant."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
  ]


def get_content_quality_feature_configs() -> list[VideoFeature]:
  """Backward-compatible alias for legacy imports."""
  return get_content_intelligence_feature_configs()
