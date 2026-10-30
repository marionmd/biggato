"""First run with no models configured: one clear message, no repeated noise.

With an empty model list, every agent build (the main agent plus the
context-window tool probe, which retries on each status refresh) used to warn
``Model '' not found`` and print "No valid model could be loaded" again, and a
typed prompt ended in a full traceback.
"""

from unittest.mock import patch

import pytest

from code_puppy.agents._builder import (
    load_model_with_fallback,
    reset_model_fallback_warnings,
)
from code_puppy.agents._no_model import NoModelConfiguredError
from code_puppy.cli_runner import _render_turn_exception
from code_puppy.i18n import t


@pytest.fixture(autouse=True)
def _clean_fallback_warning_state():
    reset_model_fallback_warnings()
    yield
    reset_model_fallback_warnings()


def _fake_get_model(model_name, config):
    if model_name not in config:
        raise ValueError(f"Model '{model_name}' not found in configuration.")
    # Configured but unusable, e.g. a missing API key.
    raise ValueError(f"Model '{model_name}' could not be instantiated.")


def _load(models_config, requested="dead-model"):
    with (
        patch(
            "code_puppy.agents._builder.ModelFactory.get_model",
            side_effect=_fake_get_model,
        ),
        patch("code_puppy.agents._builder.get_global_model_name", return_value=None),
        patch("code_puppy.agents._builder.emit_info"),
        patch("code_puppy.agents._builder.emit_warning") as mock_warning,
        patch("code_puppy.agents._builder.emit_error") as mock_error,
    ):
        with pytest.raises(ValueError) as excinfo:
            load_model_with_fallback(
                requested, models_config, "group-id", agent_name="code-puppy"
            )
    return excinfo.value, mock_warning, mock_error


@pytest.mark.parametrize("requested", ["", None])
def test_empty_model_list_raises_quietly(requested):
    exc, mock_warning, mock_error = _load({}, requested=requested)

    assert isinstance(exc, NoModelConfiguredError)
    assert str(exc) == t("cli.error.no_model")
    mock_warning.assert_not_called()
    mock_error.assert_not_called()


def test_no_model_error_is_still_a_value_error():
    # Existing callers catch ValueError around model loading.
    assert issubclass(NoModelConfiguredError, ValueError)


def test_unloadable_models_error_once_per_combo():
    broken = {"broken-model": {}}

    first, _warning, first_error = _load(broken)
    second, _warning, second_error = _load(broken)

    assert not isinstance(first, NoModelConfiguredError)
    assert first_error.call_count == 1
    second_error.assert_not_called()
    assert "config set" not in str(second)
    assert "/add_model" in str(second)


def test_turn_without_model_renders_one_line():
    with (
        patch("code_puppy.messaging.emit_warning") as mock_warning,
        patch("code_puppy.messaging.emit_error") as mock_error,
        patch("code_puppy.error_logging.log_error") as mock_log,
    ):
        _render_turn_exception(NoModelConfiguredError())

    mock_warning.assert_called_once_with(t("cli.error.no_model"))
    mock_error.assert_not_called()
    mock_log.assert_not_called()
