from PyQt6 import uic
from PyQt6.QtWidgets import (
    QFileDialog, QFrame, QHBoxLayout, QMainWindow, QMessageBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from academic import AcademicService
from app_paths import resource_path
from std import StudentService
from custom_charts import BarChart, DonutChart


class StudentController(QMainWindow):
    def __init__(self, user: dict, on_logout=None):
        super().__init__()
        uic.loadUi(resource_path("ui", "student.ui"), self)
        self.user = user
        self.on_logout = on_logout
        self.rows = []
        self.average_marks = 0.0
        self.gpa = 0.0
        self.grade = "F"
        self.usernameLabel.setText(f"Username: {user['username']}")
        self.roleLabel.setText("Role: Student")
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setMinimumHeight(80)
        self.gpaLabel.setWordWrap(True)
        self.gpaLabel.setMinimumHeight(80)
        self.statusLabel.setMinimumHeight(100)

        # Inject BarChart into performanceLayout above the table
        self.barChart = BarChart()
        self.performanceLayout.insertWidget(0, self.barChart)

        # Setup navigation buttons
        self.btnPerformance.clicked.connect(lambda: self.contentStack.setCurrentIndex(0))
        self.btnAnalytics.clicked.connect(lambda: self.contentStack.setCurrentIndex(1))
        self.btnLeaderboard.clicked.connect(lambda: self.contentStack.setCurrentIndex(2))

        # Setup Donut Chart inside analytics tab
        # The analyticsTab already has a QVBoxLayout with analyticsTable
        # We restructure it: remove the table, create HBox with table + donut
        self.donutChart = DonutChart()
        self.donutChart.setMaximumSize(180, 180)
        self.donutChart.setMinimumSize(120, 120)
        self.donutChart.center_text = "Students"

        # Remove analyticsTable from its existing layout
        self.analyticsLayout.removeWidget(self.analyticsTable)

        # Create horizontal wrapper
        analytics_wrapper = QWidget()
        h_layout = QHBoxLayout(analytics_wrapper)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(self.analyticsTable, 5)

        chart_container = QFrame()
        chart_container.setObjectName("rightPanel")
        chart_container.setMaximumWidth(200)
        chart_v = QVBoxLayout(chart_container)
        chart_v.addWidget(self.donutChart)
        h_layout.addWidget(chart_container, 1)

        self.analyticsLayout.addWidget(analytics_wrapper)

        self.refreshButton.clicked.connect(self.refresh)
        self.exportButton.clicked.connect(self.export_csv)
        self.logoutButton.clicked.connect(self.logout)
        self.refresh()

    def refresh(self) -> None:
        student_id = self.user.get("student_id")
        if not student_id:
            QMessageBox.critical(self, "Profile Error", "No student profile is linked to this account.")
            return
        try:
            profile = AcademicService.student_profile(student_id)
            self.rows = StudentService.marks(student_id)
            self.average_marks = StudentService.average_marks(self.rows)
            self.gpa = StudentService.gpa(self.rows)
            self.grade = StudentService.grade(self.rows)
            if profile:
                _, name, department, prn, average_marks, gpa, grade, subject_count = profile
                self.average_marks = float(average_marks)
                self.gpa = float(gpa)
                self.grade = grade
                self.statusLabel.setText(
                    f"Name: {name}\nDepartment: {department}\nPRN: {prn}\nSubjects Marked: {subject_count}"
                )
            self.gpaLabel.setText(f"GPA: {self.gpa}\nAvg: {self.average_marks}\nGrade: {self.grade}")
            self.marksTable.setColumnCount(4)
            self.marksTable.setHorizontalHeaderLabels(["Subject", "Marks", "Grade", "Result"])
            self.marksTable.setRowCount(len(self.rows))
            chart_data = []
            for row_index, row in enumerate(self.rows):
                subject = row[0]
                marks_val = row[1]
                if marks_val != 'Not Entered':
                    try:
                        chart_data.append((subject, float(marks_val)))
                    except (ValueError, TypeError):
                        pass
                for col, value in enumerate(row):
                    self.marksTable.setItem(row_index, col, QTableWidgetItem(str(value)))
            self.marksTable.resizeColumnsToContents()
            self.barChart.set_data(chart_data)
            self.load_analytics()
            self.load_leaderboard()
            self.log("Student performance refreshed.")
        except Exception as exc:
            QMessageBox.critical(self, "Refresh Failed", str(exc))

    def load_table(self, table: QTableWidget, headers: list[str], rows: list[tuple]) -> None:
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col, value in enumerate(row):
                table.setItem(row_index, col, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()

    def load_analytics(self) -> None:
        self.load_table(
            self.analyticsTable,
            ["Report", "Field 1", "Field 2", "Field 3", "Field 4", "Field 5", "Field 6"],
            AcademicService.analytics_dashboard_rows(),
        )
        # Load chart data for donut chart - display distribution of letter grades for the WHOLE CLASS
        # Data format expected by DonutChart: [A_count, B_count, C_count, D_count, F_count]
        # grade_distribution returns: [('A (>= 90)', count), ('B (75-89)', count), ...]
        distribution = AcademicService.grade_distribution()
        donut_data = [count for _, count in distribution]
        
        if sum(donut_data) > 0:
            self.donutChart.set_data(donut_data)
        else:
            self.donutChart.set_data([0, 0, 0, 0, 0])

    def load_leaderboard(self) -> None:
        self.load_table(
            self.leaderboardTable,
            ["Rank", "Name", "PRN", "Department", "Average", "GPA", "Grade", "Subjects"],
            AcademicService.top_performers(),
        )

    def log(self, message: str) -> None:
        self.terminalOutput.append(f"> {message}")

    def export_csv(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", f"{self.user['username']}_report.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            StudentService.export_csv(path, self.rows, self.average_marks, self.gpa, self.grade)
            self.log(f"CSV EXPORTED: {path}")
        except Exception as exc:
            QMessageBox.critical(self, "Export Failed", str(exc))

    def logout(self) -> None:
        if self.on_logout:
            self.on_logout()
        self.close()
