import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, 
                            QFrame, QToolButton)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from ui_constants import *

# This function will be exported and used by other modules
def create_sidebar(parent, main_layout, active_module=None, on_module_change=None):
    print("Sidebar function imported and running!")
    """
    Create the sidebar with user profile and navigation menu
    
    Parameters:
    - parent: The parent widget that will contain the sidebar
    - main_layout: The main layout where the sidebar will be added
    -active_module: The name of the currently active module
    - on_module_change: Callback function to call when a module is selected
    
    Returns:
    - sidebar: The sidebar widget
    - sidebar_toggle: The toggle button for the sidebar
    """
    # Sidebar container
    sidebar = QWidget()
    sidebar.setFixedWidth(220)
    sidebar.setStyleSheet(f"""
        background-color: {MEDIUM_BG};
        color: {WHITE};
        border: none;
    """)
    
    sidebar_layout = QVBoxLayout(sidebar)
    sidebar_layout.setContentsMargins(0, 0, 0, 0)
    sidebar_layout.setSpacing(0)
    
    # User profile section
    profile_widget = QWidget()
    profile_widget.setStyleSheet(f"background-color: {MEDIUM_BG};")
    profile_layout = QVBoxLayout(profile_widget)
    
    # User avatar with user_icon.png
    avatar_label = QLabel()
    user_icon_pixmap = QPixmap("pics/user_icon.png")
    
    # Scale the user icon to fit the avatar size
    user_icon_pixmap = user_icon_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    avatar_label.setPixmap(user_icon_pixmap)
    avatar_label.setStyleSheet(f"""
        border-radius: 25px;
        min-height: 50px;
        max-height: 50px;
        min-width: 50px;
        max-width: 50px;
        margin: 10px auto;
        background-color: transparent;
    """)
    
    avatar_label.setAlignment(Qt.AlignCenter)
    
    # User name and role
    user_name = QLabel("اسم المستخدم")
    user_name.setAlignment(Qt.AlignCenter)
    user_name.setStyleSheet("font-weight: bold; font-size: 14px;")
    
    user_role = QLabel("دور المستخدم")
    user_role.setAlignment(Qt.AlignCenter)
    user_role.setStyleSheet("font-size: 12px; color: #d9d9d9;")
    
    profile_layout.addWidget(avatar_label, 0, Qt.AlignCenter)
    profile_layout.addWidget(user_name)
    profile_layout.addWidget(user_role)
    
    # Add separator line between user profile and menu items
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    separator.setStyleSheet(f"background-color: {LIGHT_BG}; max-height: 1px; margin: 10px 15px;")
    
    # Menu items
    menu_widget = QWidget()
    menu_layout = QVBoxLayout(menu_widget)
    menu_layout.setContentsMargins(10, 20, 10, 10)
    menu_layout.setSpacing(20)  # Increased spacing between menu items
    
    # Create a header for "الوظائف الأساسية" (Basic Functions)
    header_layout = QHBoxLayout()
    header_layout.setSpacing(10)
    
    # Create the icon label for header - Load image from pics folder
    header_icon = QLabel()
    # Try to load the header icon image
    header_pixmap = QPixmap("pics/main.png")
  
    # If image loaded successfully, scale it to appropriate size
    header_pixmap = header_pixmap.scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    header_icon.setPixmap(header_pixmap)
    
    header_icon.setAlignment(Qt.AlignCenter)
    header_icon.setFixedWidth(40)  # Fixed width for icon container
    
    # Create the header label
    header_label = QLabel("الوظائف الأساسية")
    header_label.setStyleSheet(f"""
        color: {WHITE};
        font-size: 18px;  /* Increased font size */
        font-weight: bold;
        padding: 12px;
    """)
    
    # Add widgets to layout - icon on left, label on right
    header_layout.addWidget(header_icon)
    header_layout.addWidget(header_label)
    header_layout.addStretch()
    
    menu_layout.addLayout(header_layout)
    
    # Create menu items with icons on the left side
    # Define menu items with their text and corresponding icon paths
    menu_items = [
        {"text": "إدارة الموظفين", "icon": "pics/employee.png"},
        {"text": "إدارة الإجازات", "icon": "pics/conge.png"},
        {"text": "إدارة الغيابات", "icon": "pics/abs.png"},
        {"text": "إدارة التقييمات", "icon": "pics/note.png"},  
        {"text": "إدارة التكوين", "icon": "pics/form.png"},
        {"text": "صفحة الأرشيف", "icon": "pics/arch.png"},
        {"text": "إدارة الحسابات", "icon": "pics/Vector.png"}
    ]
    
    sidebar.buttons = {}

    # Loop through each menu item to create buttons with icons
    for item in menu_items:
        # Create a horizontal layout for each menu item
        btn_layout = QHBoxLayout()
        
        
        # Create the icon label with an image from pics folder
        icon_label = QLabel()
        # Try to load the icon image
        pixmap = QPixmap(item["icon"])
        if not pixmap.isNull():
            # If image loaded successfully, scale it to appropriate size
            pixmap = pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        else:
            # If image failed to load, use a text fallback and print error
            icon_label.setText("?")
            print(f"Failed to load icon: {item['icon']}")
        
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedWidth(40)  # Fixed width for icon container
        
        # Check if this item is the active module
        is_active = (active_module == item["text"]) 
        # Create the button with text
        btn = QPushButton(item["text"])
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE if is_active else "transparent"};
                color: {WHITE};
                border: none;
                text-align: right;
                padding: 10px;
                padding-right: 3px;  /* Reduced right padding to bring text closer to icon */
                font-size: 18px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {ORANGE if is_active else LIGHT_BG};
            }}
        """)
        
        # Connect button to module change callback if provided
        if on_module_change:
            btn.clicked.connect(lambda checked, module=item["text"]: on_module_change(module))
        
        # Store the button in the sidebar's buttons dictionary
        sidebar.buttons[item["text"]] = btn

        # Add widgets to layout - icon on left, button on right
        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(btn)
        
        menu_layout.addLayout(btn_layout)
    
    # Logout button with icon inside
    logout_btn = QPushButton("تسجيل الخروج")
    logout_icon_pixmap = QPixmap("pics/logout_icon.png")
    
    # Create icon and set it on the button
    logout_icon_pixmap = logout_icon_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    logout_btn.setIcon(QIcon(logout_icon_pixmap))
    logout_btn.setIconSize(QSize(20, 20))
    
    
    # Set the icon position to the left of the text
    logout_btn.setLayoutDirection(Qt.RightToLeft)
    # Add some padding to the left to align the icon
    logout_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {YELLOW_BTN};
            color: {WHITE};
            border: none;
            text-align: center;
            padding: 14px;
            padding-left: 20px;  /* Extra padding for icon */
            font-size: 15px;
            border-radius: 20px;
            margin-top: 30px;
        }}
        QPushButton:hover {{
            background-color: #d4af37;
        }}
    """)
    
    # Add widgets to sidebar layout
    sidebar_layout.addWidget(profile_widget)
    sidebar_layout.addWidget(separator)  # Add the separator line
    sidebar_layout.addWidget(menu_widget)
    sidebar_layout.addStretch()
    sidebar_layout.addWidget(logout_btn, 0, Qt.AlignCenter)
    sidebar_layout.addSpacing(20)
    
    # Add sidebar to main layout
    main_layout.addWidget(sidebar)
    
    # Create sidebar toggle button
    sidebar_visible = True
    sidebar_toggle = QPushButton()
    sidebar_toggle.setFixedSize(30, 30)
    sidebar_toggle.setStyleSheet(f"""
        QPushButton {{
            background-color: {MEDIUM_BG};
            border: none;
            border-radius: 15px;
            color: {WHITE};
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {LIGHT_BG};
        }}
    """)
    
    # Set sidebar toggle icon from pics folder
    toggle_icon = QPixmap("pics/sidebar_icon.png")
    if not toggle_icon.isNull():
        # If image loaded successfully, create QIcon and set it on the button
        toggle_icon = toggle_icon.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        sidebar_toggle.setIcon(QIcon(toggle_icon))
        sidebar_toggle.setIconSize(QSize(20, 20))
    else:
        # If image failed to load, use a text fallback and print error
        sidebar_toggle.setText("≡")
        print("Failed to load sidebar toggle icon: pics/sidebar_icon.png")
    
    # Connect toggle button to toggle function
    def toggle_sidebar():
        nonlocal sidebar_visible
        if sidebar_visible:
            sidebar.hide()
        else:
            sidebar.show()
        sidebar_visible = not sidebar_visible
        # Force layout update
        QApplication.processEvents()
    
    sidebar_toggle.clicked.connect(toggle_sidebar)
    
    # Add method to update active module
    def update_active_module(module_name):
        # Update all buttons
        for name, btn in sidebar.buttons.items():
            is_active = (name == module_name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ORANGE if is_active else 'transparent'};
                    color: {WHITE};
                    border: none;
                    text-align: right;
                    padding: 10px;
                    padding-right: 3px;
                    font-size: 18px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {ORANGE if is_active else LIGHT_BG};
                }}
            """)
    # Attach the method to the sidebar
    sidebar.update_active_module = update_active_module
    
    return sidebar, sidebar_toggle

def create_top_bar(parent, content_layout, sidebar_toggle):
    """
    Create the top bar with action buttons and search functionality
    
    Parameters:
    - parent: The parent widget that will contain the top bar
    - content_layout: The layout where the top bar will be added
    - sidebar_toggle: The sidebar toggle button to be added to the top bar
    
    Returns:
    - top_bar: The top bar widget
    """
    top_bar = QWidget()
    top_bar.setFixedHeight(60)
    top_bar.setStyleSheet(f"background-color: {DARK_BG}; border-bottom: 1px solid {LIGHT_BG};")
    
    top_layout = QHBoxLayout(top_bar)
    top_layout.setContentsMargins(15, 10, 15, 10)  
    
    # Right side - action buttons 
    right_widget = QWidget()
    right_layout = QHBoxLayout(right_widget)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(20)  # Increased spacing
    
    # Export button with icon
    export_btn = QToolButton()
    export_btn.setFixedSize(35, 35)  # Increased size
    export_btn.setStyleSheet(f"""
        QToolButton {{
            background-color: transparent;
            border: none;
            color: {WHITE};
            font-size: 16px;
        }}
        QToolButton:hover {{
            background-color: {LIGHT_BG};
            border-radius: 17px;
        }}
    """)
    
    # Load export icon from pics folder
    export_icon = QPixmap("pics/export.png")
    if not export_icon.isNull():
        export_icon = export_icon.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        export_btn.setIcon(QIcon(export_icon))
        export_btn.setIconSize(QSize(20, 20))
    else:
        export_btn.setText("↓")
        print("Failed to load export icon: pics/export.png")
    
    export_btn.setToolTip("تصدير")
    
    # Print button with icon
    print_btn = QToolButton()
    print_btn.setFixedSize(35, 35)  # Increased size
    print_btn.setStyleSheet(f"""
        QToolButton {{
            background-color: transparent;
            border: none;
            color: {WHITE};
            font-size: 16px;
        }}
        QToolButton:hover {{
            background-color: {LIGHT_BG};
            border-radius: 17px;
        }}
    """)
    
    # Load print icon from pics folder
    print_icon = QPixmap("pics/imprime.png")
    if not print_icon.isNull():
        print_icon = print_icon.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        print_btn.setIcon(QIcon(print_icon))
        print_btn.setIconSize(QSize(20, 20))
    else:
        print_btn.setText("🖨️")
        print("Failed to load print icon: pics/imprime.png")
    
    print_btn.setToolTip("طباعة")
    
    # Notification button with icon
    notif_btn = QToolButton()
    notif_btn.setFixedSize(35, 35)  # Increased size
    notif_btn.setStyleSheet(f"""
        QToolButton {{
            background-color: transparent;
            border: none;
            color: {WHITE};
            font-size: 16px;
        }}
        QToolButton:hover {{
            background-color: {LIGHT_BG};
            border-radius: 17px;
        }}
    """)
    
    # Load notification icon from pics folder
    notif_icon = QPixmap("pics/notification_icon.png")
    if not notif_icon.isNull():
        notif_icon = notif_icon.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        notif_btn.setIcon(QIcon(notif_icon))
        notif_btn.setIconSize(QSize(20, 20))
    else:
        notif_btn.setText("🔔")
        print("Failed to load notification icon: pics/notification_icon.png")
    
    notif_btn.setToolTip("إشعارات")
    
    right_layout.addWidget(export_btn)
    right_layout.addWidget(print_btn)
    right_layout.addWidget(notif_btn)
    
    # Center - search bar
    search_widget = QWidget()
    search_layout = QHBoxLayout(search_widget)
    search_layout.setContentsMargins(0, 0, 0, 0)
    
    search_bar = QLineEdit()
    search_bar.setPlaceholderText("بحث...")
    search_bar.setStyleSheet(f"""
        QLineEdit {{
            background-color: #e3e3e3;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 14px;
            color: {BLACK};
            text-align: right;
        }}
    """)
    search_bar.setMinimumWidth(300)
    search_bar.setLayoutDirection(Qt.RightToLeft)  # Set text direction to RTL
    
    employee_dropdown = QPushButton("بحث")
    employee_dropdown.setStyleSheet(f"""
        QPushButton {{
            background-color: {MEDIUM_BG};
            color: {WHITE};
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 14px;
            text-align: center;
        }}
        QPushButton:hover {{
            background-color: {LIGHT_BG};
        }}
    """)
    
    search_layout.addWidget(search_bar)
    search_layout.addWidget(employee_dropdown)
    
    # Add sidebar toggle to top bar (left side)
    top_layout.addWidget(sidebar_toggle)
    top_layout.addStretch()
    top_layout.addWidget(search_widget)
    top_layout.addStretch()
    top_layout.addWidget(right_widget)  # Now on the right side
    
    content_layout.addWidget(top_bar)
    
    return top_bar

# Helper function to get absolute path to pics folder
def get_pics_path():
    """
    Returns the absolute path to the pics folder
    This is useful if your script is run from different locations
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Join with the pics folder name
    pics_path = os.path.join(script_dir, "pics")
    return pics_path

