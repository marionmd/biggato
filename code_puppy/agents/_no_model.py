"""The error raised when no model is configured at all."""

from code_puppy.i18n import t


class NoModelConfiguredError(ValueError):
    """Raised by ``load_model_with_fallback`` when there are no models at all.

    Not a crash: the user just hasn't run ``/add_model`` yet. The startup
    "No model is configured" warning already explains that, so model loading
    stays silent and the REPL shows only this one-line message.
    """

    def __init__(self) -> None:
        super().__init__(t("cli.error.no_model"))
