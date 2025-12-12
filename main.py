import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget, 
                            QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Import UI constants
from ui_constants import *

# Import sidebar module
from sidebar import create_sidebar, create_top_bar

# Import management modules
from GestionFormation import FormationManagementSystem
from GestionConge import LeaveManagementSystem

class HRMSMainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the main application window that contains all modules
        """
        super().__init__()
        self.setWindowTitle("نظام إدارة الموارد البشرية")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set up the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create sidebar with active module tracking
        self.sidebar, self.sidebar_toggle = create_sidebar(
            self, 
            self.main_layout, 
            active_module="إدارة الموظفين",
            on_module_change=self.switch_module
        )
        
        # Create main content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Create top bar
        self.top_bar = create_top_bar(self, self.content_layout, self.sidebar_toggle)
        
        # Create stacked widget to hold different modules
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Initialize modules
        self.initialize_modules()
        
        # Add content to main layout
        self.main_layout.addWidget(self.content_widget)
    
    def initialize_modules(self):
        """
        Initialize all modules and add them to the stacked widget
        """
        """
    Initialize all modules and add them to the stacked widget
    """
        # Create instances of each module without parent_container parameter
        self.formation_module = FormationManagementSystem()
        self.leave_module = LeaveManagementSystem()
        
        # Add modules to stacked widget
        self.stacked_widget.addWidget(self.formation_module)
        self.stacked_widget.addWidget(self.leave_module)
        
        # Show first module by default
        self.stacked_widget.setCurrentIndex(0)
        
    def switch_module(self, module_name):
        """
        Switch to the specified module
        
        Parameters:
        - module_name: The name of the module to switch to
        """

        self.sidebar.update_active_module(module_name)

        # Map module names to their indices in the stacked widget
        module_indices = {
            #"إدارة الموظفين": 0,  # You can add this module later
            "إدارة التكوين": 0,   # Formation Management
            "إدارة الإجازات": 1,   # Leave Management
            # Add more modules as needed
        }
        
        # Switch to the selected module if it exists in the mapping
        if module_name in module_indices:
            self.stacked_widget.setCurrentIndex(module_indices[module_name])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide font for Arabic support
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Set right-to-left layout for Arabic
    app.setLayoutDirection(Qt.RightToLeft)
    
    window = HRMSMainWindow()
    window.show()
    
    sys.exit(app.exec_())