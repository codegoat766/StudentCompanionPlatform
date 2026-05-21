import csv
import hashlib
import os
import sys
from pathlib import Path

import mysql.connector
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("SPA_DB_PASSWORD"),
    "database": "spa_db",
}


QSS = """
* {
    font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
    color: #111827;
}

QMainWindow, QWidget {
    background-color: #FAFAFA;
}

QFrame {
    background-color: #FFFFFF;
    border: 2px solid #111827;
    border-radius: 12px;
}

QFrame#headerFrame {
    background-color: #FFE4B5;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
    border-radius: 16px;
    min-height: 54px;
}

QFrame#leftPanel {
    background-color: #E0E7FF;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
    border-radius: 16px;
}

QFrame#rightPanel, QFrame#profileFrame {
    background-color: #FFFFFF;
    border: 2px solid #111827;
    border-radius: 12px;
    padding: 12px;
}

QFrame#commandFrame, QFrame#loginPanel {
    background-color: #FEF3C7;
    border: 2px solid #111827;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
    border-radius: 16px;
}

QFrame#navDivider {
    background-color: #111827;
    min-height: 2px;
    max-height: 2px;
    border: none;
    margin: 4px 0;
}

QLabel#appTitle {
    font-size: 18px;
    font-weight: 800;
    color: #111827;
    background: transparent;
    border: none;
}

QLabel#profileTitle {
    font-size: 16px;
    font-weight: 800;
    color: #FF6B4A;
}

QLabel#gpaLabel {
    font-size: 20px;
    font-weight: 800;
    color: #FF6B4A;
    padding: 10px 0px;
}

QLabel {
    background: transparent;
    border: none;
    font-weight: 600;
    color: #111827;
}

QLineEdit, QComboBox {
    background: #FFFFFF;
    border: 2px solid #111827;
    border-radius: 8px;
    padding: 10px 14px;
    color: #111827;
    font-weight: 600;
    selection-background-color: #FF6B4A;
    selection-color: #FFFFFF;
}

QLineEdit:focus, QComboBox:focus {
    background: #FEF3C7;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
}

QTextEdit {
    background: #111827;
    border: 2px solid #111827;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
    border-radius: 12px;
    padding: 12px;
    color: #4ADE80;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    font-weight: 600;
}

QPushButton {
    background-color: #FF6B4A;
    color: #FFFFFF;
    border: 2px solid #111827;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 800;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #E05A3A;
    margin-top: 1px;
    margin-left: 1px;
    border-bottom: 3px solid #111827;
    border-right: 3px solid #111827;
}

QPushButton:pressed {
    background-color: #C0482B;
    margin-top: 2px;
    margin-left: 2px;
    border-bottom: 2px solid #111827;
    border-right: 2px solid #111827;
}

QPushButton#secondary_btn, QPushButton#refreshButton, QPushButton#exportButton {
    background: #FFFFFF;
    color: #111827;
}

QPushButton#secondary_btn:hover, QPushButton#refreshButton:hover, QPushButton#exportButton:hover {
    background-color: #F3F4F6;
}

QPushButton#logoutButton {
    background-color: #111827;
    color: #FFFFFF;
    border-bottom: 4px solid #374151;
    border-right: 4px solid #374151;
}

QPushButton#logoutButton:hover {
    background-color: #374151;
    border-bottom: 3px solid #111827;
    border-right: 3px solid #111827;
}

QListWidget#navSidebar {
    background: transparent;
    border: none;
    padding: 4px;
    outline: none;
}

QListWidget#navSidebar::item {
    background-color: #FFFFFF;
    border: 2px solid #111827;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    color: #111827;
    font-weight: 800;
}

QListWidget#navSidebar::item:selected {
    background-color: #FF6B4A;
    color: #FFFFFF;
    margin-top: 2px;
    margin-left: 2px;
    border-bottom: 2px solid #111827;
    border-right: 2px solid #111827;
}

QListWidget#navSidebar::item:hover:!selected {
    background-color: #FEF3C7;
}

QListWidget {
    background: #FFFFFF;
    border: 2px solid #111827;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: #FEF3C7;
    selection-color: #111827;
    font-weight: 600;
}

QListWidget::item {
    padding: 10px 12px;
    border-bottom: 1px solid #E5E7EB;
}

QTableWidget {
    background: #FFFFFF;
    border: 2px solid #111827;
    border-bottom: 4px solid #111827;
    border-right: 4px solid #111827;
    border-radius: 12px;
    gridline-color: #E5E7EB;
    alternate-background-color: #FAFAFA;
    selection-background-color: #FEF3C7;
    selection-color: #111827;
    font-weight: 600;
}

QTableWidget::item {
    padding: 8px 10px;
    border: none;
}

QHeaderView::section {
    background-color: #FEF3C7;
    border: none;
    border-bottom: 2px solid #111827;
    border-right: 2px solid #111827;
    padding: 10px 12px;
    font-weight: 800;
    color: #111827;
}

QScrollBar:vertical {
    background: transparent;
    width: 12px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #111827;
    min-height: 30px;
    border-radius: 6px;
    border: 2px solid #FAFAFA;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; border: none; }

QScrollBar:horizontal {
    background: transparent;
    height: 12px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #111827;
    min-width: 30px;
    border-radius: 6px;
    border: 2px solid #FAFAFA;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; border: none; }
"""


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def log_audit(user_id, action: str, details: str = "") -> None:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO audit_log(user_id, action, details) VALUES (%s, %s, %s)", (user_id, action, details))
        conn.commit()
        conn.close()
    except Exception:
        pass


