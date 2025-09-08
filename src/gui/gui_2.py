"""
Advanced PyQt5-based GUI for the Image-to-PDF Organizer.

This module provides an enhanced graphical user interface with dark theme,
advanced features, and better user experience using PyQt5.
"""

import os
import sys
from typing import List, Optional, Dict, Any
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLabel, QComboBox,
    QSlider, QCheckBox, QProgressBar, QStatusBar, QMenuBar,
    QAction, QFileDialog, QMessageBox, QSplitter, QGroupBox,
    QSpinBox, QTextEdit, QTabWidget, QFrame, QGridLayout,
    QScrollArea, QSizePolicy, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSize, QRect,
    QPropertyAnimation, QEasingCurve, pyqtProperty
)
from PyQt5.QtGui import (
    QPixmap, QIcon, QPalette, QColor, QFont, QPainter,
    QBrush, QLinearGradient, QDragEnterEvent, QDropEvent
)
from PIL import Image, ImageQt
from src.services.image_handler import ImageHandler
from src.services.pdf_converter import PDFConverter


class DarkTheme:
    """Dark theme color scheme and styles."""
    
    # Color palette
    BACKGROUND = "#1e1e1e"
    SURFACE = "#252526"
    SURFACE_VARIANT = "#2d2d30"
    PRIMARY = "#007acc"
    PRIMARY_VARIANT = "#005a9e"
    SECONDARY = "#3c3c3c"
    TEXT_PRIMARY = "#cccccc"
    TEXT_SECONDARY = "#969696"
    ACCENT = "#f14c4c"
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    ERROR = "#f44336"
    
    @staticmethod
    def apply_dark_theme(app: QApplication) -> None:
        """Apply dark theme to the application."""
        dark_palette = QPalette()
        
        # Window colors
        dark_palette.setColor(QPalette.Window, QColor(DarkTheme.BACKGROUND))
        dark_palette.setColor(QPalette.WindowText, QColor(DarkTheme.TEXT_PRIMARY))
        
        # Base colors for input fields
        dark_palette.setColor(QPalette.Base, QColor(DarkTheme.SURFACE))
        dark_palette.setColor(QPalette.AlternateBase, QColor(DarkTheme.SURFACE_VARIANT))
        
        # Text colors
        dark_palette.setColor(QPalette.Text, QColor(DarkTheme.TEXT_PRIMARY))
        dark_palette.setColor(QPalette.BrightText, QColor("#ffffff"))
        
        # Button colors
        dark_palette.setColor(QPalette.Button, QColor(DarkTheme.SECONDARY))
        dark_palette.setColor(QPalette.ButtonText, QColor(DarkTheme.TEXT_PRIMARY))
        
        # Highlight colors
        dark_palette.setColor(QPalette.Highlight, QColor(DarkTheme.PRIMARY))
        dark_palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        
        # Disabled colors
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(DarkTheme.TEXT_SECONDARY))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(DarkTheme.TEXT_SECONDARY))
        
        app.setPalette(dark_palette)
    
    @staticmethod
    def get_stylesheet() -> str:
        """Get the complete stylesheet for the application."""
        return f"""
        QMainWindow {{
            background-color: {DarkTheme.BACKGROUND};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QWidget {{
            background-color: {DarkTheme.BACKGROUND};
            color: {DarkTheme.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }}
        
        QPushButton {{
            background-color: {DarkTheme.SECONDARY};
            color: {DarkTheme.TEXT_PRIMARY};
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {DarkTheme.SURFACE_VARIANT};
            border-color: {DarkTheme.PRIMARY};
        }}
        
        QPushButton:pressed {{
            background-color: {DarkTheme.PRIMARY};
        }}
        
        QPushButton:disabled {{
            background-color: {DarkTheme.SURFACE};
            color: {DarkTheme.TEXT_SECONDARY};
        }}
        
        QPushButton.primary {{
            background-color: {DarkTheme.PRIMARY};
            color: white;
        }}
        
        QPushButton.primary:hover {{
            background-color: {DarkTheme.PRIMARY_VARIANT};
        }}
        
        QPushButton.danger {{
            background-color: {DarkTheme.ERROR};
            color: white;
        }}
        
        QPushButton.success {{
            background-color: {DarkTheme.SUCCESS};
            color: white;
        }}
        
        QListWidget {{
            background-color: {DarkTheme.SURFACE};
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
            border-radius: 4px;
            padding: 4px;
        }}
        
        QListWidget::item {{
            background-color: transparent;
            color: {DarkTheme.TEXT_PRIMARY};
            border: none;
            padding: 8px;
            border-radius: 2px;
        }}
        
        QListWidget::item:selected {{
            background-color: {DarkTheme.PRIMARY};
            color: white;
        }}
        
        QListWidget::item:hover {{
            background-color: {DarkTheme.SURFACE_VARIANT};
        }}
        
        QComboBox {{
            background-color: {DarkTheme.SURFACE};
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
            border-radius: 4px;
            padding: 4px 8px;
            min-width: 100px;
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: url(down_arrow.png);
            width: 10px;
            height: 10px;
        }}
        
        QSlider::groove:horizontal {{
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
            height: 8px;
            background: {DarkTheme.SURFACE};
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {DarkTheme.PRIMARY};
            border: 1px solid {DarkTheme.PRIMARY_VARIANT};
            width: 18px;
            margin: -2px 0;
            border-radius: 9px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {DarkTheme.PRIMARY_VARIANT};
        }}
        
        QProgressBar {{
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
            border-radius: 4px;
            text-align: center;
            background-color: {DarkTheme.SURFACE};
        }}
        
        QProgressBar::chunk {{
            background-color: {DarkTheme.PRIMARY};
            border-radius: 2px;
        }}
        
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {DarkTheme.SURFACE_VARIANT};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        
        QTabWidget::pane {{
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
            background-color: {DarkTheme.SURFACE};
        }}
        
        QTabBar::tab {{
            background-color: {DarkTheme.SECONDARY};
            color: {DarkTheme.TEXT_PRIMARY};
            padding: 8px 16px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {DarkTheme.PRIMARY};
            color: white;
        }}
        
        QTabBar::tab:hover {{
            background-color: {DarkTheme.SURFACE_VARIANT};
        }}
        
        QTextEdit {{
            background-color: {DarkTheme.SURFACE};
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
            border-radius: 4px;
            padding: 4px;
        }}
        
        QScrollBar:vertical {{
            background-color: {DarkTheme.SURFACE};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {DarkTheme.SECONDARY};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {DarkTheme.SURFACE_VARIANT};
        }}
        
        QStatusBar {{
            background-color: {DarkTheme.SURFACE};
            color: {DarkTheme.TEXT_PRIMARY};
            border-top: 1px solid {DarkTheme.SURFACE_VARIANT};
        }}
        
        QMenuBar {{
            background-color: {DarkTheme.SURFACE};
            color: {DarkTheme.TEXT_PRIMARY};
            border-bottom: 1px solid {DarkTheme.SURFACE_VARIANT};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 8px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {DarkTheme.PRIMARY};
        }}
        
        QMenu {{
            background-color: {DarkTheme.SURFACE};
            color: {DarkTheme.TEXT_PRIMARY};
            border: 1px solid {DarkTheme.SURFACE_VARIANT};
        }}
        
        QMenu::item {{
            padding: 4px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {DarkTheme.PRIMARY};
        }}
        """


