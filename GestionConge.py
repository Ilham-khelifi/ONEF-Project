import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QTableWidget, 
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, 
                            QFrame, QDialog, QMessageBox, QCheckBox, QComboBox, QDateEdit,
                            QScrollArea, QSizePolicy, QStackedWidget, QToolButton, QMenu,
                            QListWidget, QListWidgetItem, QGridLayout, QSpinBox, QHeaderView)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize, QDate, QTimer, QLocale

# Import from external files
from ui_constants import *  # Import color themes
from sidebar import create_sidebar, create_top_bar  # Import sidebar and topbar functions
from custom_dialogs import CustomWarningDialog, CustomInfoDialog, CustomMessageBox  # Import custom dialogs


class AddLeaveDialog(QDialog):
    """
    Dialog for adding a new leave
    """
    def __init__(self, parent=None, employee_id="", employee_name=""):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("إضافة عطلة")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set window flags to allow maximize/minimize
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a centered container for the form
        center_container = QWidget()
        center_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout = QHBoxLayout(center_container)
        
        # Form container with fixed width
        form_container_wrapper = QWidget()
        form_container_wrapper.setFixedWidth(500)
        form_wrapper_layout = QVBoxLayout(form_container_wrapper)
        form_wrapper_layout.setContentsMargins(20, 20, 20, 20)
        form_wrapper_layout.setSpacing(15)
        
        # Title
        self.title_label = QLabel(f"إضافة عطلة - {employee_name} ({employee_id})")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet(f"background-color: {MEDIUM_BG}; border-radius: 10px;")
        
        container_layout = QVBoxLayout(form_container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Form fields
        fields = [
            {"name": "رقم القرار", "type": "text", "placeholder": "أدخل رقم القرار"},
            {"name": "تاريخ القرار", "type": "date"},
            {"name": "تاريخ البداية", "type": "date"},
            {"name": "تاريخ النهاية", "type": "date"}
        ]
        
        self.form_fields = {}
        
        for field in fields:
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)
            
            label = QLabel(field["name"])
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            
            if field["type"] == "date":
                input_field = QDateEdit()
                input_field.setCalendarPopup(True)
                input_field.setDate(QDate.currentDate())
                
                # Set standard date format
                input_field.setDisplayFormat("yyyy-MM-dd")
                
                input_field.setStyleSheet(f"""
                    QDateEdit {{
                        background-color: {DARKER_BG};
                        border: none;
                        border-radius: 5px;
                        padding: 8px;
                        color: {WHITE};
                        font-size: 13px;
                        text-align: right;
                    }}
                """)
                input_field.setLayoutDirection(Qt.RightToLeft)  # Set text direction to RTL
                
                # Connect date fields to calculate period automatically
                if field["name"] == "تاريخ البداية" or field["name"] == "تاريخ النهاية":
                    input_field.dateChanged.connect(self.calculate_leave_days)
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
                input_field.setLayoutDirection(Qt.RightToLeft)  # Set text direction to RTL
                input_field.setAlignment(Qt.AlignRight)  # Align text to right for Arabic
            
            field_layout.addWidget(label)
            field_layout.addWidget(input_field)
            container_layout.addLayout(field_layout)
            
            self.form_fields[field["name"]] = input_field
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Save button - حفظ
        save_btn = QPushButton("حفظ")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {GREEN};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #3d8b40;
            }}
        """)
        
        # Cancel button - إلغاء
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {RED};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #d32f2f;
            }}
        """)
        
        # Connect buttons
        save_btn.clicked.connect(self.save_leave)
        cancel_btn.clicked.connect(self.reject)
        
        # Add buttons in right-to-left order for Arabic
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        container_layout.addLayout(buttons_layout)
        
        # Add to form wrapper layout
        form_wrapper_layout.addWidget(self.title_label)
        form_wrapper_layout.addWidget(form_container)
        
        # Add form wrapper to center layout
        center_layout.addStretch()
        center_layout.addWidget(form_container_wrapper)
        center_layout.addStretch()
        
        # Add center container to main layout
        main_layout.addWidget(center_container)
        
        # Store calculated days
        self.calculated_days = 0
        
        # Store employee data
        self.employee_id = employee_id
        self.employee_name = employee_name
    
    def calculate_leave_days(self):
        """
        Calculate the leave days automatically based on start and end dates
        """
        # Check if both date fields exist in the form
        if "تاريخ البداية" in self.form_fields and "تاريخ النهاية" in self.form_fields:
            start_date = self.form_fields["تاريخ البداية"].date()
            end_date = self.form_fields["تاريخ النهاية"].date()
            
            # Calculate the difference in days
            days_diff = start_date.daysTo(end_date) + 1  # Include both start and end days
            
            # Store the calculated days for later use
            self.calculated_days = max(0, days_diff)
    
    def validate_form(self):
        """
        Validate the form fields
        """
        # Check required fields
        required_fields = ["رقم القرار"]
        
        for field_name in required_fields:
            field = self.form_fields[field_name]
            if isinstance(field, QLineEdit) and not field.text().strip():
                warning = CustomWarningDialog(self, "تحذير", f"الرجاء إدخال {field_name}")
                warning.exec_()
                field.setFocus()
                return False
                
        # Validate date range
        start_date = self.form_fields["تاريخ البداية"].date()
        end_date = self.form_fields["تاريخ النهاية"].date()
        
        if start_date > end_date:
            warning = CustomWarningDialog(self, "تحذير", "تاريخ البداية يجب أن يكون قبل تاريخ النهاية")
            warning.exec_()
            return False
            
        return True
    
    def save_leave(self):
        """
        Save the leave data and return it to the parent
        """
        if not self.validate_form():
            return
        
        # Get form data
        decision_id = self.form_fields["رقم القرار"].text()
        decision_date = self.form_fields["تاريخ القرار"].date().toString("yyyy-MM-dd")
        start_date = self.form_fields["تاريخ البداية"].date().toString("yyyy-MM-dd")
        end_date = self.form_fields["تاريخ النهاية"].date().toString("yyyy-MM-dd")
        
        # Create data dictionary to return
        leave_data = {
            "decision_id": decision_id,
            "decision_date": decision_date,
            "start_date": start_date,
            "end_date": end_date,
            "days": self.calculated_days
        }
        
        # Set the result and accept the dialog
        self.leave_data = leave_data
        self.accept()