class SidebarTopbarDemo(QMainWindow):
    def __init__(self):
        """
        Initialize the main application window and set up the UI components
        """
        super().__init__()
        self.setWindowTitle("Sidebar and Topbar Demo")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {WHITE};")
        
        # Set up the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create sidebar using the exported function
        self.sidebar, self.sidebar_toggle = create_sidebar(self, self.main_layout)
        
        # Create main content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Create top bar using the exported function
        self.top_bar = create_top_bar(self, self.content_layout, self.sidebar_toggle)
        
        # Add a placeholder for the main content
        main_content = QWidget()
        main_content.setStyleSheet(f"background-color: {DARK_BG}; margin: 20px;")
        main_content_layout = QVBoxLayout(main_content)
        
        content_placeholder = QLabel("Main Content Area")
        content_placeholder.setAlignment(Qt.AlignCenter)
        content_placeholder.setStyleSheet(f"""
            background-color: {MEDIUM_BG};
            color: {WHITE};
            border-radius: 10px;
            padding: 50px;
            font-size: 24px;
        """)
        main_content_layout.addWidget(content_placeholder)
        
        self.content_layout.addWidget(main_content)
        
        # Add content to main layout
        self.main_layout.addWidget(self.content_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide font for Arabic support
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Set right-to-left layout for Arabic
    app.setLayoutDirection(Qt.RightToLeft)
    
    # Print the expected pics folder path to help with debugging
    print(f"Looking for icons in: {get_pics_path()}")
    
    window = SidebarTopbarDemo()
    window.show()
    
    sys.exit(app.exec_())