def authenticate(identifier: str, password: str) -> dict | None:
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password_hash=%s AND is_active=TRUE",
            (identifier, hash_password(password)),
        )
        user = cur.fetchone()
        if not user:
            cur.execute(
                """
                SELECT u.*
                FROM users u
                JOIN students s ON s.user_id = u.id
                WHERE s.prn=%s AND u.password_hash=%s AND u.is_active=TRUE
                """,
                (identifier, hash_password(password)),
            )
            user = cur.fetchone()

        if not user:
            log_audit(None, "LOGIN_FAILED", f"identifier={identifier}")
            return None

        cur.execute("SELECT id FROM students WHERE user_id=%s", (user["id"],))
        student = cur.fetchone()
        user["student_id"] = student["id"] if student else None
        log_audit(user["id"], "LOGIN_SUCCESS", f"identifier={identifier} role={user['role']}")
        return user
    finally:
        conn.close()


def fetch_all(query: str, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        conn.close()


def execute(query: str, params=()) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def subjects() -> list[str]:
    return [row[0] for row in fetch_all("SELECT name FROM subjects ORDER BY name")]


class BaseWindow(QMainWindow):
    def panel(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        return frame, layout

    def log(self, text: str) -> None:
        self.terminal.append(f"> {text}")


class DonutChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.colors = [QColor("#4ADE80"), QColor("#60A5FA"), QColor("#FBBF24"), QColor("#F87171"), QColor("#9CA3AF")]
        self.labels = ["A", "B", "C", "D", "F"]
        self.setMinimumSize(250, 250)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.data or sum(self.data) == 0:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("Inter", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Data Available")
            return
        total = sum(self.data)
        width, height = self.width(), self.height()
        size = min(width, height) - 40
        rect = QRectF((width - size) / 2, (height - size) / 2, size, size)
        start_angle = 90 * 16
        for i, value in enumerate(self.data):
            if value == 0: continue
            span_angle = -int((value / total) * 360 * 16)
            painter.setBrush(QBrush(self.colors[i]))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, start_angle, span_angle)
            start_angle += span_angle
        inner_size = size * 0.65
        inner_rect = QRectF((width - inner_size) / 2, (height - inner_size) / 2, inner_size, inner_size)
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(inner_rect)
        painter.setPen(QColor("#111827"))
        painter.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        painter.drawText(inner_rect, Qt.AlignmentFlag.AlignCenter, str(total))
        painter.setFont(QFont("Inter", 10))
        painter.setPen(QColor("#6B7280"))
        painter.drawText(inner_rect.adjusted(0, 25, 0, 0), Qt.AlignmentFlag.AlignCenter, "Students")
        legend_y, legend_x = height - 20, (width - (len(self.data) * 40)) / 2
        painter.setFont(QFont("Inter", 10, QFont.Weight.Bold))
        for i, value in enumerate(self.data):
            if value > 0:
                painter.setBrush(QBrush(self.colors[i]))
                painter.drawEllipse(int(legend_x), int(legend_y), 10, 10)
                painter.setPen(QColor("#111827"))
                painter.drawText(int(legend_x + 15), int(legend_y + 10), self.labels[i])
                legend_x += 40

class BarChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.setMinimumSize(300, 250)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.data:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("Inter", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Data Available")
            return
        width, height = self.width(), self.height()
        margin_left, margin_right, margin_top, margin_bottom = 40, 20, 30, 60
        chart_width, chart_height = width - margin_left - margin_right, height - margin_top - margin_bottom
        painter.setPen(QPen(QColor("#E5E7EB"), 1, Qt.PenStyle.DashLine))
        for i in range(5):
            y = margin_top + chart_height - (i * chart_height / 4)
            painter.drawLine(margin_left, int(y), width - margin_right, int(y))
            painter.setPen(QColor("#6B7280"))
            painter.setFont(QFont("Inter", 9))
            painter.drawText(0, int(y - 10), margin_left - 10, 20, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, str(i * 25))
            painter.setPen(QPen(QColor("#E5E7EB"), 1, Qt.PenStyle.DashLine))
        num_bars = len(self.data)
        bar_width = min(40, chart_width / (num_bars * 1.5))
        spacing = (chart_width - (num_bars * bar_width)) / (num_bars + 1)
        painter.setFont(QFont("Inter", 9))
        for i, (subject, marks) in enumerate(self.data):
            x = margin_left + spacing + i * (bar_width + spacing)
            bar_height = (marks / 100.0) * chart_height
            y = margin_top + chart_height - bar_height
            if marks >= 90: color = QColor("#4ADE80")
            elif marks >= 75: color = QColor("#60A5FA")
            elif marks >= 60: color = QColor("#FBBF24")
            elif marks >= 40: color = QColor("#F97316")
            else: color = QColor("#F87171")
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_width, bar_height), 4, 4)
            if bar_height > 4: painter.drawRect(QRectF(x, y + 4, bar_width, bar_height - 4))
            painter.setPen(QColor("#111827"))
            painter.drawText(int(x), int(y - 20), int(bar_width), 20, Qt.AlignmentFlag.AlignCenter, f"{marks:g}")
            painter.setPen(QColor("#4B5563"))
            display_name = subject[:6] + ".." if len(subject) > 8 else subject
            painter.drawText(int(x - 10), int(margin_top + chart_height + 5), int(bar_width + 20), 30, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.TextWordWrap, display_name)


class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.dashboard = None
        self.setWindowTitle("SPA - Login")
        self.setFixedSize(520, 620)
        root = QWidget()
        root.setStyleSheet("background-color: #FAFAFA;")
        main_layout = QVBoxLayout(root)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(root)

        card = QFrame()
        card.setObjectName("loginPanel")
        card.setFixedWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(24)

        app_name = QLabel("Welcome to SPA")
        app_name.setStyleSheet("font-size: 24px; font-weight: 800; color: #111827;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(app_name)

        subtitle = QLabel("Please enter your details to sign in.")
        subtitle.setStyleSheet("font-size: 14px; color: #64748B; font-weight: 600;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(12)

        self.ident_input = QLineEdit()
        self.ident_input.setPlaceholderText("Username / PRN")
        card_layout.addWidget(self.ident_input)

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.pwd_input)

        card_layout.addSpacing(20)

        self.login_btn = QPushButton("Sign In")
        self.login_btn.setMinimumHeight(46)
        self.login_btn.clicked.connect(self.login)
        card_layout.addWidget(self.login_btn)

        self.status = QLabel("")
        self.status.setStyleSheet("color: #EF4444; font-weight: 600; font-size: 12px;")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.status)

        main_layout.addWidget(card)

        # Hidden terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setVisible(False)
        
        # In PRN analyzer aliasing ident_input to self.identifier and self.password
        self.identifier = self.ident_input
        self.password = self.pwd_input
        
        self.identifier.returnPressed.connect(self.login)
        self.password.returnPressed.connect(self.login)

    def login(self) -> None:
        try:
            user = authenticate(self.identifier.text().strip(), self.password.text())
        except Exception as exc:
            QMessageBox.critical(self, "DATABASE ERROR", str(exc))
            return

        if not user:
            QMessageBox.warning(self, "LOGIN FAILED", "INVALID CREDENTIALS OR INACTIVE ACCOUNT.")
            self.log("SUBJECT RESTRICTIONS LOADED")
            return

        role = user["role"]
        if role == "admin":
            self.dashboard = AdminWindow(user, self.return_to_login)
        elif role == "faculty":
            self.dashboard = FacultyWindow(user, self.return_to_login)
        elif role == "student":
            self.dashboard = StudentWindow(user, self.return_to_login)
        else:
            QMessageBox.critical(self, "ACCESS DENIED", f"UNKNOWN ROLE: {role}")
            return

        self.dashboard.show()
        self.hide()

    def return_to_login(self) -> None:
        self.identifier.clear()
        self.password.clear()
        self.show()


class AdminWindow(BaseWindow):
    def __init__(self, user: dict, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.setWindowTitle("SPA — ADMIN DASHBOARD")
        self.setMinimumSize(1024, 800)
        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setSpacing(8)
        outer.setContentsMargins(10, 8, 10, 8)
        self.setCentralWidget(root)

        # Header
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header = QHBoxLayout(header_frame)
        title = QLabel("Admin Control Panel")
        title.setObjectName("appTitle")
        header.addWidget(title)
        header.addStretch()
        refresh = QPushButton("Refresh")
        refresh.setObjectName("refreshButton")
        refresh.clicked.connect(self.refresh)
        logout = QPushButton("Logout")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(self.logout)
        header.addWidget(refresh)
        header.addWidget(logout)
        outer.addWidget(header_frame)
        
        body = QHBoxLayout()
        body.setSpacing(24)
        
        left_frame = QFrame()
        left_frame.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_frame)
        left_layout.setSpacing(16)
        
        profile_frame = QFrame()
        profile_frame.setObjectName("profileFrame")
        profile_layout = QVBoxLayout(profile_frame)
        profile_title = QLabel("Admin Profile")
        profile_title.setObjectName("profileTitle")
        profile_layout.addWidget(profile_title)
        profile_layout.addWidget(QLabel(f"Username: {user['username']}"))
        profile_layout.addWidget(QLabel("Role: Admin"))
        profile_layout.addWidget(QLabel("Status: Online"))
        left_layout.addWidget(profile_frame)
        
        sidebar = QListWidget()
        sidebar.setObjectName("navSidebar")
        left_layout.addWidget(sidebar)
        
        add_user = QPushButton("Create User")
        add_user.setObjectName("secondary_btn")
        add_user.clicked.connect(self.create_user)
        add_subject = QPushButton("Add Subject")
        add_subject.setObjectName("secondary_btn")
        add_subject.clicked.connect(self.add_subject)
        toggle = QPushButton("Toggle User")
        toggle.setObjectName("secondary_btn")
        toggle.clicked.connect(self.toggle_user)
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        actions_layout.addWidget(add_user)
        actions_layout.addWidget(add_subject)
        actions_layout.addWidget(toggle)
        left_layout.addLayout(actions_layout)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumHeight(80)
        self.terminal.setPlainText("Admin session active.")
        left_layout.addWidget(self.terminal)
        
        stack = QStackedWidget()
        
        self.users_table = QTableWidget()
        stack.addWidget(self.users_table)
        sidebar.addItem("Users")
        
        self.subject_list = QListWidget()
        stack.addWidget(self.subject_list)
        sidebar.addItem("Subjects")
        
        self.audit_table = QTableWidget()
        stack.addWidget(self.audit_table)
        sidebar.addItem("Audit")
        
        analytics_tab = QWidget()
        analytics_layout = QHBoxLayout(analytics_tab)
        self.analytics_table = QTableWidget()
        self.donut_chart = DonutChart()
        analytics_layout.addWidget(self.analytics_table, 1)
        analytics_layout.addWidget(self.donut_chart, 1)
        stack.addWidget(analytics_tab)
        sidebar.addItem("Analytics")
        
        sidebar.currentRowChanged.connect(stack.setCurrentIndex)
        sidebar.setCurrentRow(0)
        
        body.addWidget(left_frame, 1)
        body.addWidget(stack, 4)
        outer.addLayout(body)
        self.resize(1300, 800)
        self.refresh()

    def refresh(self):
        self.load_table(self.users_table, ["Username", "Role", "Status", "Created"], [
            (u, r, "ACTIVE" if a else "DISABLED", c)
            for u, r, a, c in fetch_all("SELECT username, role, is_active, created_at FROM users ORDER BY role, username")
        ])
        self.subject_list.clear()
        self.subject_list.addItems(subjects())
        self.load_table(self.audit_table, ["User", "Action", "Details", "Timestamp"], fetch_all(
            "SELECT COALESCE(u.username, 'SYSTEM'), a.action, a.details, a.timestamp FROM audit_log a LEFT JOIN users u ON u.id=a.user_id ORDER BY a.timestamp DESC LIMIT 50"
        ))
        self.log("Admin data refreshed.")
        
        # Load Analytics
        self.analytics_table.setColumnCount(7)
        self.analytics_table.setHorizontalHeaderLabels(["Report", "Field 1", "Field 2", "Field 3", "Field 4", "Field 5", "Field 6"])
        analytics_rows = []
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT 'A (>= 90)', SUM(CASE WHEN marks >= 90 THEN 1 ELSE 0 END) FROM student_marks UNION ALL SELECT 'B (75-89)', SUM(CASE WHEN marks >= 75 AND marks < 90 THEN 1 ELSE 0 END) FROM student_marks UNION ALL SELECT 'C (60-74)', SUM(CASE WHEN marks >= 60 AND marks < 75 THEN 1 ELSE 0 END) FROM student_marks UNION ALL SELECT 'D (40-59)', SUM(CASE WHEN marks >= 40 AND marks < 60 THEN 1 ELSE 0 END) FROM student_marks UNION ALL SELECT 'F (< 40)', SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END) FROM student_marks")
            grade_dist = cur.fetchall()
            counts = [int(count or 0) for label, count in grade_dist]
            self.donut_chart.set_data(counts)
            for label, count in grade_dist:
                analytics_rows.append(("Marks Distribution", label, str(count or 0), "", "", "", ""))
        finally:
            conn.close()
            
        self.analytics_table.setRowCount(len(analytics_rows))
        for row_index, row in enumerate(analytics_rows):
            for col, value in enumerate(row):
                self.analytics_table.setItem(row_index, col, QTableWidgetItem(str(value)))
        self.analytics_table.resizeColumnsToContents()

    def load_table(self, table, headers, rows):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()

    def add_subject(self):
        name, ok = QInputDialog.getText(self, "ADD SUBJECT", "SUBJECT NAME:")
        if ok and name.strip():
            execute("INSERT INTO subjects(name) VALUES (%s)", (name.strip(),))
            log_audit(self.user["id"], "ADD_SUBJECT", f"subject={name.strip()}")
            self.refresh()

    def create_user(self):
        QMessageBox.information(self, "CREATE USER", "USE ADMIN DASHBOARD IN THE MODULAR PROJECT FOR FULL GUIDED USER CREATION.")

    def toggle_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            return
        username = self.users_table.item(row, 0).text()
        if username == self.user["username"]:
            QMessageBox.warning(self, "BLOCKED", "YOU CANNOT DISABLE YOURSELF.")
            return
        active = fetch_all("SELECT is_active FROM users WHERE username=%s", (username,))
        if active:
            execute("UPDATE users SET is_active=%s WHERE username=%s", (not bool(active[0][0]), username))
            log_audit(self.user["id"], "TOGGLE_USER", f"username={username}")
            self.refresh()

    def logout(self):
        self.on_logout()
        self.close()


