import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QTableWidget, 
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, 
                            QFrame, QDialog, QMessageBox, QCheckBox, QComboBox, QDateEdit,
                            QScrollArea, QSizePolicy, QStackedWidget, QToolButton, QMenu,
                            QListWidget, QListWidgetItem, QGridLayout, QHeaderView)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize, QDate, QTimer, QLocale, pyqtSignal

# Import color constants from ui_constants.py
from ui_constants import *

# Import custom dialogs from custom_dialogs.py
from custom_dialogs import CustomWarningDialog, CustomInfoDialog, CustomMessageBox

# New class for form windows
class FormationFormWindow(QMainWindow):
    # Signal to send form data back to main window
    formSaved = pyqtSignal(list)
    
    def __init__(self, parent=None, title="Form Window", form_data=None):
        """
        Initialize the form window with title and optional data
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set window flags to have maximize, restore, and close buttons
        self.setWindowFlags(
            Qt.Window |              # Regular window
            Qt.WindowCloseButtonHint |  # Close button
            Qt.WindowMaximizeButtonHint |  # Maximize button
            Qt.WindowMinimizeButtonHint    # Minimize button
        )
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create a scroll area for the form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {DARK_BG};
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 0px;  /* Hide scrollbar but keep functionality */
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: transparent;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Create form content
        form_content = QWidget()
        form_layout = QVBoxLayout(form_content)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet(f"background-color: {LIGHT_BG}; border-radius: 10px;")
        form_container.setFixedWidth(500)  # Reduced width from 600 to 500
        
        container_layout = QVBoxLayout(form_container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Form fields
        fields = [
            {"name": "السنة", "type": "text", "placeholder": "أدخل السنة"},
            {"name": "رقم الموظف", "type": "text", "placeholder": "أدخل رقم الموظف"},
            {"name": "الإسم", "type": "text", "placeholder": "أدخل الإسم"},
            {"name": "اللقب", "type": "text", "placeholder": "أدخل اللقب"},
            {"name": "نوع التكوين", "type": "combo", "options": ["تقني", "إداري", "مهني", "أخرى"]},
            {"name": "تاريخ البدء", "type": "date"},
            {"name": "تاريخ الإنتهاء", "type": "date"},
            {"name": "مدة التكوين", "type": "text", "placeholder": "تحسب تلقائيا", "readonly": True},
            {"name": "مؤسسة التكوين", "type": "text", "placeholder": "أدخل مؤسسة التكوين"},
            {"name": "محتوى التكوين", "type": "text", "placeholder": "أدخل محتوى التكوين"}
        ]
        
        self.form_fields = {}
        
        for field in fields:
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)
            
            label = QLabel(field["name"])
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            label.setAlignment(Qt.AlignRight)
            
            if field["type"] == "date":
                input_field = QDateEdit()
                input_field.setCalendarPopup(True)
                input_field.setDate(QDate.currentDate())
                
                if field["name"] == "تاريخ الإنتهاء":
                    input_field.setMaximumDate(QDate.currentDate())
                
                input_field.setDisplayFormat("yyyy-MM-dd")
                
                input_field.setStyleSheet(f"""
                    QDateEdit {{
                        background-color: {DARKER_BG};
                        border: none;
                        border-radius: 5px;
                        padding: 8px;
                        color: {WHITE};
                        font-size: 13px;
                    }}
                """)
                
                if field["name"] == "تاريخ البدء" or field["name"] == "تاريخ الإنتهاء":
                    input_field.dateChanged.connect(self.calculate_formation_period)
            elif field["type"] == "combo":
                input_field = QComboBox()
                input_field.addItems(field["options"])
                input_field.setStyleSheet(f"""
                    QComboBox {{
                        background-color: {DARKER_BG};
                        border: none;
                        border-radius: 5px;
                        padding: 8px;
                        color: {WHITE};
                        font-size: 13px;
                        text-align: right;
                    }}
                    QComboBox::drop-down {{
                        border: none;
                    }}
                    QComboBox::down-arrow {{
                        image: url(dropdown.png);
                        width: 12px;
                        height: 12px;
                    }}
                """)
                input_field.setLayoutDirection(Qt.RightToLeft)
            else:
                input_field = QLineEdit()
                input_field.setPlaceholderText(field.get("placeholder", ""))
                input_field.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: {DARKER_BG};
                        border: none;
                        border-radius: 5px;
                        padding: 8px;
                        color: {WHITE};
                        font-size: 13px;
                        text-align: right;
                    }}
                """)
                input_field.setLayoutDirection(Qt.RightToLeft)
                input_field.setAlignment(Qt.AlignRight)
                
                if field.get("readonly", False):
                    input_field.setReadOnly(True)
                    input_field.setStyleSheet(input_field.styleSheet() + f"background-color: #3A3D42;")
            
            field_layout.addWidget(label)
            field_layout.addWidget(input_field)
            container_layout.addLayout(field_layout)
            
            self.form_fields[field["name"]] = input_field
        
        # Fill form with data if provided
        if form_data:
            self.fill_form_with_data(form_data)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        save_btn = QPushButton("حفظ")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {GREEN};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #3d8b40;
            }}
        """)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {RED};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #d32f2f;
            }}
        """)
        
        # Connect buttons
        save_btn.clicked.connect(self.save_form)
        cancel_btn.clicked.connect(self.close)
        
        # Add buttons in right-to-left order for Arabic
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        container_layout.addLayout(buttons_layout)
        
        # Add to form layout
        form_layout.addWidget(title_label)
        form_layout.addWidget(form_container, 0, Qt.AlignCenter)
        
        # Set the form content as the scroll area widget
        scroll_area.setWidget(form_content)
        
        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)
        
        # Get current date for validation
        self.today = QDate.currentDate()
    
    def fill_form_with_data(self, data):
        """Fill form fields with provided data"""
        for i, (field_name, field) in enumerate(self.form_fields.items()):
            if i < len(data):
                value = data[i]
                if isinstance(field, QDateEdit):
                    date = QDate.fromString(value, "yyyy-MM-dd")
                    field.setDate(date)
                elif isinstance(field, QComboBox):
                    index = field.findText(value)
                    if index >= 0:
                        field.setCurrentIndex(index)
                else:
                    field.setText(value)
    
    def calculate_formation_period(self):
        """Calculate the formation period automatically based on start and end dates"""
        if "تاريخ البدء" in self.form_fields and "تاريخ الإنتهاء" in self.form_fields and "مدة التكوين" in self.form_fields:
            start_date = self.form_fields["تاريخ البدء"].date()
            end_date = self.form_fields["تاريخ الإنتهاء"].date()
            
            days_diff = start_date.daysTo(end_date)
            
            if days_diff >= 0:
                self.form_fields["مدة التكوين"].setText(f"{days_diff} يوم")
            else:
                self.form_fields["مدة التكوين"].setText("تاريخ البدء بعد تاريخ الإنتهاء!")
    
    def validate_form(self):
        """
        Validate the form fields
        Checks required fields, numeric values, and date ranges
        """
        # Check required fields
        required_fields = ["السنة", "رقم الموظف", "الإسم", "اللقب"]
        
        for field_name in required_fields:
            field = self.form_fields[field_name]
            if isinstance(field, QLineEdit) and not field.text().strip():
                # Use custom dialog instead of QMessageBox
                warning_dialog = CustomWarningDialog(self, "تحذير", f"الرجاء إدخال {field_name}")
                warning_dialog.exec_()
                field.setFocus()
                return False
                
        # Validate employee ID format (numeric)
        emp_id_field = self.form_fields["رقم الموظف"]
        if not emp_id_field.text().isdigit():
            warning_dialog = CustomWarningDialog(self, "تحذير", "رقم الموظف يجب أن يكون رقمًا")
            warning_dialog.exec_()
            emp_id_field.setFocus()
            return False
            
        # Validate year format (numeric)
        year_field = self.form_fields["السنة"]
        if not year_field.text().isdigit():
            warning_dialog = CustomWarningDialog(self, "تحذير", "السنة يجب أن تكون رقمًا")
            warning_dialog.exec_()
            year_field.setFocus()
            return False
            
        # Validate date range
        start_date = self.form_fields["تاريخ البدء"].date()
        end_date = self.form_fields["تاريخ الإنتهاء"].date()
        
        if start_date > end_date:
            warning_dialog = CustomWarningDialog(self, "تحذير", "تاريخ البدء يجب أن يكون قبل تاريخ الإنتهاء")
            warning_dialog.exec_()
            return False
            
        # Validate end date is not after today
        if end_date > self.today:
            warning_dialog = CustomWarningDialog(self, "تحذير", "تاريخ الإنتهاء يجب أن يكون قبل أو يساوي اليوم الحالي")
            warning_dialog.exec_()
            return False
            
        return True
    
    def save_form(self):
        """Save form data and emit signal with the data"""
        # Validate form data
        if not self.validate_form():
            return
        
        # Get form data
        form_data = []
        for field_name, field in self.form_fields.items():
            if isinstance(field, QDateEdit):
                form_data.append(field.date().toString("yyyy-MM-dd"))
            elif isinstance(field, QComboBox):
                form_data.append(field.currentText())
            else:
                form_data.append(field.text())
        
        # Emit signal with form data
        self.formSaved.emit(form_data)
        
        # Close the window
        self.close()

