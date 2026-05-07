import sys
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QInputDialog, QLineEdit, QMessageBox

from controllers.login_controller import LoginController
from db import ensure_db_setup


BASE_DIR = Path(__file__).resolve().parent


def load_stylesheet(app: QApplication) -> None:
    qss_path = BASE_DIR / "ui" / "cyberpunk.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))


def main() -> int:

    # Create the QApplication early so we can show dialogs if needed.
    app = QApplication(sys.argv)
    app.setApplicationName("Student Performance Analyzer")
    app.setQuitOnLastWindowClosed(True)

    # If the database already exists and is accessible, skip asking for a password
    from db import db_exists

    env_pwd = os.getenv("SPA_DB_PASSWORD")
    if db_exists(env_pwd):
        # DB present, continue without prompting
        load_stylesheet(app)
    else:
        # Prompt the user for MySQL root password via GUI so windowed exe users
        # can provide credentials; set env var for the rest of the startup.
        pwd, ok = QInputDialog.getText(None, "MySQL Password",
                                       "Enter MySQL root password to initialize the database:",
                                       QLineEdit.EchoMode.Password)
        if not (ok and pwd):
            QMessageBox.critical(None, "Database Setup Aborted",
                                 "No MySQL password provided. Set SPA_DB_PASSWORD or run the app from a console.")
            return 1
        os.environ["SPA_DB_PASSWORD"] = pwd

        try:
            ensure_db_setup()
        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Error during DB setup: {e}")
            return 1
        load_stylesheet(app)

    login = LoginController()
    login.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
