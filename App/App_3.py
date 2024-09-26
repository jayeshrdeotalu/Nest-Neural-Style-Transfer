import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QStackedWidget, QPushButton
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import QTimer, QPropertyAnimation, pyqtSlot, Qt
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QGraphicsBlurEffect


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("NEST")
        self.resize(1000, 800)

        # Create a QStackedWidget to handle multiple pages
        self.stacked_widget = QStackedWidget(self)

        # Add pages to QStackedWidget
        self.page1 = QWidget()
        self.image_styling_page = QWidget()
        self.video_styling_page = QWidget()

        self.setup_page1()
        self.setup_image_styling_page()
        self.setup_video_styling_page()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.image_styling_page)
        self.stacked_widget.addWidget(self.video_styling_page)

        # Create a layout for the main window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        # Background label to handle background images
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)  # Ensure the background image scales
        self.set_background_image("Data/Wallpaper_2.jpeg")  # Initial background

        # Move background to behind the stacked widget
        self.background_label.lower()  # Send the background label to the back

        # Handle window resizing to adjust background size
        self.resizeEvent(None)

        # Start the welcome animation
        self.show_welcome_animation()

    def set_background_image(self, image_path):
        """ Set the background image for the window. """
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap)
        self.background_label.resize(self.size())  # Make sure the background resizes

    def setup_page1(self):
        # Set layout for page 1
        self.page1_layout = QVBoxLayout(self.page1)

        # Add title label
        title_label = QLabel("Please choose a method to perform styling", self.page1)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: black;
                background-color : gray;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        self.page1_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create clickable boxes for image and video styling
        self.create_styling_boxes(self.page1_layout)

    def setup_image_styling_page(self):
        # Set layout for image styling page
        layout = QVBoxLayout(self.image_styling_page)
        label = QLabel("Image Styling Page", self.image_styling_page)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.go_to_main_page)
        layout.addWidget(back_button)

    def setup_video_styling_page(self):
        # Set layout for video styling page
        layout = QVBoxLayout(self.video_styling_page)
        label = QLabel("Video Styling Page", self.video_styling_page)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.go_to_main_page)
        layout.addWidget(back_button)

    def go_to_main_page(self):
        self.stacked_widget.setCurrentWidget(self.page1)
        self.set_background_image("Data/Wallpaper_2.jpeg")  # Change background for main page

    def on_image_styling_click(self, event):
        self.stacked_widget.setCurrentWidget(self.image_styling_page)
        self.set_background_image("Data/image_styling_background.jpeg")  # Set background for image styling page

    def on_video_styling_click(self, event):
        self.stacked_widget.setCurrentWidget(self.video_styling_page)
        self.set_background_image("Data/video_styling_background.jpeg")  # Set background for video styling page

    def create_styling_boxes(self, parent_layout):
        # Create a horizontal layout for image and video styling options
        animation_layout = QHBoxLayout()

        animation_style = """
        QPushButton:hover {
            background-color: #2980b9;
        }

        QLabel {
            border: none;
            background-color: transparent;
            min-width : 150px;
            max-width : 250px;
            min-height : 120px;
            max-height : 220px;
        }
        """

        # Image styling GIF and label
        image_animation = QLabel(self)
        image_animation.setStyleSheet(animation_style)
        image_animation.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        movie = QMovie("Data/image_styling_animation_2.gif")
        image_animation.setMovie(movie)
        image_animation.setScaledContents(True)
        movie.start()
        image_animation.mousePressEvent = self.on_image_styling_click

        image_label = QLabel("Image Styling", self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("background-color: gray; border-radius: 10px;")

        image_layout = QVBoxLayout()
        image_layout.addWidget(image_animation)
        image_layout.addWidget(image_label)
        image_layout.setSpacing(20)

        # Video styling GIF and label
        video_animation = QLabel(self)
        video_animation.setStyleSheet(animation_style)
        video_animation.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        v_movie = QMovie("Data/test_video_annimation_2.gif")
        video_animation.setMovie(v_movie)
        video_animation.setScaledContents(True)
        v_movie.start()
        video_animation.mousePressEvent = self.on_video_styling_click

        video_label = QLabel("Video Styling", self)
        video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_label.setStyleSheet("background-color: gray; border-radius: 10px;")

        video_layout = QVBoxLayout()
        video_layout.addWidget(video_animation)
        video_layout.addWidget(video_label)
        video_layout.setSpacing(20)

        # Add image and video layouts to animation layout
        animation_layout.addLayout(image_layout)
        animation_layout.addLayout(video_layout)

        # Add animation layout to parent layout
        parent_layout.addLayout(animation_layout)

    def show_welcome_animation(self):
        # Welcome animation can be kept unchanged
        self.welcome_label = QLabel("Welcome to NEST", self.page1)
        self.welcome_label.setStyleSheet(
            "QLabel { font-size: 30px; color: black; background-color: white; border-radius: 15px; padding: 20px;}"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.resize(300, 100)
        self.welcome_label.move(self.rect().center() - self.welcome_label.rect().center())

        self.blur_effect = QGraphicsBlurEffect()
        self.stacked_widget.setGraphicsEffect(self.blur_effect)

        self.welcome_label.raise_()
        QTimer.singleShot(1500, self.fade_out_welcome_message)

    def fade_out_welcome_message(self):
        self.opacity_effect = QGraphicsOpacityEffect()
        self.welcome_label.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(self.remove_welcome_message)
        self.fade_animation.start()

    @pyqtSlot()
    def remove_welcome_message(self):
        self.welcome_label.hide()
        self.stacked_widget.setGraphicsEffect(None)

    def resizeEvent(self, event):
        # Ensure the background image resizes with the window
        self.background_label.resize(self.size())


# Initialization of application
app = QApplication(sys.argv)

# Create window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())
