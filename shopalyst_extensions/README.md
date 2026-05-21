# Shopalyst fork extensions

Shopalyst-only behavior lives here so merges with upstream `abcds-detector` `main` touch fewer shared files.

## Upstream hooks (keep small when merging)

| Shared file | Hook ||
|-------------|------|
| `main.py` | Calls `shopalyst_extensions.pipeline` for content eval / export |
| `utils.py` | Calls `shopalyst_extensions.cli` for `-rcq`, `-bcp`, brand rules |
| `features_repository/feature_configs_handler.py` | Delegates content category + grouping |
| `evaluation_services/video_evaluation_service.py` | Delegates feature filter + sort |
| `models.py`, `configuration.py` | `run_content_quality`, `content_quality_evaluated_features` |

## This package

| Module | Responsibility |
|--------|----------------|
| `cli.py` | Presets, `-rcq` / `-bcp`, brand metadata validation |
| `pipeline.py` | Run content pass, print, persist JSON/BQ |
| `assessment.py` | Risk-aware scoring, JSON export, BQ rows for content |
| `evaluation.py` | `features_to_evaluate` filter, sort order |
| `feature_grouping.py` | LLM batching by `feature_group` |
| `feature_registry.py` | Loads `content_intelligence_features.py` |

Feature definitions remain in `features_repository/content_intelligence_features.py`.