# New class for history window
class HistoryWindow(QMainWindow):
    def __init__(self, parent=None):
        """
        Initialize the history window
        """
        super().__init__(parent)
        self.setWindowTitle("سجل الأنشطة")
        self.setGeometry(150, 150, 800, 600)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set window flags to have maximize, restore, and close buttons
        self.setWindowFlags(
            Qt.Window |              # Regular window
            Qt.WindowCloseButtonHint |  # Close button
            Qt.WindowMaximizeButtonHint |  # Maximize button
            Qt.WindowMinimizeButtonHint    # Minimize button
        )
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("سجل الأنشطة على إدارة التكوين")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {MEDIUM_BG};
                color: {WHITE};
                border: none;
                gridline-color: {LIGHT_BG};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {LIGHT_BG};
            }}
            QHeaderView::section {{
                background-color: {DARKER_BG};
                color: {WHITE};
                padding: 8px;
                border: none;
                font-weight: bold;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 0px;  /* Hide scrollbar but keep functionality */
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: transparent;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Set up columns
        columns = ["التاريخ", "المستخدم", "التصرف", "التفاصيل"]
        
        self.history_table.setColumnCount(len(columns))
        self.history_table.setHorizontalHeaderLabels(columns)
        
        # Make columns resizable and movable
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setSectionsMovable(True)
        self.history_table.verticalHeader().setVisible(False)
        # Allow moving columns
        self.history_table.horizontalHeader().setSectionsMovable(True)
        # Set column resizing fixed
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        # Set column widths
        self.history_table.setColumnWidth(0, 150)  # Date column
        self.history_table.setColumnWidth(1, 150)  # User column
        self.history_table.setColumnWidth(2, 100)  # Action column
        
        # Set text alignment for all columns to right-aligned
        for i in range(len(columns)):
            self.history_table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Add sample data
        self.load_history_data()
        
        # Close button
        close_btn = QPushButton("إغلاق")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #e05d00;
            }}
        """)
        close_btn.clicked.connect(self.close)
        
        # Add widgets to layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.history_table)
        main_layout.addWidget(close_btn, 0, Qt.AlignCenter)
    
    def load_history_data(self):
        """Load sample history data into the table"""
        history_data = [
            ["2025-04-10 14:30", "أحمد محمد", "إضافة", "إضافة تكوين جديد للموظف رقم 1001"],
            ["2025-04-09 10:15", "سارة أحمد", "تعديل", "تعديل تكوين للموظف رقم 1002"],
            ["2025-04-08 16:45", "محمد علي", "حذف", "حذف تكوين للموظف رقم 1003"],
            ["2025-04-07 09:30", "فاطمة محمد", "إضافة", "إضافة تكوين جديد للموظف رقم 1004"],
            ["2025-04-06 11:20", "أحمد محمد", "تعديل", "تعديل تكوين للموظف رقم 1005"]
        ]
        
        self.history_table.setRowCount(len(history_data))
        
        for row, data in enumerate(history_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.history_table.setItem(row, col, item)

# New class for filter dialog
class FilterDialog(QDialog):
    filterApplied = pyqtSignal(list, str)
    
    def __init__(self, parent=None, columns=None):
        super().__init__(parent)
        self.setWindowTitle("ترشيح")
        self.setFixedWidth(350)
        self.setStyleSheet(f"background-color: {MEDIUM_BG}; color: {WHITE};")
        
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("اختر الأعمدة للترشيح:")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
        dialog_layout.addWidget(title_label)
        
        # Create checkboxes for each column
        if not columns:
            columns = [
                "السنة", "رقم الموظف", "الإسم", "اللقب", "نوع التكوين", 
                "تاريخ البدء", "تاريخ الإنتهاء", "مدة التكوين", "مؤسسة التكوين"
            ]
        
        # Create a scroll area for checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {MEDIUM_BG};
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 0px;  /* Hide scrollbar but keep functionality */
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: transparent;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Create a widget to hold checkboxes
        checkbox_widget = QWidget()
        checkbox_layout = QVBoxLayout(checkbox_widget)
        
        self.filter_checkboxes = {}
        
        for column in columns:
            checkbox = QCheckBox(column)
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    font-size: 14px;
                    padding: 8px 0;
                }}
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                }}
                QCheckBox::indicator:checked {{
                    background-color: {ORANGE};
                    border: 2px solid {WHITE};
                }}
            """)
            checkbox_layout.addWidget(checkbox)
            self.filter_checkboxes[column] = checkbox
        
        # Set the checkbox widget as the scroll area widget
        scroll_area.setWidget(checkbox_widget)
        
        # Filter value input
        filter_value_layout = QHBoxLayout()
        filter_value_layout.setSpacing(10)
        
        filter_value_label = QLabel("قيمة الترشيح:")
        filter_value_label.setStyleSheet("font-size: 14px;")
        
        self.filter_value_input = QLineEdit()
        self.filter_value_input.setPlaceholderText("أدخل قيمة للترشيح...")
        self.filter_value_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: {BLACK};
                font-size: 13px;
                text-align: right;
            }}
        """)
        self.filter_value_input.setLayoutDirection(Qt.RightToLeft)
        
        filter_value_layout.addWidget(filter_value_label)
        filter_value_layout.addWidget(self.filter_value_input)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        apply_btn = QPushButton("تطبيق")
        apply_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #e05d00;
            }}
        """)
        apply_btn.clicked.connect(self.apply_filter)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MEDIUM_BG};
                color: {WHITE};
                border: 1px solid {LIGHT_BG};
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_BG};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(apply_btn)
        
        # Add widgets to layout
        dialog_layout.addWidget(scroll_area)
        dialog_layout.addSpacing(15)
        dialog_layout.addLayout(filter_value_layout)
        dialog_layout.addSpacing(15)
        dialog_layout.addLayout(buttons_layout)
    
    def apply_filter(self):
        # Get selected columns
        selected_columns = []
        for column, checkbox in self.filter_checkboxes.items():
            if checkbox.isChecked():
                selected_columns.append(column)
        
        # Get filter value
        filter_value = self.filter_value_input.text().strip()
        
        # Emit signal with filter data
        self.filterApplied.emit(selected_columns, filter_value)
        
        # Close the dialog
        self.accept()