class EditTrancheDialog(QDialog):
    """
    Dialog for editing a tranche
    """
    def __init__(self, parent=None, tranche_data=None, tranche_index=0):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("تعديل الشطر")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set window flags to allow maximize/minimize
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Store tranche data
        self.tranche_data = tranche_data or {}
        self.tranche_index = tranche_index
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a centered container for the form
        center_container = QWidget()
        center_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout = QHBoxLayout(center_container)
        
        # Form container with fixed width
        form_container_wrapper = QWidget()
        form_container_wrapper.setFixedWidth(500)
        form_wrapper_layout = QVBoxLayout(form_container_wrapper)
        form_wrapper_layout.setContentsMargins(20, 20, 20, 20)
        form_wrapper_layout.setSpacing(15)
        
        # Title
        self.title_label = QLabel(f"تعديل الشطر {tranche_index + 1}")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet(f"background-color: {MEDIUM_BG}; border-radius: 10px;")
        
        container_layout = QVBoxLayout(form_container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Form fields
        fields = [
            {"name": "رقم القرار", "type": "text", "placeholder": "أدخل رقم القرار"},
            {"name": "تاريخ القرار", "type": "date"},
            {"name": "تاريخ البداية", "type": "date"},
            {"name": "تاريخ النهاية", "type": "date"}
        ]
        
        self.form_fields = {}
        
        for field in fields:
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)
            
            label = QLabel(field["name"])
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            
            if field["type"] == "date":
                input_field = QDateEdit()
                input_field.setCalendarPopup(True)
                input_field.setDate(QDate.currentDate())
                
                # Set standard date format
                input_field.setDisplayFormat("yyyy-MM-dd")
                
                input_field.setStyleSheet(f"""
                    QDateEdit {{
                        background-color: {DARKER_BG};
                        border: none;
                        border-radius: 5px;
                        padding: 8px;
                        color: {WHITE};
                        font-size: 13px;
                        text-align: right;
                    }}
                """)
                input_field.setLayoutDirection(Qt.RightToLeft)  # Set text direction to RTL
                
                # Connect date fields to calculate period automatically
                if field["name"] == "تاريخ البداية" or field["name"] == "تاريخ النهاية":
                    input_field.dateChanged.connect(self.calculate_tranche_days)
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
                input_field.setLayoutDirection(Qt.RightToLeft)  # Set text direction to RTL
                input_field.setAlignment(Qt.AlignRight)  # Align text to right for Arabic
            
            field_layout.addWidget(label)
            field_layout.addWidget(input_field)
            container_layout.addLayout(field_layout)
            
            self.form_fields[field["name"]] = input_field
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Save button - حفظ
        save_btn = QPushButton("حفظ")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {GREEN};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #3d8b40;
            }}
        """)
        
        # Cancel button - إلغاء
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {RED};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #d32f2f;
            }}
        """)
        
        # Connect buttons
        save_btn.clicked.connect(self.save_tranche)
        cancel_btn.clicked.connect(self.reject)
        
        # Add buttons in right-to-left order for Arabic
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        container_layout.addLayout(buttons_layout)
        
        # Add to form wrapper layout
        form_wrapper_layout.addWidget(self.title_label)
        form_wrapper_layout.addWidget(form_container)
        
        # Add form wrapper to center layout
        center_layout.addStretch()
        center_layout.addWidget(form_container_wrapper)
        center_layout.addStretch()
        
        # Add center container to main layout
        main_layout.addWidget(center_container)
        
        # Store calculated days
        self.calculated_tranche_days = 0
        
        # Fill form with tranche data
        self.fill_form()
    
    def fill_form(self):
        """
        Fill the form with tranche data
        """
        if "رقم القرار" in self.form_fields:
            self.form_fields["رقم القرار"].setText(self.tranche_data.get("decision_id", ""))
            
        if "تاريخ القرار" in self.form_fields:
            decision_date = QDate.fromString(self.tranche_data.get("decision_date", ""), "yyyy-MM-dd")
            if decision_date.isValid():
                self.form_fields["تاريخ القرار"].setDate(decision_date)
            else:
                self.form_fields["تاريخ القرار"].setDate(QDate.currentDate())
                
        if "تاريخ البداية" in self.form_fields:
            start_date = QDate.fromString(self.tranche_data.get("start_date", ""), "yyyy-MM-dd")
            if start_date.isValid():
                self.form_fields["تاريخ البداية"].setDate(start_date)
            else:
                self.form_fields["تاريخ البداية"].setDate(QDate.currentDate())
                
        if "تاريخ النهاية" in self.form_fields:
            end_date = QDate.fromString(self.tranche_data.get("end_date", ""), "yyyy-MM-dd")
            if end_date.isValid():
                self.form_fields["تاريخ النهاية"].setDate(end_date)
            else:
                self.form_fields["تاريخ النهاية"].setDate(QDate.currentDate())
        
        # Calculate days
        self.calculate_tranche_days()
    
    def calculate_tranche_days(self):
        """
        Calculate the tranche days automatically based on start and end dates
        """
        # Check if both date fields exist in the form
        if "تاريخ البداية" in self.form_fields and "تاريخ النهاية" in self.form_fields:
            start_date = self.form_fields["تاريخ البداية"].date()
            end_date = self.form_fields["تاريخ النهاية"].date()
            
            # Calculate the difference in days
            days_diff = start_date.daysTo(end_date) + 1  # Include both start and end days
            
            # Store the calculated days for later use
            self.calculated_tranche_days = max(0, days_diff)
    
    def validate_form(self):
        """
        Validate the form fields
        """
        # Check required fields
        required_fields = ["رقم القرار"]
        
        for field_name in required_fields:
            field = self.form_fields[field_name]
            if isinstance(field, QLineEdit) and not field.text().strip():
                warning = CustomWarningDialog(self, "تحذير", f"الرجاء إدخال {field_name}")
                warning.exec_()
                field.setFocus()
                return False
                
        # Validate date range
        start_date = self.form_fields["تاريخ البداية"].date()
        end_date = self.form_fields["تاريخ النهاية"].date()
        
        if start_date > end_date:
            warning = CustomWarningDialog(self, "تحذير", "تاريخ البداية يجب أن يكون قبل تاريخ النهاية")
            warning.exec_()
            return False
            
        return True
    
    def save_tranche(self):
        """
        Save the tranche data and return it to the parent
        """
        if not self.validate_form():
            return
        
        # Get form data
        decision_id = self.form_fields["رقم القرار"].text()
        decision_date = self.form_fields["تاريخ القرار"].date().toString("yyyy-MM-dd")
        start_date = self.form_fields["تاريخ البداية"].date().toString("yyyy-MM-dd")
        end_date = self.form_fields["تاريخ النهاية"].date().toString("yyyy-MM-dd")
        
        # Create data dictionary to return
        tranche_data = {
            "decision_id": decision_id,
            "decision_date": decision_date,
            "start_date": start_date,
            "end_date": end_date,
            "days": self.calculated_tranche_days
        }
        
        # Set the result and accept the dialog
        self.tranche_data = tranche_data
        self.accept()

