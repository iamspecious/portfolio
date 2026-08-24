"""
Environment configuration and the sandbox/production switch.

Every credential and endpoint the receiver needs comes from the environment,
never a hardcoded value. See .env.example at the project root for the full
list with descriptions.

The switch that matters most: REMOTE_ENV. Get it wrong and you're either
testing against nothing (fine) or writing to a real company's payroll data
(not fine). It defaults to "sandbox" specifically so that forgetting to set
it fails safe.
"""

import os


class ConfigError(Exception):
    pass


def _env(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        raise ConfigError(f"Required environment variable {name} is not set.")
    return val


class Config:
    def __init__(self):
        # ---- Remote (the one live integration) ----
        self.remote_env = _env("REMOTE_ENV", "sandbox")
        if self.remote_env not in ("sandbox", "production"):
            raise ConfigError(
                f"REMOTE_ENV must be 'sandbox' or 'production', got {self.remote_env!r}."
            )
        self.remote_base_url = (
            "https://gateway.remote-sandbox.com"
            if self.remote_env == "sandbox"
            else "https://gateway.remote.com"
        )
        self.remote_client_id = _env("REMOTE_CLIENT_ID")
        self.remote_client_secret = _env("REMOTE_CLIENT_SECRET")
        self.remote_webhook_secret = _env("REMOTE_WEBHOOK_SECRET")

        # ---- Ashby (simulated — see RESEARCH.md) ----
        self.ashby_api_key = _env("ASHBY_API_KEY")
        self.ashby_webhook_secret = _env("ASHBY_WEBHOOK_SECRET")

        # ---- HiBob (simulated — see RESEARCH.md) ----
        self.hibob_service_user_id = _env("HIBOB_SERVICE_USER_ID")
        self.hibob_service_user_token = _env("HIBOB_SERVICE_USER_TOKEN")
        self.hibob_webhook_secret = _env("HIBOB_WEBHOOK_SECRET")

        # ---- Receiver ----
        self.receiver_host = _env("RECEIVER_HOST", "0.0.0.0")
        self.receiver_port = int(_env("RECEIVER_PORT", "8787"))
        self.db_path = _env("DB_PATH", "hr_integration.sqlite3")

        # ---- Flow behaviour ----
        # Dry-run is on by default on purpose — see DEVLOG.md. Only an
        # explicit "false" turns it off; any typo or unset value stays safe.
        self.dry_run = _env("DRY_RUN", "true").strip().lower() != "false"

    def require_remote_credentials(self):
        if not (self.remote_client_id and self.remote_client_secret):
            raise ConfigError(
                "REMOTE_CLIENT_ID / REMOTE_CLIENT_SECRET are not set — "
                "no live Remote sandbox call is possible without them."
            )

    def is_production(self):
        return self.remote_env == "production"


def load_config():
    return Config()
