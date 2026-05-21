import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap

os.environ["SPA_DB_PASSWORD"] = "mysql"

app = QApplication(sys.argv)

def save_screenshot(widget, filename):
    widget.show()
    # Let it render and fetch data
    for _ in range(10):
        app.processEvents()
    
    # Take screenshot
    pixmap = widget.grab()
    pixmap.save(filename)
    widget.close()

from controllers.student_controller import StudentController
from controllers.faculty_controller import FacultyController

try:
    print("Testing Student...")
    s = StudentController({'username': 'std1', 'student_id': 1}, None)
    save_screenshot(s, "student_test_screenshot.png")

    print("Testing Faculty...")
    f = FacultyController({'username': 'fac1', 'id': 1}, None)
    save_screenshot(f, "faculty_test_screenshot.png")

    print("Screenshots captured successfully!")
except Exception as e:
    print(f"Error capturing screenshots: {e}")