class FacultyWindow(BaseWindow):
    def __init__(self, user: dict, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.current_student = None
        self.setWindowTitle("SPA — FACULTY DASHBOARD")
        self.setMinimumSize(1024, 700)
        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setSpacing(8)
        outer.setContentsMargins(10, 8, 10, 8)
        self.setCentralWidget(root)

        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header = QHBoxLayout(header_frame)
        title = QLabel("Faculty Marks Console")
        title.setObjectName("appTitle")
        header.addWidget(title)
        header.addStretch()
        logout = QPushButton("Logout")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(self.logout)
        header.addWidget(logout)
        outer.addWidget(header_frame)

        body = QHBoxLayout()
        body.setSpacing(24)
        
        left_frame = QFrame()
        left_frame.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_frame)
        left_layout.setSpacing(16)
        
        profile_frame = QFrame()
        profile_frame.setObjectName("profileFrame")
        profile_layout = QVBoxLayout(profile_frame)
        profile_title = QLabel("Faculty Info")
        profile_title.setObjectName("profileTitle")
        profile_layout.addWidget(profile_title)
        profile_layout.addWidget(QLabel(f"Username: {user['username']}"))
        profile_layout.addWidget(QLabel("Role: Faculty"))
        left_layout.addWidget(profile_frame)
        
        sidebar = QListWidget()
        sidebar.setObjectName("navSidebar")
        left_layout.addWidget(sidebar)
        
        self.student_label = QLabel("No student selected")
        self.student_label.setStyleSheet("color: #111827; font-weight: 800; font-size: 12px;")
        self.subject_combo = QComboBox()
        self.mark_input = QLineEdit()
        self.mark_input.setPlaceholderText("Marks 0-100")
        save = QPushButton("Save Mark")
        save.clicked.connect(self.save_mark)
        bulk = QPushButton("Save Subject Marks")
        bulk.setObjectName("secondary_btn")
        bulk.clicked.connect(self.bulk_update)
        self.subject_combo.currentTextChanged.connect(self.load_roster)
        left_layout.addWidget(self.student_label)
        left_layout.addWidget(self.subject_combo)
        left_layout.addWidget(self.mark_input)
        left_layout.addWidget(save)
        left_layout.addWidget(bulk)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumHeight(80)
        self.terminal.setPlainText("Faculty session active.\nSubject access is restricted.")
        left_layout.addWidget(self.terminal)

        stack = QStackedWidget()
        self.tabs = stack  # Aliasing tabs to stack so self.tabs.setCurrentWidget works
        
        marks_tab = QWidget()
        marks_layout = QVBoxLayout(marks_tab)
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        self.prn = QLineEdit()
        self.prn.setPlaceholderText("Enter student PRN...")
        search = QPushButton("Search")
        search.clicked.connect(self.search_student)
        search_layout.addWidget(self.prn)
        search_layout.addWidget(search)
        marks_layout.addWidget(search_frame)
        self.marks_table = QTableWidget()
        marks_layout.addWidget(self.marks_table)
        
        stack.addWidget(marks_tab)
        sidebar.addItem("Student Marks")
        
        self.roster_table = QTableWidget()
        stack.addWidget(self.roster_table)
        sidebar.addItem("Subject Roster")
        
        self.subject_list = QListWidget()
        stack.addWidget(self.subject_list)
        sidebar.addItem("Subjects")
        
        sidebar.currentRowChanged.connect(stack.setCurrentIndex)
        sidebar.setCurrentRow(0)

        body.addWidget(left_frame, 1)
        body.addWidget(stack, 4)
        outer.addLayout(body)
        self.resize(1300, 800)
        self.refresh_subjects()

    def refresh_subjects(self):
        rows = fetch_all("SELECT subject_name FROM faculty_subjects WHERE faculty_id=%s ORDER BY subject_name", (self.user["id"],))
        names = [r[0] for r in rows]
        self.subject_list.clear()
        self.subject_list.addItems(names)
        self.subject_combo.clear()
        self.subject_combo.addItems(names)

    def search_student(self):
        rows = fetch_all("SELECT id, name, department, prn FROM students WHERE prn=%s", (self.prn.text().strip(),))
        if not rows:
            QMessageBox.information(self, "NOT FOUND", "STUDENT NOT FOUND.")
            return
        self.current_student = rows[0]
        self.student_label.setText(f"{rows[0][1]} | {rows[0][2]} | {rows[0][3]}")
        self.load_marks(rows[0][0])

    def load_marks(self, student_id):
        rows = fetch_all("SELECT subject, marks FROM student_marks WHERE student_id=%s ORDER BY subject", (student_id,))
        self.load_table(self.marks_table, ["Subject", "Marks"], rows)

    def load_roster(self, subject):
        if not subject:
            return
        rows = fetch_all(
            """
            SELECT s.id, s.name, s.prn, sm.marks
            FROM students s
            LEFT JOIN student_marks sm ON sm.student_id=s.id AND sm.subject=%s
            ORDER BY s.name
            """,
            (subject,),
        )
        self.load_table(self.roster_table, ["ID", "Student", "PRN", "Marks"], rows)
        self.roster_table.setColumnHidden(0, True)
        self.tabs.setCurrentWidget(self.roster_table)

    def load_table(self, table, headers, rows):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem("" if value is None else str(value))
                if table is self.roster_table and c in {0, 1, 2}:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(r, c, item)
        table.resizeColumnsToContents()

    def save_mark(self):
        if not self.current_student:
            QMessageBox.information(self, "NO STUDENT", "SEARCH A STUDENT FIRST.")
            return
        self.upsert_mark(self.current_student[0], self.subject_combo.currentText(), float(self.mark_input.text()))
        self.load_marks(self.current_student[0])
        self.load_roster(self.subject_combo.currentText())

    def upsert_mark(self, student_id, subject, marks):
        if not 0 <= marks <= 100:
            raise ValueError("MARKS MUST BE BETWEEN 0 AND 100.")
        exists = fetch_all("SELECT id FROM student_marks WHERE student_id=%s AND subject=%s", (student_id, subject))
        if exists:
            execute("UPDATE student_marks SET marks=%s WHERE student_id=%s AND subject=%s", (marks, student_id, subject))
        else:
            execute("INSERT INTO student_marks(student_id, subject, marks) VALUES (%s, %s, %s)", (student_id, subject, marks))
        log_audit(self.user["id"], "UPSERT_MARKS", f"student_id={student_id} subject={subject} marks={marks}")

    def bulk_update(self):
        subject = self.subject_combo.currentText()
        for row in range(self.roster_table.rowCount()):
            sid = self.roster_table.item(row, 0)
            marks = self.roster_table.item(row, 3)
            if sid and marks and marks.text().strip():
                self.upsert_mark(int(sid.text()), subject, float(marks.text()))
        self.load_roster(subject)
        QMessageBox.information(self, "SUBJECT MARKS", "SUBJECT MARKS UPDATED.")

    def logout(self):
        self.on_logout()
        self.close()