class AnimatedButton(QPushButton):
    """A button with hover animations."""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        
    def enterEvent(self, event):
        """Handle mouse enter event with animation."""
        super().enterEvent(event)
        # Add subtle scale animation on hover
        
    def leaveEvent(self, event):
        """Handle mouse leave event."""
        super().leaveEvent(event)


class ImagePreviewWidget(QWidget):
    """Widget for displaying image thumbnails with information."""
    
    def __init__(self, image_path: str, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.thumbnail_size = QSize(120, 120)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        
        # Thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(self.thumbnail_size)
        self.thumbnail_label.setScaledContents(True)
        self.thumbnail_label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {DarkTheme.SURFACE_VARIANT};
                border-radius: 4px;
                background-color: {DarkTheme.SURFACE};
            }}
        """)
        
        # Load and set thumbnail
        self.load_thumbnail()
        
        # File name
        filename = os.path.basename(self.image_path)
        name_label = QLabel(filename)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet(f"color: {DarkTheme.TEXT_PRIMARY}; font-size: 9pt;")
        
        # Image info
        try:
            with Image.open(self.image_path) as img:
                width, height = img.size
                info_text = f"{width}×{height}"
                info_label = QLabel(info_text)
                info_label.setAlignment(Qt.AlignCenter)
                info_label.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY}; font-size: 8pt;")
        except Exception:
            info_label = QLabel("Invalid")
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setStyleSheet(f"color: {DarkTheme.ERROR}; font-size: 8pt;")
        
        layout.addWidget(self.thumbnail_label)
        layout.addWidget(name_label)
        layout.addWidget(info_label)
        
    def load_thumbnail(self):
        """Load and set the thumbnail image."""
        try:
            with Image.open(self.image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create thumbnail
                img.thumbnail((self.thumbnail_size.width(), self.thumbnail_size.height()))
                
                # Convert to QPixmap
                qt_image = ImageQt.ImageQt(img)
                pixmap = QPixmap.fromImage(qt_image)
                
                self.thumbnail_label.setPixmap(pixmap)
                
        except Exception as e:
            # Show error placeholder
            self.thumbnail_label.setText(f"Error:\n{str(e)[:20]}...")
            self.thumbnail_label.setAlignment(Qt.AlignCenter)
            self.thumbnail_label.setStyleSheet(f"""
                QLabel {{
                    color: {DarkTheme.ERROR};
                    background-color: {DarkTheme.SURFACE};
                    border: 2px dashed {DarkTheme.ERROR};
                    border-radius: 4px;
                }}
            """)


class ConversionThread(QThread):
    """Thread for PDF conversion to keep UI responsive."""
    
    progress_updated = pyqtSignal(float)
    conversion_finished = pyqtSignal(str)
    conversion_failed = pyqtSignal(str)
    
    def __init__(self, image_paths: List[str], output_path: str, 
                 page_size: str, compress: bool, quality: int):
        super().__init__()
        self.image_paths = image_paths
        self.output_path = output_path
        self.page_size = page_size
        self.compress = compress
        self.quality = quality
        
    def run(self):
        """Run the conversion in a separate thread."""
        try:
            converter = PDFConverter()
            
            def progress_callback(progress: float):
                self.progress_updated.emit(progress)
            
            converter.convert_images_to_pdf(
                image_paths=self.image_paths,
                output_path=self.output_path,
                page_size=self.page_size,
                compress=self.compress,
                compression_quality=self.quality,
                callback=progress_callback
            )
            
            self.conversion_finished.emit(self.output_path)
            
        except Exception as e:
            self.conversion_failed.emit(str(e))


class BatchProcessDialog(QDialog):
    """Dialog for batch processing settings."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Processing")
        self.setModal(True)
        self.resize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Input folder selection
        input_group = QGroupBox("Input Settings")
        input_layout = QVBoxLayout(input_group)
        
        self.input_folder_label = QLabel("No folder selected")
        input_folder_btn = QPushButton("Select Input Folder")
        input_folder_btn.clicked.connect(self.select_input_folder)
        
        input_layout.addWidget(QLabel("Input Folder:"))
        input_layout.addWidget(self.input_folder_label)
        input_layout.addWidget(input_folder_btn)
        
        # Output settings
        output_group = QGroupBox("Output Settings")
        output_layout = QVBoxLayout(output_group)
        
        self.output_folder_label = QLabel("No folder selected")
        output_folder_btn = QPushButton("Select Output Folder")
        output_folder_btn.clicked.connect(self.select_output_folder)
        
        self.subfolder_check = QCheckBox("Create subfolders for each PDF")
        self.subfolder_check.setChecked(True)
        
        output_layout.addWidget(QLabel("Output Folder:"))
        output_layout.addWidget(self.output_folder_label)
        output_layout.addWidget(output_folder_btn)
        output_layout.addWidget(self.subfolder_check)
        
        # Processing options
        options_group = QGroupBox("Processing Options")
        options_layout = QGridLayout(options_group)
        
        options_layout.addWidget(QLabel("Images per PDF:"), 0, 0)
        self.images_per_pdf = QSpinBox()
        self.images_per_pdf.setRange(1, 1000)
        self.images_per_pdf.setValue(10)
        options_layout.addWidget(self.images_per_pdf, 0, 1)
        
        options_layout.addWidget(QLabel("File naming:"), 1, 0)
        self.naming_combo = QComboBox()
        self.naming_combo.addItems(["Sequential (001, 002, ...)", "Folder name", "Custom prefix"])
        options_layout.addWidget(self.naming_combo, 1, 1)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(input_group)
        layout.addWidget(output_group)
        layout.addWidget(options_group)
        layout.addWidget(button_box)
        
        self.input_folder = ""
        self.output_folder = ""
        
    def select_input_folder(self):
        """Select input folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_folder_label.setText(os.path.basename(folder))
            
    def select_output_folder(self):
        """Select output folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(os.path.basename(folder))


