import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF

class DonutChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.colors = [
            QColor("#4ADE80"), # A - Green
            QColor("#60A5FA"), # B - Blue
            QColor("#FBBF24"), # C - Yellow
            QColor("#F87171"), # D - Red
            QColor("#9CA3AF")  # F - Gray
        ]
        self.labels = ["A", "B", "C", "D", "F"]
        self.center_text = "Students"
        self.setMinimumSize(250, 250)

    def set_data(self, data):
        # data is a list of 5 integers [grade_a_count, b, c, d, f]
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
        
        # Calculate chart area
        width = self.width()
        height = self.height()
        size = min(width, height) - 40
        rect = QRectF((width - size) / 2, (height - size) / 2, size, size)
        
        start_angle = 90 * 16 # Start at 12 o'clock

        for i, value in enumerate(self.data):
            if value == 0:
                continue
            span_angle = -int((value / total) * 360 * 16)
            
            painter.setBrush(QBrush(self.colors[i]))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, start_angle, span_angle)
            
            start_angle += span_angle

        # Draw inner circle for donut effect
        inner_size = size * 0.65
        inner_rect = QRectF((width - inner_size) / 2, (height - inner_size) / 2, inner_size, inner_size)
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(inner_rect)

        # Draw total text in the center
        painter.setPen(QColor("#111827"))
        painter.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        painter.drawText(inner_rect, Qt.AlignmentFlag.AlignCenter, str(total))
        
        painter.setFont(QFont("Inter", 10))
        painter.setPen(QColor("#6B7280"))
        painter.drawText(inner_rect.adjusted(0, 25, 0, 0), Qt.AlignmentFlag.AlignCenter, self.center_text)
        
        # Draw legend
        legend_y = height - 20
        legend_x = (width - (len(self.data) * 40)) / 2
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
        self.data = []  # list of tuples (subject_name, marks)
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

        width = self.width()
        height = self.height()
        
        margin_left = 40
        margin_right = 20
        margin_top = 30
        margin_bottom = 60
        
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        
        # Draw background grid lines (25, 50, 75, 100)
        painter.setPen(QPen(QColor("#E5E7EB"), 1, Qt.PenStyle.DashLine))
        for i in range(5):
            y = margin_top + chart_height - (i * chart_height / 4)
            painter.drawLine(margin_left, int(y), width - margin_right, int(y))
            
            # Y-axis labels
            painter.setPen(QColor("#6B7280"))
            painter.setFont(QFont("Inter", 9))
            painter.drawText(0, int(y - 10), margin_left - 10, 20, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, str(i * 25))
            painter.setPen(QPen(QColor("#E5E7EB"), 1, Qt.PenStyle.DashLine))

        num_bars = len(self.data)
        bar_width = min(40, chart_width / (num_bars * 1.5))
        spacing = (chart_width - (num_bars * bar_width)) / (num_bars + 1)

        painter.setFont(QFont("Inter", 9))

        for i, (subject, marks) in enumerate(self.data):
            marks_float = float(marks)
            x = margin_left + spacing + i * (bar_width + spacing)
            bar_height = (marks_float / 100.0) * chart_height
            y = margin_top + chart_height - bar_height

            # Determine color based on marks
            if marks_float >= 90:
                color = QColor("#4ADE80") # Green
            elif marks_float >= 75:
                color = QColor("#60A5FA") # Blue
            elif marks_float >= 60:
                color = QColor("#FBBF24") # Yellow
            elif marks_float >= 40:
                color = QColor("#F97316") # Orange
            else:
                color = QColor("#F87171") # Red

            # Draw bar with rounded top corners
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            rect = QRectF(x, y, bar_width, bar_height)
            painter.drawRoundedRect(rect, 4, 4)
            
            # Draw square bottom to overwrite the bottom rounding
            if bar_height > 4:
                bottom_rect = QRectF(x, y + 4, bar_width, bar_height - 4)
                painter.drawRect(bottom_rect)

            # Draw marks label above bar
            painter.setPen(QColor("#111827"))
            painter.drawText(int(x), int(y - 20), int(bar_width), 20, Qt.AlignmentFlag.AlignCenter, f"{marks:g}")

            # Draw subject label (truncated)
            painter.setPen(QColor("#4B5563"))
            display_name = subject[:6] + ".." if len(subject) > 8 else subject
            painter.drawText(int(x - 10), int(margin_top + chart_height + 5), int(bar_width + 20), 30, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, display_name)