class StudentWindow(BaseWindow):
    def __init__(self, user: dict, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.rows = []
        self.gpa = 0
        self.setWindowTitle("SPA — STUDENT DASHBOARD")
        self.setMinimumSize(1024, 700)
        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setSpacing(8)
        outer.setContentsMargins(10, 8, 10, 8)
        self.setCentralWidget(root)

        # Header
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header = QHBoxLayout(header_frame)
        title = QLabel("Student Performance Feed")
        title.setObjectName("appTitle")
        header.addWidget(title)
        header.addStretch()
        refresh = QPushButton("Refresh")
        refresh.setObjectName("refreshButton")
        refresh.clicked.connect(self.refresh)
        export = QPushButton("Export CSV")
        export.setObjectName("exportButton")
        export.clicked.connect(self.export_csv)
        logout = QPushButton("Logout")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(self.logout)
        header.addWidget(refresh)
        header.addWidget(export)
        header.addWidget(logout)
        outer.addWidget(header_frame)

        content = QHBoxLayout()
        content.setSpacing(24)
        
        left_frame = QFrame()
        left_frame.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_frame)
        left_layout.setSpacing(16)
        
        profile_frame = QFrame()
        profile_frame.setObjectName("profileFrame")
        profile_layout = QVBoxLayout(profile_frame)
        profile_title = QLabel("Student Info")
        profile_title.setObjectName("profileTitle")
        profile_layout.addWidget(profile_title)
        profile_layout.addWidget(QLabel(f"Username: {user['username']}"))
        profile_layout.addWidget(QLabel("Role: Student"))
        self.gpa_label = QLabel("GPA: 0.0")
        self.gpa_label.setObjectName("gpaLabel")
        profile_layout.addWidget(self.gpa_label)
        left_layout.addWidget(profile_frame)
        
        sidebar = QListWidget()
        sidebar.setObjectName("navSidebar")
        left_layout.addWidget(sidebar)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumHeight(80)
        self.terminal.setPlainText("Student session active.")
        left_layout.addWidget(self.terminal)

        stack = QStackedWidget()
        self.tabs = stack  # alias to avoid rewriting other code if any
        
        perf_tab = QWidget()
        perf_layout = QHBoxLayout(perf_tab)
        self.table = QTableWidget()
        self.bar_chart = BarChart()
        perf_layout.addWidget(self.table, 1)
        perf_layout.addWidget(self.bar_chart, 1)
        
        stack.addWidget(perf_tab)
        sidebar.addItem("Performance")
        
        sidebar.currentRowChanged.connect(stack.setCurrentIndex)
        sidebar.setCurrentRow(0)

        content.addWidget(left_frame, 1)
        content.addWidget(stack, 4)
        outer.addLayout(content)
        self.resize(1100, 720)
        self.refresh()

    def refresh(self):
        student_id = self.user.get("student_id")
        self.rows = fetch_all("SELECT subject, marks FROM student_marks WHERE student_id=%s ORDER BY subject", (student_id,))
        self.gpa = round(sum(float(r[1]) for r in self.rows) / len(self.rows), 2) if self.rows else 0
        self.gpa_label.setText(f"GPA: {self.gpa}")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Subject", "Marks"])
        self.table.setRowCount(len(self.rows))
        chart_data = []
        for row_index, row in enumerate(self.rows):
            subject = row[0]
            marks_val = row[1]
            if marks_val != 'Not Entered':
                try:
                    chart_data.append((subject, float(marks_val)))
                except ValueError:
                    pass
            for col, value in enumerate(row):
                self.table.setItem(row_index, col, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()
        self.bar_chart.set_data(chart_data)
        
        self.log("Student performance feed refreshed.")

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Csv", f"{self.user['username']}_report.csv", "Csv Files (*.csv)")
        if not path:
            return
        with Path(path).open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Subject", "Marks"])
            writer.writerows(self.rows)
            writer.writerow([])
            writer.writerow(["Average (GPA)", self.gpa])

    def logout(self):
        self.on_logout()
        self.close()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Student Performance Analyzer")
    app.setStyleSheet(QSS)
    login = LoginWindow()
    login.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