class AdvancedImageToPdfGUI(QMainWindow):
    """Advanced PyQt5-based GUI for Image-to-PDF conversion."""
    
    def __init__(self):
        super().__init__()
        self.image_paths: List[str] = []
        self.recent_files: List[str] = []
        self.conversion_thread: Optional[ConversionThread] = None
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the main user interface."""
        self.setWindowTitle("Image-to-PDF Organizer Pro")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Image management
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Options and preview
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes
        splitter.setSizes([600, 400])
        
        main_layout.addWidget(splitter)
        
    def create_left_panel(self) -> QWidget:
        """Create the left panel with image management."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Images")
        title.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {DarkTheme.TEXT_PRIMARY};")
        
        # Action buttons
        add_btn = AnimatedButton("Add Images")
        add_btn.setProperty("class", "primary")
        add_btn.clicked.connect(self.add_images)
        
        remove_btn = AnimatedButton("Remove")
        remove_btn.setProperty("class", "danger")
        remove_btn.clicked.connect(self.remove_selected_images)
        
        clear_btn = AnimatedButton("Clear All")
        clear_btn.clicked.connect(self.clear_all_images)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        header_layout.addWidget(remove_btn)
        header_layout.addWidget(clear_btn)
        
        # Image list with thumbnails
        self.image_scroll = QScrollArea()
        self.image_scroll.setWidgetResizable(True)
        self.image_scroll.setAcceptDrops(True)
        self.image_scroll.dragEnterEvent = self.drag_enter_event
        self.image_scroll.dropEvent = self.drop_event
        
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout(self.image_container)
        self.image_layout.setAlignment(Qt.AlignTop)
        
        # Drop zone placeholder
        self.drop_zone = QLabel("Drop images here or click 'Add Images'")
        self.drop_zone.setAlignment(Qt.AlignCenter)
        self.drop_zone.setMinimumHeight(200)
        self.drop_zone.setStyleSheet(f"""
            QLabel {{
                border: 2px dashed {DarkTheme.SURFACE_VARIANT};
                border-radius: 8px;
                color: {DarkTheme.TEXT_SECONDARY};
                font-size: 12pt;
                background-color: {DarkTheme.SURFACE};
            }}
        """)
        self.image_layout.addWidget(self.drop_zone)
        
        self.image_scroll.setWidget(self.image_container)
        
        # Reorder buttons
        reorder_layout = QHBoxLayout()
        move_up_btn = QPushButton("↑ Move Up")
        move_down_btn = QPushButton("↓ Move Down")
        
        move_up_btn.clicked.connect(self.move_image_up)
        move_down_btn.clicked.connect(self.move_image_down)
        
        reorder_layout.addWidget(move_up_btn)
        reorder_layout.addWidget(move_down_btn)
        reorder_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addWidget(self.image_scroll)
        layout.addLayout(reorder_layout)
        
        return panel
        
    def create_right_panel(self) -> QWidget:
        """Create the right panel with options and preview."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Tab widget for different sections
        tab_widget = QTabWidget()
        
        # PDF Options tab
        options_tab = self.create_options_tab()
        tab_widget.addTab(options_tab, "PDF Options")
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "Advanced")
        
        # Batch Processing tab
        batch_tab = self.create_batch_tab()
        tab_widget.addTab(batch_tab, "Batch")
        
        # Preview tab
        preview_tab = self.create_preview_tab()
        tab_widget.addTab(preview_tab, "Preview")
        
        # Progress and export
        progress_group = QGroupBox("Export")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        export_btn = AnimatedButton("Export as PDF")
        export_btn.setProperty("class", "primary")
        export_btn.setMinimumHeight(50)
        export_btn.clicked.connect(self.export_pdf)
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(export_btn)
        
        layout.addWidget(tab_widget)
        layout.addWidget(progress_group)
        
        return panel
    
    def create_options_tab(self) -> QWidget:
        """Create the PDF options tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Page size
        size_group = QGroupBox("Page Size")
        size_layout = QVBoxLayout(size_group)
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "LETTER", "LEGAL", "TABLOID", "FIT"])
        size_layout.addWidget(self.page_size_combo)
        
        # Compression
        compression_group = QGroupBox("Compression")
        compression_layout = QVBoxLayout(compression_group)
        
        self.compress_check = QCheckBox("Enable compression")
        self.compress_check.stateChanged.connect(self.toggle_compression)
        
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Quality:"))
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(85)
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        
        self.quality_label = QLabel("85")
        self.quality_label.setMinimumWidth(30)
        
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_label)
        
        compression_layout.addWidget(self.compress_check)
        compression_layout.addLayout(quality_layout)
        
        # Initially disable quality controls
        self.quality_slider.setEnabled(False)
        self.quality_label.setEnabled(False)
        
        layout.addWidget(size_group)
        layout.addWidget(compression_group)
        layout.addStretch()
        
        return tab
    
    def create_advanced_tab(self) -> QWidget:
        """Create the advanced options tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Watermark
        watermark_group = QGroupBox("Watermark (Future Feature)")
        watermark_layout = QVBoxLayout(watermark_group)
        
        watermark_check = QCheckBox("Add watermark")
        watermark_check.setEnabled(False)  # Future feature
        watermark_text = QLabel("Text watermark support coming soon...")
        watermark_text.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY};")
        
        watermark_layout.addWidget(watermark_check)
        watermark_layout.addWidget(watermark_text)
        
        # Metadata
        metadata_group = QGroupBox("PDF Metadata (Future Feature)")
        metadata_layout = QVBoxLayout(metadata_group)
        
        metadata_text = QLabel("Custom PDF metadata support coming soon...")
        metadata_text.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY};")
        
        metadata_layout.addWidget(metadata_text)
        
        layout.addWidget(watermark_group)
        layout.addWidget(metadata_group)
        layout.addStretch()
        
        return tab
    
    def create_batch_tab(self) -> QWidget:
        """Create the batch processing tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        description = QLabel("""
        Batch processing allows you to process multiple folders of images
        automatically, creating separate PDFs for each batch.
        """)
        description.setWordWrap(True)
        description.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY}; margin: 10px;")
        
        batch_btn = AnimatedButton("Configure Batch Processing")
        batch_btn.clicked.connect(self.open_batch_dialog)
        
        layout.addWidget(description)
        layout.addWidget(batch_btn)
        layout.addStretch()
        
        return tab
    
    def create_preview_tab(self) -> QWidget:
        """Create the preview tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Preview area
        self.preview_label = QLabel("No image selected")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(300)
        self.preview_label.setStyleSheet(f"""
            QLabel {{
                border: 1px solid {DarkTheme.SURFACE_VARIANT};
                border-radius: 4px;
                background-color: {DarkTheme.SURFACE};
                color: {DarkTheme.TEXT_SECONDARY};
            }}
        """)
        
        # Image info
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(100)
        self.info_text.setReadOnly(True)
        self.info_text.setPlainText("Select an image to view details...")
        
        layout.addWidget(QLabel("Preview:"))
        layout.addWidget(self.preview_label)
        layout.addWidget(QLabel("Image Information:"))
        layout.addWidget(self.info_text)
        
        return tab
    
    def setup_menu(self):
        """Setup the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        add_action = QAction("Add Images", self)
        add_action.setShortcut("Ctrl+O")
        add_action.triggered.connect(self.add_images)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export PDF", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_pdf)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        batch_action = QAction("Batch Processing", self)
        batch_action.triggered.connect(self.open_batch_dialog)
        tools_menu.addAction(batch_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Setup the status bar."""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
        # Add permanent widgets
        self.image_count_label = QLabel("0 images")
        self.status_bar.addPermanentWidget(self.image_count_label)
    
    def load_settings(self):
        """Load application settings."""
        # Future: Load from QSettings
        pass
    
    def save_settings(self):
        """Save application settings."""
        # Future: Save to QSettings
        pass
    
    def drag_enter_event(self, event: QDragEnterEvent):
        """Handle drag enter events."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def drop_event(self, event: QDropEvent):
        """Handle drop events."""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        valid_files = [f for f in files if ImageHandler.is_valid_image(f)]
        
        if valid_files:
            self.add_images_from_paths(valid_files)
            event.accept()
        else:
            event.ignore()
    
    def add_images(self):
        """Add images through file dialog."""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.tiff *.gif)")
        
        if file_dialog.exec_():
            files = file_dialog.selectedFiles()
            self.add_images_from_paths(files)
    
    def add_images_from_paths(self, paths: List[str]):
        """Add images from file paths."""
        added_count = 0
        
        for path in paths:
            if path not in self.image_paths and ImageHandler.is_valid_image(path):
                self.image_paths.append(path)
                added_count += 1
        
        if added_count > 0:
            self.refresh_image_list()
            self.status_bar.showMessage(f"Added {added_count} images")
            QTimer.singleShot(3000, lambda: self.status_bar.showMessage("Ready"))
    
    def refresh_image_list(self):
        """Refresh the image list display."""
        # Clear existing items
        for i in reversed(range(self.image_layout.count())):
            child = self.image_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        if not self.image_paths:
            # Show drop zone
            self.image_layout.addWidget(self.drop_zone)
        else:
            # Hide drop zone and show images
            self.drop_zone.setParent(None)
            
            for i, path in enumerate(self.image_paths):
                preview_widget = ImagePreviewWidget(path)
                preview_widget.mousePressEvent = lambda event, p=path: self.select_image_for_preview(p)
                self.image_layout.addWidget(preview_widget)
        
        # Update status
        self.image_count_label.setText(f"{len(self.image_paths)} images")
    
    def select_image_for_preview(self, image_path: str):
        """Select an image for preview."""
        try:
            # Load image for preview
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize for preview
                img.thumbnail((400, 400))
                
                # Convert to QPixmap
                qt_image = ImageQt.ImageQt(img)
                pixmap = QPixmap.fromImage(qt_image)
                
                self.preview_label.setPixmap(pixmap)
                self.preview_label.setScaledContents(True)
                
                # Update info
                original_img = Image.open(image_path)
                info_text = f"""
File: {os.path.basename(image_path)}
Path: {image_path}
Size: {original_img.size[0]} × {original_img.size[1]} pixels
Mode: {original_img.mode}
Format: {original_img.format}
File Size: {os.path.getsize(image_path) / 1024:.1f} KB
                """.strip()
                
                self.info_text.setPlainText(info_text)
                
        except Exception as e:
            self.preview_label.setText(f"Preview Error:\n{str(e)}")
            self.info_text.setPlainText(f"Error loading image: {str(e)}")
    
    def remove_selected_images(self):
        """Remove selected images (placeholder)."""
        # Future: Implement image selection and removal
        if self.image_paths:
            self.image_paths.pop()  # Remove last image for now
            self.refresh_image_list()
            self.status_bar.showMessage("Removed 1 image")
    
    def clear_all_images(self):
        """Clear all images."""
        if self.image_paths:
            reply = QMessageBox.question(
                self, "Clear All Images",
                f"Are you sure you want to remove all {len(self.image_paths)} images?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.image_paths.clear()
                self.refresh_image_list()
                self.status_bar.showMessage("Cleared all images")
    
    def move_image_up(self):
        """Move selected image up (placeholder)."""
        # Future: Implement with proper selection
        pass
    
    def move_image_down(self):
        """Move selected image down (placeholder)."""
        # Future: Implement with proper selection
        pass
    
    def toggle_compression(self, state: int):
        """Toggle compression options."""
        enabled = state == Qt.Checked
        self.quality_slider.setEnabled(enabled)
        self.quality_label.setEnabled(enabled)
    
    def update_quality_label(self, value: int):
        """Update quality label."""
        self.quality_label.setText(str(value))
    
    def export_pdf(self):
        """Export images to PDF."""
        if not self.image_paths:
            QMessageBox.warning(self, "No Images", "Please add at least one image before exporting.")
            return
        
        # Get save location
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_dialog.setDefaultSuffix("pdf")
        
        if not file_dialog.exec_():
            return
        
        output_path = file_dialog.selectedFiles()[0]
        
        # Disable UI and show progress
        self.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage("Converting to PDF...")
        
        # Start conversion thread
        self.conversion_thread = ConversionThread(
            image_paths=self.image_paths,
            output_path=output_path,
            page_size=self.page_size_combo.currentText(),
            compress=self.compress_check.isChecked(),
            quality=self.quality_slider.value()
        )
        
        self.conversion_thread.progress_updated.connect(self.update_progress)
        self.conversion_thread.conversion_finished.connect(self.conversion_complete)
        self.conversion_thread.conversion_failed.connect(self.conversion_error)
        
        self.conversion_thread.start()
    
    def update_progress(self, progress: float):
        """Update progress bar."""
        self.progress_bar.setValue(int(progress * 100))
    
    def conversion_complete(self, output_path: str):
        """Handle successful conversion."""
        self.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("PDF created successfully")
        
        reply = QMessageBox.question(
            self, "Export Complete",
            f"PDF exported successfully to:\n{output_path}\n\nWould you like to open it now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            self.open_file(output_path)
    
    def conversion_error(self, error_message: str):
        """Handle conversion error."""
        self.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Export failed")
        
        QMessageBox.critical(
            self, "Export Error",
            f"Failed to export PDF:\n{error_message}"
        )
    
    def open_file(self, file_path: str):
        """Open file with default system viewer."""
        import platform
        import subprocess
        
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux
                subprocess.call(['xdg-open', file_path])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open file: {e}")
    
    def new_project(self):
        """Start a new project."""
        if self.image_paths:
            reply = QMessageBox.question(
                self, "New Project",
                "This will clear all current images. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.image_paths.clear()
                self.refresh_image_list()
                self.status_bar.showMessage("New project started")
    
    def open_batch_dialog(self):
        """Open batch processing dialog."""
        dialog = BatchProcessDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Future: Implement batch processing
            QMessageBox.information(
                self, "Batch Processing",
                "Batch processing feature coming soon!"
            )
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About Image-to-PDF Organizer Pro",
            """
            <h3>Image-to-PDF Organizer Pro</h3>
            <p>Version 2.0</p>
            <p>A powerful tool for organizing and converting images to PDF documents.</p>
            <p>Features:</p>
            <ul>
            <li>Drag & drop support</li>
            <li>Dark theme interface</li>
            <li>Advanced PDF options</li>
            <li>Batch processing (coming soon)</li>
            <li>Watermarking (coming soon)</li>
            </ul>
            <p>Built with PyQt5 and Python.</p>
            """
        )
    
    def closeEvent(self, event):
        """Handle close event."""
        if self.conversion_thread and self.conversion_thread.isRunning():
            reply = QMessageBox.question(
                self, "Exit",
                "Conversion is in progress. Exit anyway?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
            
            self.conversion_thread.terminate()
            self.conversion_thread.wait()
        
        self.save_settings()
        event.accept()


def main():
    """Run the advanced GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Image-to-PDF Organizer Pro")
    app.setApplicationVersion("2.0")
    
    # Apply dark theme
    DarkTheme.apply_dark_theme(app)
    app.setStyleSheet(DarkTheme.get_stylesheet())
    
    # Create and show main window
    window = AdvancedImageToPdfGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