class LeaveDetailsDialog(QDialog):
    """
    Dialog for showing leave details
    """
    def __init__(self, parent=None, leave_id="", employee_data=None, tranches=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("تفاصيل العطلة")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")

        # Set window flags to allow maximize/minimize
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Store data
        self.leave_id = leave_id
        self.employee_data = employee_data or {}
        self.tranches = tranches or []
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a centered container for the content
        center_container = QWidget()
        center_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(15)

        # Add top bar from sidebar.py
        top_bar = create_top_bar(self, center_layout, None)
        center_layout.insertWidget(0, top_bar)

        # Title
        title_label = QLabel("جدول تفاصيل العطلة")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Tranche details table
        tranche_container = QWidget()
        tranche_container.setStyleSheet(f"background-color: {MEDIUM_BG}; border-radius: 10px;")
        tranche_layout = QVBoxLayout(tranche_container)
        tranche_layout.setContentsMargins(15, 15, 15, 15)
        
        self.tranche_table = QTableWidget()
        self.tranche_table.setStyleSheet(f"""
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
                padding: 8px;
                border: none;
                font-weight: bold;
                text-align: center;
            }}
            QScrollBar {{
                width: 0px;
                height: 0px;
            }}
        """)
        
        # Set up columns for tranche table
        tranche_columns = [
            "رقم العطلة", "رقم الموظف", "لقب الموظف", "اسم الموظف", 
            "رقم الشطر", "رقم القرار", "تاريخ القرار", "تاريخ البداية", "تاريخ النهاية"
        ]
        
        self.tranche_table.setColumnCount(len(tranche_columns))
        self.tranche_table.setHorizontalHeaderLabels(tranche_columns)
        self.tranche_table.horizontalHeader().setStretchLastSection(True)
        self.tranche_table.verticalHeader().setVisible(False)
        self.tranche_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set text alignment for all columns to center-aligned
        for i in range(len(tranche_columns)):
            self.tranche_table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
        
        # Connect double-click signal to edit tranche
        self.tranche_table.cellDoubleClicked.connect(self.edit_tranche)
        
        tranche_layout.addWidget(self.tranche_table)
        
        # Allow moving columns
        self.tranche_table.horizontalHeader().setSectionsMovable(True)
        # Set column resizing fixed
        self.tranche_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Action buttons at the bottom
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(15)
        
        edit_btn = QPushButton("تعديل")
        delete_btn = QPushButton("حذف")
        
        for btn in [edit_btn, delete_btn]:
            btn.setFixedSize(120, 40)
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
            """)
        
        # Make delete button red
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {RED};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #d32f2f;
            }}
        """)
        
        # Connect buttons
        edit_btn.clicked.connect(self.edit_selected_tranche)
        delete_btn.clicked.connect(self.delete_selected_tranche)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()
        
        # Add all widgets to the center layout
        center_layout.addWidget(title_label)
        center_layout.addWidget(tranche_container)
        center_layout.addWidget(buttons_widget)
        
        # Add center container to main layout
        main_layout.addWidget(center_container)
        
        # Populate table with tranche data
        self.populate_table()
    
    def populate_table(self):
        """
        Populate the table with tranche data
        """
        # Clear existing rows
        self.tranche_table.setRowCount(0)
        
        # Add rows for each tranche
        for i, tranche in enumerate(self.tranches):
            # Add a new row
            row_idx = self.tranche_table.rowCount()
            self.tranche_table.insertRow(row_idx)
            
            # Set data for each column
            self.tranche_table.setItem(row_idx, 0, QTableWidgetItem(self.leave_id))
            self.tranche_table.setItem(row_idx, 1, QTableWidgetItem(self.employee_data.get("employee_id", "")))
            self.tranche_table.setItem(row_idx, 2, QTableWidgetItem(self.employee_data.get("last_name", "")))
            self.tranche_table.setItem(row_idx, 3, QTableWidgetItem(self.employee_data.get("first_name", "")))
            self.tranche_table.setItem(row_idx, 4, QTableWidgetItem(f"الشطر {i+1}"))
            self.tranche_table.setItem(row_idx, 5, QTableWidgetItem(tranche.get("decision_id", "")))
            self.tranche_table.setItem(row_idx, 6, QTableWidgetItem(tranche.get("decision_date", "")))
            self.tranche_table.setItem(row_idx, 7, QTableWidgetItem(tranche.get("start_date", "")))
            self.tranche_table.setItem(row_idx, 8, QTableWidgetItem(tranche.get("end_date", "")))
            
            # Center align all items in the row
            for col in range(self.tranche_table.columnCount()):
                item = self.tranche_table.item(row_idx, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
    
    def edit_tranche(self, row, column):
        """
        Edit a tranche when double-clicked
        """
        self.edit_selected_tranche(row)
    
    def edit_selected_tranche(self, row=None):
        """
        Edit the selected tranche
        """
        if row is None:
            selected_rows = self.tranche_table.selectionModel().selectedRows()
            if not selected_rows:
                warning = CustomWarningDialog(self, "تحذير", "الرجاء اختيار شطر للتعديل")
                warning.exec_()
                return
            row = selected_rows[0].row()
        
        # Get tranche data
        tranche_data = {}
        for col in range(self.tranche_table.columnCount()):
            header = self.tranche_table.horizontalHeaderItem(col).text()
            if self.tranche_table.item(row, col):
                value = self.tranche_table.item(row, col).text()
                
                # Map column headers to data keys
                if header == "رقم العطلة":
                    tranche_data["leave_id"] = value
                elif header == "رقم الموظف":
                    tranche_data["employee_id"] = value
                elif header == "لقب الموظف":
                    tranche_data["last_name"] = value
                elif header == "اسم الموظف":
                    tranche_data["first_name"] = value
                elif header == "رقم الشطر":
                    tranche_data["tranche_number"] = value
                elif header == "رقم القرار":
                    tranche_data["decision_id"] = value
                elif header == "تاريخ القرار":
                    tranche_data["decision_date"] = value
                elif header == "تاريخ البداية":
                    tranche_data["start_date"] = value
                elif header == "تاريخ النهاية":
                    tranche_data["end_date"] = value
        
        # Open edit dialog
        edit_dialog = EditTrancheDialog(self, tranche_data, row)
        if edit_dialog.exec_() == QDialog.Accepted:
            # Update tranche data
            updated_data = edit_dialog.tranche_data
            
            # Update table
            self.tranche_table.setItem(row, 5, QTableWidgetItem(updated_data.get("decision_id", "")))
            self.tranche_table.setItem(row, 6, QTableWidgetItem(updated_data.get("decision_date", "")))
            self.tranche_table.setItem(row, 7, QTableWidgetItem(updated_data.get("start_date", "")))
            self.tranche_table.setItem(row, 8, QTableWidgetItem(updated_data.get("end_date", "")))
            
            # Center align all updated items
            for col in [5, 6, 7, 8]:
                item = self.tranche_table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
            
            # Update tranches list
            self.tranches[row].update(updated_data)
            
            # Notify parent of the change
            self.parent.update_tranche(row, updated_data)
    
    def delete_selected_tranche(self):
        """
        Delete the selected tranche
        """
        selected_rows = self.tranche_table.selectionModel().selectedRows()
        if not selected_rows:
            warning = CustomWarningDialog(self, "تحذير", "الرجاء اختيار شطر للحذف")
            warning.exec_()
            return
        
        row = selected_rows[0].row()
        
        # Show confirmation dialog
        dialog = CustomMessageBox(
            self,
            "حذف الشطر",
            "هل أنت متأكد أنك تريد حذف هذا الشطر؟"
        )
        
        if dialog.exec_() == QDialog.Accepted:
            # Remove the row from the tranche table
            self.tranche_table.removeRow(row)
            
            # Remove from tranches list
            del self.tranches[row]
            
            # Notify parent of the deletion
            self.parent.delete_tranche(row)
            
            # Show success message
            info = CustomInfoDialog(self, "نجاح", f"تم حذف الشطر {row+1} بنجاح")
            info.exec_()

class HistoryDialog(QDialog):
    """
    Dialog for showing activity history
    """
    def __init__(self, parent=None, history_data=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("سجل الأنشطة")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set window flags to allow maximize/minimize
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Store data
        self.history_data = history_data or []
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a centered container for the content
        center_container = QWidget()
        center_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(15)
        
        # Add top bar from sidebar.py
        top_bar = create_top_bar(self, center_layout, None)
        center_layout.insertWidget(0, top_bar)

        # Title
        title_label = QLabel("سجل الأنشطة على إدارة الإجازات")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Create a container for the table to center it
        table_container = QWidget()
        table_container.setStyleSheet(f"background-color: {MEDIUM_BG}; border-radius: 10px;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # History table
        history_table = QTableWidget()
        history_table.setStyleSheet(f"""
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
                text-align: center;
            }}
            QScrollBar {{
                width: 0px;
                height: 0px;
            }}
        """)
        
        # Set up columns
        columns = ["التاريخ", "المستخدم", "التصرف", "التفاصيل"]
        
        history_table.setColumnCount(len(columns))
        history_table.setHorizontalHeaderLabels(columns)
        
        # Set equal column widths
        for i in range(len(columns)):
            history_table.setColumnWidth(i, 200)
        
        history_table.verticalHeader().setVisible(False)
        
        # Set text alignment for all columns to center-aligned
        for i in range(len(columns)):
            history_table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
        
        # Add sample data
        history_table.setRowCount(len(self.history_data))
        
        for row, data in enumerate(self.history_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                history_table.setItem(row, col, item)
        
        # Add table to container
        table_layout.addWidget(history_table)
        
        # Add all widgets to the center layout
        center_layout.addWidget(title_label)
        center_layout.addWidget(table_container)
        
        # Add center container to main layout
        main_layout.addWidget(center_container)

class PreviousYearsDialog(QDialog):
    """
    Dialog for showing previous years data
    """
    def __init__(self, parent=None, previous_years_data=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("عطلات السنوات السابقة")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set window flags to allow maximize/minimize
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Store data
        self.previous_years_data = previous_years_data or []
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a centered container for the content
        center_container = QWidget()
        center_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(15)
        
        top_bar = create_top_bar(self, center_layout, None)
        center_layout.insertWidget(0, top_bar)
        # Title
        title_label = QLabel("جدول تفاصيل عطلات السنوات السابقة")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Table container
        table_container = QWidget()
        table_container.setStyleSheet(f"background-color: {MEDIUM_BG}; border-radius: 10px;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # Previous years table
        previous_years_table = QTableWidget()
        previous_years_table.setStyleSheet(f"""
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
                text-align: center;
            }}
            QScrollBar {{
                width: 0px;
                height: 0px;
            }}
        """)
        
        # Set up columns for previous years table
        columns = [
            "رقم العطلة", "السنة", "رقم الموظف", "لقب الموظف", "اسم الموظف", 
            "عدد الأيام المستحقة", "الشطر 1", "الشطر 2", "الشطر 3", "الشطر 4", "الشطر 5",
            "عدد الأيام المستهلكة", "عدد الأيام المتبقية"
        ]
        
        previous_years_table.setColumnCount(len(columns))
        previous_years_table.setHorizontalHeaderLabels(columns)
        previous_years_table.horizontalHeader().setStretchLastSection(True)
        previous_years_table.verticalHeader().setVisible(False)
        
        # Set text alignment for all columns to center-aligned
        for i in range(len(columns)):
            previous_years_table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
        
        # Add data to table
        previous_years_table.setRowCount(len(self.previous_years_data))
        
        for row, data in enumerate(self.previous_years_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                previous_years_table.setItem(row, col, item)
        
        # Add table to container
        table_layout.addWidget(previous_years_table)
        
        # Add all widgets to the center layout
        center_layout.addWidget(title_label)
        center_layout.addWidget(table_container)
        
        # Allow moving columns
        previous_years_table.horizontalHeader().setSectionsMovable(True)
        # Set column resizing fixed
        previous_years_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Add center container to main layout
        main_layout.addWidget(center_container)

class LeaveManagementSystem(QMainWindow):
    def __init__(self):
        """
        Initialize the main application window and set up the UI components
        """
        super().__init__()
        self.setWindowTitle("نظام إدارة الموارد البشرية - إدارة الإجازات")
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
        
        # Create main page
        self.main_page = QWidget()
        self.main_page_layout = QVBoxLayout(self.main_page)
        self.main_page_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create action bar with Filter button and Add button
        self.create_action_bar()
        
        # Add title for the main table
        self.create_table_title()
        
        # Create table and buttons
        self.create_table()
        self.create_action_buttons()
        
        # Add main page to content layout
        self.content_layout.addWidget(self.main_page)
        
        # Add content to main layout
        self.main_layout.addWidget(self.content_widget)
        
        # Sample data
        self.load_sample_data()
        
        # Initialize filter state
        self.filter_dialog = None
        self.selected_filter_columns = []
        
        # Get current date for validation
        self.today = QDate.currentDate()
        
        # Current selected tranche for editing
        self.current_tranche_index = -1
        self.current_leave_id = -1
        
        # Store tranches data for each leave
        self.leave_tranches = {}
        
        # History data
        self.history_data = [
            ["2025-04-10 14:30", "أحمد محمد", "إضافة", "إضافة عطلة جديدة للموظف رقم 1001"],
            ["2025-04-09 10:15", "سارة أحمد", "تعديل", "تعديل عطلة للموظف رقم 1002"],
            ["2025-04-08 16:45", "محمد علي", "حذف", "حذف عطلة للموظف رقم 1003"],
            ["2025-04-07 09:30", "فاطمة محمد", "إضافة", "إضافة عطلة جديدة للموظف رقم 1004"],
            ["2025-04-06 11:20", "أحمد محمد", "تعديل", "تعديل عطلة للموظف رقم 1005"]
        ]

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
                border-radius: 10px;  
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #e05d00;
            }}
        """)
        add_btn.clicked.connect(self.show_add_leave_form)
        
        # Add widgets to layout - filter on left, add on right
        action_layout.addWidget(filter_container)
        action_layout.addStretch()
        action_layout.addWidget(add_btn)
        
        self.main_page_layout.addWidget(action_bar)

    def create_table_title(self):
        """
        Create a title for the main table
        """
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 10)
        
        # Create title label
        title_label = QLabel("تفاصيل جدول الإجازات")
        title_label.setStyleSheet(f"""
            color: {WHITE};
            font-size: 18px;
            font-weight: bold;
        """)
        title_label.setLayoutDirection(Qt.RightToLeft)
        title_layout.addWidget(title_label)
        
        self.main_page_layout.addWidget(title_container)

    def show_filter_dialog(self):
        """
        Show the filter dialog with checkboxes for column selection
        """
        # Create filter dialog if it doesn't exist
        if not self.filter_dialog:
            self.filter_dialog = QDialog(self)
            self.filter_dialog.setWindowTitle("ترشيح")
            self.filter_dialog.setFixedWidth(350)
            self.filter_dialog.setStyleSheet(f"background-color: {MEDIUM_BG}; color: {WHITE};")
            
            dialog_layout = QVBoxLayout(self.filter_dialog)
            dialog_layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title_label = QLabel("اختر الأعمدة للترشيح:")
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
            dialog_layout.addWidget(title_label)
            
            # Create checkboxes for each column
            columns = [
                "السنة", "رقم الموظف", "الإسم", "اللقب", "عدد الأيام المستحقة", 
                "الشطر 1", "الشطر 2", "الشطر 3", "الشطر 4", "الشطر 5",
                "عدد الأيام المستهلكة", "عدد الأيام المتبقية"
            ]
            
            self.filter_checkboxes = {}
            
            for column in columns:
                checkbox = QCheckBox(column)
                checkbox.setStyleSheet(f"""
                    QCheckBox {{
                        font-size: 14px;
                        padding: 8px 0;  /* Increased spacing between items */
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
                dialog_layout.addWidget(checkbox)
                self.filter_checkboxes[column] = checkbox
            
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
            self.filter_value_input.setLayoutDirection(Qt.RightToLeft)  # Set text direction to RTL
            
            filter_value_layout.addWidget(filter_value_label)
            filter_value_layout.addWidget(self.filter_value_input)
            
            dialog_layout.addSpacing(15)
            dialog_layout.addLayout(filter_value_layout)
            
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
            cancel_btn.clicked.connect(self.filter_dialog.reject)
            
            # Add buttons in right-to-left order for Arabic
            buttons_layout.addWidget(cancel_btn)
            buttons_layout.addWidget(apply_btn)
            
            dialog_layout.addSpacing(15)
            dialog_layout.addLayout(buttons_layout)
        
        # Show the dialog
        self.filter_dialog.exec_()

    def apply_filter(self):
        """
        Apply the filter to the table based on selected columns and input value
        """
        # Get selected columns
        self.selected_filter_columns = []
        for column, checkbox in self.filter_checkboxes.items():
            if checkbox.isChecked():
                self.selected_filter_columns.append(column)
        
        # Get filter value
        filter_value = self.filter_value_input.text().strip().lower()
        
        if not filter_value or not self.selected_filter_columns:
            # Reset filter if no value or no columns selected
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)
            self.filter_dialog.accept()
            return
        
        # Get column indices for selected columns
        column_indices = []
        for col_name in self.selected_filter_columns:
            for col_idx in range(self.table.columnCount()):
                if self.table.horizontalHeaderItem(col_idx).text() == col_name:
                    column_indices.append(col_idx)
        
        # Apply filter
        for row in range(self.table.rowCount()):
            row_visible = False
            
            # Check if any selected column contains the filter value
            for col_idx in column_indices:
                cell_value = self.table.item(row, col_idx).text().lower()
                if filter_value in cell_value:
                    row_visible = True
                    break
            
            self.table.setRowHidden(row, not row_visible)
        
        # Close the dialog
        self.filter_dialog.accept()

    def create_table(self):
        """
        Create the main data table with all columns
        """
        # Table container
        table_container = QWidget()
        table_container.setStyleSheet(f"background-color: {MEDIUM_BG}; border-radius: 10px;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(15, 15, 15, 15)  # Increased margins
        
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
                padding: 8px;  /* Increased padding */
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
        
        # Set up columns - UPDATED ORDER with 5th tranche
        columns = [
            "رقم العطلة", "السنة", "رقم الموظف", "لقب الموظف", "اسم الموظف", 
            "عدد الأيام المستحقة", "الشطر 1", "الشطر 2", "الشطر 3", "الشطر 4", "الشطر 5",
            "عدد الأيام المستهلكة", "عدد الأيام المتبقية"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Make entitled days column editable, others read-only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Set column widths
        for i in range(len(columns)):
            self.table.setColumnWidth(i, 120)
        
        # Set text alignment for all columns to center-aligned
        for i in range(len(columns)):
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
        
        # To move the columns
        self.table.horizontalHeader().setSectionsMovable(True)
        #Set column resizing fixed
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        
        # Connect double-click signal to edit entitled days
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)
        
        # Add table to layout
        table_layout.addWidget(self.table)
        self.main_page_layout.addWidget(table_container)

    def handle_cell_double_click(self, row, column):
        """
        Handle double-click on table cells
        Only allow editing of the entitled days column (index 5)
        """
        if column == 5:  # عدد الأيام المستحقة column
            # Create a temporary line edit for in-place editing
            current_value = self.table.item(row, column).text()
            line_edit = QLineEdit(current_value)
            line_edit.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {WHITE};
                    color: {BLACK};
                    border: none;
                    padding: 2px;
                }}
            """)
            
            # Connect editing finished signal
            line_edit.editingFinished.connect(lambda: self.finish_entitled_days_edit(row, column, line_edit))
            
            # Set the line edit as the cell widget
            self.table.setCellWidget(row, column, line_edit)
            line_edit.setFocus()
            line_edit.selectAll()

    def finish_entitled_days_edit(self, row, column, line_edit):
        """
        Finish editing entitled days and update related fields
        """
        # Get the new value
        new_value = line_edit.text()
        
        # Validate that it's a number
        if not new_value.isdigit():
            warning = CustomWarningDialog(self, "تحذير", "يجب أن يكون عدد الأيام المستحقة رقمًا")
            warning.exec_()
            new_value = "0"
        
        # Update the cell
        self.table.removeCellWidget(row, column)
        self.table.setItem(row, column, QTableWidgetItem(new_value))
        
        # Center align the new item
        item = self.table.item(row, column)
        if item:
            item.setTextAlignment(Qt.AlignCenter)
        
        # Update remaining days
        self.update_leave_days(row)

    def update_leave_days(self, row):
        """
        Update consumed and remaining days based on tranches
        """
        # Get entitled days
        entitled_item = self.table.item(row, 5)
        entitled_days = int(entitled_item.text()) if entitled_item and entitled_item.text().isdigit() else 0
        
        # Calculate consumed days from tranches
        consumed_days = 0
        for i in range(5):  # Now 5 tranches
            tranche_col = 6 + i  # Tranche columns start at index 6
            tranche_item = self.table.item(row, tranche_col)
            if tranche_item and tranche_item.text().isdigit():
                consumed_days += int(tranche_item.text())
        
        # Update consumed days (column 11)
        consumed_item = QTableWidgetItem(str(consumed_days))
        consumed_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 11, consumed_item)
        
        # Update remaining days (column 12)
        remaining_days = entitled_days - consumed_days
        remaining_item = QTableWidgetItem(str(remaining_days))
        remaining_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 12, remaining_item)

    def create_action_buttons(self):
        """
        Create action buttons for view details, previous years, and activity log
        All buttons have the same size
        """
        # Buttons container
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 20, 0, 0)  # Increased top margin
        buttons_layout.setSpacing(25)  # Increased spacing
        
        # Create buttons - REMOVED DELETE BUTTON as requested
        view_details_btn = QPushButton("عرض التفاصيل")
        previous_years_btn = QPushButton("عرض تفاصيل السنوات السابقة")
        history_btn = QPushButton("سجل الأنشطة")
        
        # Style buttons - all with the same fixed size
        for btn in [view_details_btn, previous_years_btn, history_btn]:
            btn.setFixedSize(160, 45)  # Same fixed size for all buttons
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
                QPushButton:disabled {{
                    background-color: #a0a0a0;
                    color: #e0e0e0;
                }}
            """)
        
        # Connect buttons to actions
        view_details_btn.clicked.connect(self.show_leave_details)
        previous_years_btn.clicked.connect(self.show_previous_years)
        history_btn.clicked.connect(self.show_history)
        
        # Add buttons to layout - right to left for Arabic
        buttons_layout.addWidget(view_details_btn)
        buttons_layout.addWidget(previous_years_btn)
        buttons_layout.addWidget(history_btn)
        
        self.main_page_layout.addWidget(buttons_widget)

    def show_add_leave_form(self):
        """
        Show the add leave form dialog
        """
        # Check if a row is selected
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            warning = CustomWarningDialog(self, "تحذير", "الرجاء اختيار موظف لإضافة عطلة")
            warning.exec_()
            return
            
        # Get selected row data
        row = selected_rows[0].row()
        
        # Get employee data
        employee_id = self.table.item(row, 2).text()
        employee_name = f"{self.table.item(row, 4).text()} {self.table.item(row, 3).text()}"
        
        # Check if employee has already used all 5 tranches
        leave_id = self.table.item(row, 0).text()
        tranches_used = 0
        for i in range(5):
            tranche_col = 6 + i
            tranche_value = self.table.item(row, tranche_col).text()
            if tranche_value != "0":
                tranches_used += 1
        
        if tranches_used >= 5:
            warning = CustomWarningDialog(self, "تحذير", "لا يمكن إضافة عطلة جديدة. تم استخدام جميع الأشطر الخمسة المتاحة.")
            warning.exec_()
            return
        
        # Store the selected row for later use
        self.selected_row = row
        
        # Create and show add leave dialog
        add_dialog = AddLeaveDialog(self, employee_id, employee_name)
        if add_dialog.exec_() == QDialog.Accepted:
            # Get leave data
            leave_data = add_dialog.leave_data
            
            # Find first empty tranche
            for i in range(5):
                tranche_col = 6 + i
                tranche_value = self.table.item(row, tranche_col).text()
                if tranche_value == "0":
                    # Update tranche with the calculated days
                    tranche_item = QTableWidgetItem(str(leave_data["days"]))
                    tranche_item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row, tranche_col, tranche_item)
                    
                    # Store tranche data
                    if leave_id not in self.leave_tranches:
                        self.leave_tranches[leave_id] = []
                    
                    self.leave_tranches[leave_id].append({
                        "decision_id": leave_data["decision_id"],
                        "decision_date": leave_data["decision_date"],
                        "start_date": leave_data["start_date"],
                        "end_date": leave_data["end_date"],
                        "days": leave_data["days"]
                    })
                    
                    # Update consumed and remaining days
                    self.update_leave_days(row)
                    
                    # Log the action
                    self.log_action("إضافة", f"إضافة عطلة جديدة للموظف رقم {employee_id}")
                    
                    # Show success message
                    info = CustomInfoDialog(self, "نجاح", "تم إضافة العطلة بنجاح")
                    info.exec_()
                    
                    break

    def show_leave_details(self):
        """
        Show the leave details dialog
        """
        # Check if a row is selected
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            warning = CustomWarningDialog(self, "تحذير", "الرجاء اختيار عطلة لعرض التفاصيل")
            warning.exec_()
            return
        
        # Get selected row data
        row = selected_rows[0].row()
        
        # Get leave ID
        leave_id = self.table.item(row, 0).text()
        
        # Get employee data
        employee_data = {
            "employee_id": self.table.item(row, 2).text(),
            "last_name": self.table.item(row, 3).text(),
            "first_name": self.table.item(row, 4).text()
        }
        
        # Get tranches data
        tranches = []
        if leave_id in self.leave_tranches:
            tranches = self.leave_tranches[leave_id]
        else:
            # Create dummy tranches data if not available
            for i in range(5):
                tranche_col = 6 + i
                tranche_value = self.table.item(row, tranche_col).text()
                if tranche_value != "0":
                    tranches.append({
                        "decision_id": f"2025/{100+i}",
                        "decision_date": f"2025-0{i+1}-01",
                        "start_date": f"2025-0{i+1}-01",
                        "end_date": f"2025-0{i+1}-{15+i}",
                        "days": tranche_value
                    })
            
            # Store tranches data
            self.leave_tranches[leave_id] = tranches
        
        # Create and show leave details dialog
        details_dialog = LeaveDetailsDialog(self, leave_id, employee_data, tranches)
        details_dialog.exec_()

    def show_previous_years(self):
        """
        Show the previous years dialog
        """
        # Create and show previous years dialog
        previous_years_dialog = PreviousYearsDialog(self, self.previous_years_data)
        previous_years_dialog.exec_()

    def show_history(self):
        """
        Show the history dialog
        """
        # Create and show history dialog
        history_dialog = HistoryDialog(self, self.history_data)
        history_dialog.exec_()

    def update_tranche(self, tranche_index, tranche_data):
        """
        Update a tranche in the main table
        """
        # Get the selected row in the main table
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        row = selected_rows[0].row()
        
        # Update the tranche column in the main table
        tranche_col = 6 + tranche_index  # Tranche columns start at index 6
        days = tranche_data["days"]
        tranche_item = QTableWidgetItem(str(days))
        tranche_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, tranche_col, tranche_item)
        
        # Update consumed and remaining days
        self.update_leave_days(row)
        
        # Log the action
        leave_id = self.table.item(row, 0).text()
        self.log_action("تعديل", f"تعديل الشطر {tranche_index + 1} للعطلة رقم {leave_id}")

    def delete_tranche(self, tranche_index):
        """
        Delete a tranche from the main table
        """
        # Get the selected row in the main table
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        row = selected_rows[0].row()
        
        # Update the tranche column to empty
        tranche_col = 6 + tranche_index  # Tranche columns start at index 6
        empty_item = QTableWidgetItem("0")
        empty_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, tranche_col, empty_item)
        
        # Update consumed and remaining days
        self.update_leave_days(row)
        
        # Log the action
        leave_id = self.table.item(row, 0).text()
        self.log_action("حذف", f"حذف الشطر {tranche_index+1} للعطلة رقم {leave_id}")

    def log_action(self, action_type, details):
        """
        Log user actions for auditing purposes
        """
        # Create timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        user = "اسم المستخدم"  # This would come from the logged-in user
        
        # Add to history data
        self.history_data.insert(0, [timestamp, user, action_type, details])
        
        # Print to console for debugging
        print(f"Action logged: {timestamp} | {user} | {action_type} | {details}")

    def load_sample_data(self):
        """
        Load sample data into the table for demonstration
        """
        # Sample data for the table - UPDATED with 5th tranche column
        sample_data = [
            ["1", "2025", "1001", "أحمد", "محمد", "30", "15", "0", "0", "0", "0", "15", "15"],
            ["2", "2025", "1002", "علي", "أحمد", "25", "10", "10", "0", "0", "0", "20", "5"],
            ["3", "2025", "1003", "محمد", "فاطمة", "28", "14", "0", "0", "0", "0", "14", "14"],
            ["4", "2025", "1004", "أحمد", "سارة", "30", "10", "10", "5", "5", "0", "30", "0"],
            ["5", "2025", "1005", "محمود", "علي", "25", "0", "0", "0", "0", "0", "0", "25"]
        ]
        
        # Sample data for previous years - UPDATED with 5th tranche column
        self.previous_years_data = [
            ["101", "2024", "1001", "أحمد", "محمد", "30", "10", "10", "5", "5", "0", "30", "0"],
            ["102", "2024", "1002", "علي", "أحمد", "25", "10", "5", "5", "0", "0", "20", "5"],
            ["103", "2024", "1003", "محمد", "فاطمة", "28", "10", "8", "5", "5", "0", "28", "0"],
            ["104", "2023", "1001", "أحمد", "محمد", "30", "10", "10", "5", "0", "0", "25", "5"],
            ["105", "2023", "1002", "علي", "أحمد", "25", "10", "5", "5", "5", "0", "25", "0"]
        ]
        
        # Load data into main table
        self.table.setRowCount(len(sample_data))
        
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide font for Arabic support
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Set right-to-left layout for Arabic
    app.setLayoutDirection(Qt.RightToLeft)
    
    window = LeaveManagementSystem()
    window.show()
    
    sys.exit(app.exec_())