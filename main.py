import sys
import os
from PyQt6.QtWidgets import QApplication, QInputDialog, QLineEdit, QMessageBox

from app_paths import resource_path
from controllers.login_controller import LoginController
from db import ensure_db_setup, remove_demo_seed_data


def load_stylesheet(app: QApplication) -> None:
    qss_path = resource_path("ui", "cyberpunk.qss")
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))


def ensure_database_ready() -> tuple[bool, str | None]:
    """
    Make sure the MySQL database exists before showing login.
    Returns (success, error_message).
    """
    from db import db_exists

    env_pwd = os.getenv("SPA_DB_PASSWORD")
    if db_exists(env_pwd):
        return True, None

    pwd, ok = QInputDialog.getText(
        None,
        "MySQL Password",
        "Enter MySQL root password to initialize the database:",
        QLineEdit.EchoMode.Password,
    )
    if not (ok and pwd):
        return False, "No MySQL password provided. Set SPA_DB_PASSWORD or try again."

    os.environ["SPA_DB_PASSWORD"] = pwd
    try:
        ensure_db_setup()
    except Exception as exc:
        return False, f"Error during DB setup: {exc}"

    if not db_exists(pwd):
        return False, "Database setup did not complete successfully."

    return True, None


def main() -> int:

    # Create the QApplication early so we can show dialogs if needed.
    app = QApplication(sys.argv)
    app.setApplicationName("Student Performance Analyzer")
    app.setQuitOnLastWindowClosed(True)

    is_ready, error_message = ensure_database_ready()
    if not is_ready:
        QMessageBox.critical(None, "Database Setup Aborted", error_message or "Unknown database setup error.")
        return 1

    try:
        remove_demo_seed_data()
    except Exception as e:
        QMessageBox.critical(None, "Database Error", f"Error cleaning demo data: {e}")
        return 1
    load_stylesheet(app)

    login = LoginController()
    login.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