class FormationManagementSystem(QMainWindow):
    def __init__(self):
        """
        Initialize the main application window and set up the UI components
        """
        super().__init__()
        self.setWindowTitle("نظام إدارة الموارد البشرية - إدارة التكوين")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set up the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create main content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Create main page
        self.main_page = QWidget()
        self.main_page_layout = QVBoxLayout(self.main_page)
        self.main_page_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create action bar with Filter button and Add button
        self.create_action_bar()
        
        # Create table and buttons
        self.create_table()
        self.create_action_buttons()
        
        self.stacked_widget.addWidget(self.main_page)
        
        # Add content to main layout
        self.main_layout.addWidget(self.content_widget)
        
        # Show main page by default
        self.stacked_widget.setCurrentIndex(0)
        
        # Sample data
        self.load_sample_data()
        
        # Initialize filter state
        self.selected_filter_columns = []
        
        # Get current date for validation
        self.today = QDate.currentDate()
        
        # Initialize form windows
        self.add_form_window = None
        self.edit_form_window = None
        self.history_window = None

    def create_action_bar(self):
        """
        Create the action bar with Filter button and Add button
        """
        action_bar = QWidget()
        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(0, 0, 0, 15)  # Add margin at bottom
        
        # Filter button with title
        filter_container = QWidget()
        filter_container_layout = QHBoxLayout(filter_container)
        filter_container_layout.setContentsMargins(0, 0, 0, 0)
        filter_container_layout.setSpacing(5)
        
        filter_title = QLabel("ترشيح")

        filter_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        filter_btn = QPushButton()
        filter_btn.setFixedSize(35, 35)
        filter_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MEDIUM_BG};
                border: none;
                border-radius: 17px;
                color: {WHITE};
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_BG};
            }}
        """)
        filter_icon = QPixmap("pics/filter.png")
        if not filter_icon.isNull():
            filter_icon = filter_icon.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        filter_btn = QPushButton()
        filter_btn.setIcon(QIcon(filter_icon))
        filter_btn.setIconSize(QSize(20, 20))
        filter_btn.setToolTip("ترشيح")
        filter_btn.clicked.connect(self.show_filter_dialog)

        
        filter_container_layout.addWidget(filter_title)
        filter_container_layout.addWidget(filter_btn)
        
        # Add button
        add_btn = QPushButton("إضافة")
        add_btn.setFixedSize(160, 45)  # Smaller size
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE};
                color: {WHITE};
                border: none;
                border-radius: 10px;  /* Rounded corners as requested */
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #e05d00;
            }}
        """)
        add_btn.clicked.connect(self.show_add_formation_form)
        
        # Add widgets to layout - filter on left, add on right
        action_layout.addWidget(filter_container)
        action_layout.addStretch()
        action_layout.addWidget(add_btn)
        
        self.main_page_layout.addWidget(action_bar)

    def show_filter_dialog(self):
        """
        Show the filter dialog with checkboxes for column selection
        """
        # Create columns list
        columns = [
            "السنة", "رقم الموظف", "الإسم", "اللقب", "نوع التكوين", 
            "تاريخ البدء", "تاريخ الإنتهاء", "مدة التكوين", "مؤسسة التكوين"
        ]
        
        # Create and show filter dialog
        filter_dialog = FilterDialog(self, columns)
        filter_dialog.filterApplied.connect(self.apply_filter)
        filter_dialog.exec_()

    def apply_filter(self, selected_columns, filter_value):
        """
        Apply the filter to the table based on selected columns and input value
        """
        # Store selected columns
        self.selected_filter_columns = selected_columns
        
        if not filter_value or not selected_columns:
            # Reset filter if no value or no columns selected
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)
            return
        
        # Get column indices for selected columns
        column_indices = []
        for col_name in selected_columns:
            for col_idx in range(self.table.columnCount()):
                if self.table.horizontalHeaderItem(col_idx).text() == col_name:
                    column_indices.append(col_idx)
        
        # Apply filter
        for row in range(self.table.rowCount()):
            row_visible = False
            
            # Check if any selected column contains the filter value
            for col_idx in column_indices:
                cell_value = self.table.item(row, col_idx).text().lower()
                if filter_value.lower() in cell_value:
                    row_visible = True
                    break
            
            self.table.setRowHidden(row, not row_visible)

    def create_table(self):
        """
        Create the main data table with all columns
        """
        # Table container
        table_container = QWidget()
        table_container.setStyleSheet(f"background-color: {MEDIUM_BG}; border-radius: 10px;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create table
        self.table = QTableWidget()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {MEDIUM_BG};
                color: {WHITE};
                border: none;
                gridline-color: {LIGHT_BG};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {LIGHT_BG};
            }}
            QTableWidget::item:selected {{
                background-color: {ORANGE};
                color: {WHITE};
            }}
             QHeaderView::section {{
                background-color: {DARKER_BG};
                color: {WHITE};
                padding: 8px;  /* Increased padding */
                border: none;
                font-weight: bold;
                text-align: center;
            }}
            QScrollBar {{
                width: 0px;
                height: 0px;
            }}
        """)
        
        # Set up columns
        columns = [
            "السنة", "رقم الموظف", "الإسم", "اللقب", "نوع التكوين", 
            "تاريخ البدء", "تاريخ الإنتهاء", "مدة التكوين", "مؤسسة التكوين", "محتوى التكوين"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Make columns resizable and movable - FIXED: Force Interactive mode
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        for i in range(len(columns)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
        
        # Allow moving columns
        self.table.horizontalHeader().setSectionsMovable(True)
        # Set column resizing fixed
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        # Enable movable sections - FIXED: Explicitly enable this
        self.table.horizontalHeader().setSectionsMovable(True)
        self.table.horizontalHeader().setDragEnabled(True)
        self.table.horizontalHeader().setDragDropMode(QTableWidget.InternalMove)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Set column widths - FIXED: Set explicit widths
        self.table.setColumnWidth(0, 80)   # Year
        self.table.setColumnWidth(1, 100)  # Employee ID
        self.table.setColumnWidth(2, 120)  # First name
        self.table.setColumnWidth(3, 120)  # Last name
        self.table.setColumnWidth(4, 100)  # Training type
        self.table.setColumnWidth(5, 120)  # Start date
        self.table.setColumnWidth(6, 120)  # End date
        self.table.setColumnWidth(7, 100)  # Duration
        self.table.setColumnWidth(8, 150)  # Institution
        
        # Set text alignment for all columns to right-aligned
        for i in range(len(columns)):
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Add table to layout
        table_layout.addWidget(self.table)
        self.main_page_layout.addWidget(table_container)

    def create_action_buttons(self):
        """
        Create action buttons for edit, delete, and history
        All buttons have the same size
        """
        # Buttons container
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 20, 0, 0)
        buttons_layout.setSpacing(25)
        
        # Create buttons
        edit_btn = QPushButton("تعديل")
        delete_btn = QPushButton("حذف")
        history_btn = QPushButton("سجل الأنشطة")
        
        # Style buttons - all with the same fixed size
        for btn in [edit_btn, delete_btn, history_btn]:
            btn.setFixedSize(160, 45)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ORANGE};
                    color: {WHITE};
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #e05d00;
                }}
                QPushButton:pressed {{
                    background-color: #cc5200;
                }}
            """)
        
        # Connect buttons to actions
        edit_btn.clicked.connect(self.show_edit_form)
        delete_btn.clicked.connect(self.show_delete_dialog)
        history_btn.clicked.connect(self.show_history_window)
        
        # Add buttons to layout - right to left for Arabic
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(history_btn)
        
        self.main_page_layout.addWidget(buttons_widget)

    def show_add_formation_form(self):
        """
        Show the add formation form in a separate window
        """
        # Create and show add formation form window
        self.add_form_window = FormationFormWindow(self, "إضافة تكوين")
        self.add_form_window.formSaved.connect(self.save_new_formation_from_window)
        self.add_form_window.show()

    def save_new_formation_from_window(self, formation_data):
        """
        Save a new formation from the form window data
        """
        # Add new row to table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        for col, value in enumerate(formation_data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_position, col, item)
            
        # Log the action
        self.log_action("إضافة", f"إضافة تكوين جديد للموظف رقم {formation_data[1]}")
        
        # Show success message using custom dialog
        info_dialog = CustomInfoDialog(self, "نجاح", "تم إضافة التكوين بنجاح")
        info_dialog.exec_()

    def show_edit_form(self):
        """
        Show the edit form in a separate window with selected row data
        """
        # Check if a row is selected
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            warning_dialog = CustomWarningDialog(self, "تحذير", "الرجاء اختيار تكوين للتعديل")
            warning_dialog.exec_()
            return
        
        # Get selected row data
        row = selected_rows[0].row()
        row_data = []
        
        for col in range(self.table.columnCount()):
            row_data.append(self.table.item(row, col).text())
        
        # Create and show edit form window
        self.edit_form_window = FormationFormWindow(self, "تعديل تكوين", row_data)
        self.edit_form_window.formSaved.connect(lambda data: self.save_edited_formation(row, data))
        self.edit_form_window.show()

    def save_edited_formation(self, row, formation_data):
        """
        Save changes to an existing formation from the form window
        """
        # Update existing row
        for col, value in enumerate(formation_data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, col, item)
            
        # Log the action
        self.log_action("تعديل", f"تعديل تكوين للموظف رقم {formation_data[1]}")
        
        # Show success message using custom dialog
        info_dialog = CustomInfoDialog(self, "نجاح", "تم تعديل التكوين بنجاح")
        info_dialog.exec_()

    def show_delete_dialog(self):
        """
        Show confirmation dialog for deleting a formation
        """
        # Check if a row is selected
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            warning_dialog = CustomWarningDialog(self, "تحذير", "الرجاء اختيار تكوين للحذف")
            warning_dialog.exec_()
            return
        
        # Use CustomMessageBox instead of DeleteConfirmationDialog
        delete_dialog = CustomMessageBox(self, "حذف تكوين", "هل أنت متأكد أنك تريد حذف هذه التكوين ؟")
        # Connect the accept signal to delete_formation
        delete_dialog.accepted.connect(lambda: self.delete_formation(selected_rows[0].row()))
        delete_dialog.exec_()

    def delete_formation(self, row):
        """
        Delete a formation from the table
        Removes the selected row and logs the action
        """
        # Get employee ID for logging
        employee_id = self.table.item(row, 1).text()
        
        # Remove the row
        self.table.removeRow(row)
        
        # Log the action
        self.log_action("حذف", f"حذف تكوين للموظف رقم {employee_id}")
        
        # Show success message using custom dialog
        info_dialog = CustomInfoDialog(self, "نجاح", "تم حذف التكوين بنجاح")
        info_dialog.exec_()

    def show_history_window(self):
        """
        Show the history window
        """
        # Create and show history window
        self.history_window = HistoryWindow(self)
        self.history_window.show()

    def log_action(self, action_type, details):
        """
        Log user actions for auditing purposes
        In a real application, this would save to a database
        """
        # In a real application, this would save to a database
        # For this example, we'll just print to console
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        user = "اسم المستخدم"  # This would come from the logged-in user
        
        print(f"Action logged: {timestamp} | {user} | {action_type} | {details}")

    def load_sample_data(self):
        """
        Load sample data into the table for demonstration
        """
        # Sample data for the table
        sample_data = [
            ["2025", "1001", "محمد", "أحمد", "تقني", "2025-01-15", "2025-02-15", "30 يوم", "معهد التكوين", "تطوير البرمجيات"],
            ["2025", "1002", "أحمد", "علي", "إداري", "2025-02-10", "2025-03-10", "30 يوم", "مركز التدريب", "إدارة الموارد البشرية"],
            ["2025", "1003", "فاطمة", "محمد", "تقني", "2025-03-05", "2025-04-05", "30 يوم", "معهد التكوين", "قواعد البيانات"],
            ["2025", "1004", "سارة", "أحمد", "إداري", "2025-04-01", "2025-05-01", "30 يوم", "مركز التدريب", "إدارة المشاريع"],
            ["2025", "1005", "علي", "محمود", "تقني", "2025-05-15", "2025-06-15", "30 يوم", "معهد التكوين", "أمن المعلومات"]
        ]
        
        self.table.setRowCount(len(sample_data))
        
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, col, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide font for Arabic support
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Set right-to-left layout for Arabic
    app.setLayoutDirection(Qt.RightToLeft)
    
    window = FormationManagementSystem()
    window.show()
    
    sys.exit(app.exec_())