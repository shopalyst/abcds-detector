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


def get_content_intelligence_feature_configs() -> list[VideoFeature]:
  """Gets all content intelligence and safety feature configurations."""
  return [
      # ------------------------------------------------------------------ #
      # Group 1 – Quality & Clarity                                         #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="content_clarity_focus",
          name="Content Clarity & Focus",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="narrative_structure",
          name="Narrative Structure",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="informational_depth",
          name="Informational Depth",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="production_quality",
          name="Acceptable Production Quality",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="audience_relevance",
          name="Audience Relevance",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="engagement_potential",
          name="Engagement Potential",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="low_effort_spam",
          name="Not Low-Effort / Spam",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      # ------------------------------------------------------------------ #
      # Group 3 – Authenticity & Trust                                      #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="authenticity_trustworthiness",
          name="Authenticity & Trustworthiness",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TRUST",
          evaluation_criteria="""
              The content appears honest, genuine, and grounded. The creator
              seems authentic and not putting on an exaggerated or deceptive
              persona. The content does not use manipulative tactics, false
              urgency, or deceptive framing to influence the viewer.
          """,
          prompt_template="""
              Does this content feel authentic and trustworthy — honest,
              genuine, and not deceptive or manipulative?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "Assess whether the creator appears genuine, whether the"
                  " claims feel honest, and whether any persuasion tactics"
                  " feel transparent rather than manipulative."
              ),
              (
                  "Return True if and only if the content feels authentic,"
                  " trustworthy, and non-deceptive."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="clickbait_detection",
          name="Clickbait Detection",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      # ------------------------------------------------------------------ #
      # Group 4 – Safety & Appropriateness                                  #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="negativity_hate_speech",
          name="Negativity / Hate Speech",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="brand_safety",
          name="Brand Safety Risk",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="audience_appropriateness",
          name="Audience Appropriateness",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="cultural_sensitivity",
          name="Cultural Sensitivity",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      # ------------------------------------------------------------------ #
      # Group 5 – Content Diagnostics (LLM-only, boolean + evidence)         #
      # ------------------------------------------------------------------ #
      VideoFeature(
          id="genre_of_content",
          name="Genre of Content",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria="""
              The content fits a clear, recognizable genre (e.g., tutorial/how-to,
              review, entertainment/skit, vlog, news/commentary, testimonial, demo,
              narrative/story, challenge, educational explainer).
          """,
          prompt_template="""
              Does this content fit a clear, recognizable genre?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to the primary genre label"
                  " (e.g., 'tutorial/how-to', 'review', 'vlog', 'skit', 'demo')."
              ),
              (
                  "If True, explicitly name the primary genre and (optionally) a"
                  " secondary genre in the evidence."
              ),
              (
                  "Return True if and only if you can identify a clear primary"
                  " genre based on what the content is doing."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria="""
              The content communicates a clear emotional tone (e.g. funny, serious,
              inspirational, aggressive, empathetic, urgent, calm) that is consistent
              for most of the content.
          """,
          prompt_template="""
              Is there a clear and mostly consistent emotional tone to this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to the primary tone label"
                  " (e.g., 'funny', 'serious', 'inspirational', 'aggressive')."
              ),
              (
                  "If True, state the primary tone (and any notable tone shifts)"
                  " in the evidence."
              ),
              (
                  "Return True if and only if the tone is clearly inferable from"
                  " delivery, visuals, and audio."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria="""
              The audio is clear and intelligible: speech (if present) can be heard,
              volume is consistent, and noise/distortion does not hinder understanding.
          """,
          prompt_template="""
              Is the audio quality clear enough that the content is easy to understand?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If False, cite specific problems (e.g., clipping, muffled audio,"
                  " loud background noise, inconsistent volume)."
              ),
              "Return True if and only if audio quality is clear and intelligible.",
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="video_quality",
          name="Video Quality",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria="""
              The visuals are clear enough to comfortably watch: the video is not
              excessively blurry, pixelated, poorly framed, or distracting due to
              severe shake.
          """,
          prompt_template="""
              Is the video quality visually clear and comfortable to watch?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If False, cite the dominant issue (blur, shake, bad framing,"
                  " low resolution, compression artifacts)."
              ),
              "Return True if and only if the visuals are clear and watchable.",
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="lighting_quality",
          name="Lighting Quality",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria="""
              Lighting supports viewing: subject(s) are visible, exposure is not
              consistently too dark/bright, and key details are not lost due to
              harsh glare or severe backlighting.
          """,
          prompt_template="""
              Is the lighting generally good enough to clearly see the main subject(s)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If False, describe the primary lighting issue (too dark, blown"
                  " highlights, strong backlight, flicker, uneven lighting)."
              ),
              "Return True if and only if lighting is generally sufficient and clear.",
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="camera_movement",
          name="Camera Movement",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria="""
              The video uses noticeable camera movement (e.g., handheld motion, pans,
              tilts, zooms, tracking shots) that is intentional and does not harm
              comprehension.
          """,
          prompt_template="""
              Is there noticeable, intentional camera movement in this content?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "In evidence, describe the dominant movement style (handheld,"
                  " stabilized pan/tilt, zoom, tracking)."
              ),
              (
                  "Return True if and only if camera movement is clearly present"
                  " and appears intentional."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria="""
              The content demonstrates a discernible editing style (e.g., jump cuts,
              fast cuts, montage, minimal edits, heavy effects/filters, text-led
              editing) that is consistent enough to describe.
          """,
          prompt_template="""
              Does this content have a clear, describable editing style?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to a short editing-style"
                  " label (e.g., 'jump cuts', 'fast-cut montage', 'minimal edits',"
                  " 'effects-heavy', 'text-led')."
              ),
              (
                  "If True, name the editing style in evidence and cite 1-2 concrete"
                  " markers (e.g., frequent jump cuts, on-beat cuts, overlay-heavy)."
              ),
              (
                  "Return True if and only if you can clearly describe the editing"
                  " style using observable cues."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          id="audio_type",
          name="Audio Type",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria="""
              The primary audio format can be identified as one of: voice-over,
              dialogue/on-camera speech, music-first/trending sound, or mixed.
          """,
          prompt_template="""
              Can you identify the primary audio type (voice-over, dialogue, music/trending sound, or mixed)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to one of:"
                  " 'voice-over', 'dialogue', 'music-first/trending sound', or 'mixed'."
              ),
              (
                  "If True, state the primary audio type in evidence and note any"
                  " significant secondary type."
              ),
              (
                  "Return True if and only if one primary audio type is clearly"
                  " dominant."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria="""
              When both music and speech are present, the mix supports understanding:
              dialogue is not consistently overpowered by music and remains intelligible.
          """,
          prompt_template="""
              When music and speech are both present, is the dialogue still clearly intelligible (not overpowered)?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If False, describe whether music is overpowering, the mix is"
                  " inconsistent, or speech is drowned out."
              ),
              (
                  "Return True if and only if speech remains consistently intelligible"
                  " when music is present."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="speech_pace_clarity",
          name="Speech Pace & Clarity",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="TECHNICAL_QUALITY",
          evaluation_criteria="""
              Speech (if present) is delivered at a pace and with clarity that is
              easy to follow, without being consistently too fast, mumbled, or
              unclear for typical viewers.
          """,
          prompt_template="""
              If speech is present, is it delivered at a clear pace that is easy to follow?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If False, specify the issue: too fast, unclear articulation,"
                  " heavy overlap, or unclear diction."
              ),
              (
                  "Return True if and only if speech delivery is generally clear and"
                  " easy to follow."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          id="narration_style_scripted_vs_organic",
          name="Narration Style (Scripted vs Organic)",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="STYLE_CLASSIFICATION",
          evaluation_criteria="""
              If narration/speech is present, the delivery style can be characterized
              as mostly scripted (polished, rehearsed, structured) or organic
              (conversational, spontaneous, imperfect).
          """,
          prompt_template="""
              If narration/speech is present, can its style be characterized as mostly scripted or mostly organic?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If detected=True, set the field 'value' to either 'scripted' or"
                  " 'organic'."
              ),
              (
                  "If True, state the dominant style (scripted vs organic) in evidence"
                  " and mention 1-2 markers that led you there."
              ),
              (
                  "Return True if and only if one dominant narration style is clearly"
                  " inferable."
              ),
          ],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="language_accent_detection",
          name="Language / Accent Detection",
          category=VideoFeatureCategory.CONTENT_QUALITY,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          feature_group="LANGUAGE",
          evaluation_criteria="""
              The spoken language and notable accent/variety (if any) can be identified
              (e.g., English with regional accent, Spanish, Hindi, etc.). If there is
              no speech, return False.
          """,
          prompt_template="""
              Is there speech, and if so, can you identify the language and any notable accent/variety?
          """,
          extra_instructions=[
              "Consider the following criteria for your answer: {criteria}.",
              (
                  "If True, state the language and any notable accent/variety in evidence."
              ),
              (
                  "If detected=True, set the field 'value' to the best label you can,"
                  " e.g. 'Hindi', 'English (Indian)', 'Spanish (LatAm)'."
              ),
              (
                  "Return True if and only if speech is present AND language is"
                  " identifiable with reasonable confidence."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          id="integration_style",
          name="Integration Style",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
          id="genuine_vs_ad",
          name="Genuine Content (Not Advertisement)",
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
                  "Assess whether the creator delivery and framing feel authentic"
                  " (UGC/real moment/personal voice) versus ad-like (promotional,"
                  " scripted, polished commercial intent)."
              ),
              (
                  "If detected=True, set the field 'value' to one of:"
                  " 'genuine/organic' or 'ad-like/scripted'."
              ),
              (
                  "Return True if and only if the content feels genuinely organic"
                  " and not scripted as an advertisement."
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
          category=VideoFeatureCategory.CONTENT_QUALITY,
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
