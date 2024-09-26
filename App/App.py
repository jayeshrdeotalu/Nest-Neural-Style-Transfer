# Just Checking the version...
from PyQt6.QtCore import QT_VERSION_STR
print("Just Checking the version..." + QT_VERSION_STR)

# Basic code
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QScreen

# More imports
from PyQt6.QtCore import QTimer, QPropertyAnimation, pyqtSlot, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, 
    QGraphicsOpacityEffect, QGraphicsBlurEffect
)
from PyQt6.QtWidgets import *

# Importing movie functionalities 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

from PyQt6.QtCore import QUrl

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("NEST")
        self.resize(1000, 800)  # Set the window size (width, height)

        # Center the window on the screen
        self.center_window()

        # Create a background label
        self.background_label = QLabel(self)
        self.set_background_image(r"Data/Wallpaper_2.jpeg")  # image path

        # Set main layout
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.addStretch(2)
        self.front_setup()
        self.main_layout.addStretch(3)

         # Start the welcome animation
        self.show_welcome_animation()

    def set_background_image(self, image_path):
        # Load the image
        pixmap = QPixmap(image_path)
        # Set the pixmap to the label
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)  # Make sure it scales
        self.background_label.resize(self.size())  # Resize the label to fit the window

    def resizeEvent(self, event):
        # This ensures the background image resizes when the window is resized
        self.background_label.resize(self.size())

    def center_window(self):
        # Getting the screen geometry and the window geometry
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Moving to center
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def show_welcome_animation(self):
        # Create the welcome message label
        self.welcome_label = QLabel("Welcome to NEST", self)
        self.welcome_label.setStyleSheet(
            "QLabel { font-size: 30px; color: black; background-color: white; border-radius: 15px; padding: 20px;}"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.resize(300, 100)
        self.welcome_label.move(self.rect().center() - self.welcome_label.rect().center())

        # Create a blur effect for the background
        self.blur_effect = QGraphicsBlurEffect()
        self.background_label.setGraphicsEffect(self.blur_effect)

        self.welcome_label.raise_()

        # Set up a timer to fade out the welcome label
        QTimer.singleShot(1500, self.fade_out_welcome_message)  # Increased to 1.5 seconds

    def fade_out_welcome_message(self):
        # Create a fade-out animation for the welcome label
        self.opacity_effect = QGraphicsOpacityEffect()
        self.welcome_label.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)  # Duration of the fade effect
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(self.remove_welcome_message)
        self.fade_animation.start()

    @pyqtSlot()
    def remove_welcome_message(self):
        # Remove the welcome label and reset the blur effect
        self.welcome_label.hide()
        self.background_label.setGraphicsEffect(None)

    def on_button_click(self):
        print("Button clicked!")

    def front_setup(self):
        # Add a label at the top
        title_label = QLabel("Please choose a method to perform styling", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: black; background-color: #f0f0f0; padding: 10px; border-radius: 10px;")
        # title_label.setStyleSheet("font-size: 24px; color: black;")
        # title_label.setFixedWidth(700)  # Fixed width for the label
        title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(1) 

         # Create the two clickable boxes
        self.create_styling_boxes(self.main_layout)

    def create_styling_boxes(self, parent_layout):
        # Create a horizontal layout for the two boxes
        animation_layout = QHBoxLayout()

        # Styling for the boxes and text inside
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

        # Create the first label for image styling (GIF)
        image_animation = QLabel(self)
        image_animation.setStyleSheet(animation_style)
        image_animation.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        movie = QMovie("Data/image_styling_animation_2.gif")  # Replace with actual GIF file path
        image_animation.setMovie(movie)
        image_animation.setScaledContents(True)  # Scale the GIF to fit the label
        movie.start()

        # Add click event to image styling animation
        image_animation.mousePressEvent = self.on_image_styling_click

        # Create a label below for "Image Styling"
        image_label = QLabel("Image Styling", self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("background-color: gray;border-radius: 10px;")

        # Create a vertical layout to stack the image animation and its label
        image_layout = QVBoxLayout()
        image_layout.addWidget(image_animation)
        image_layout.addWidget(image_label)

        image_layout.setSpacing(20)  # Space between image and label

         # Create the first label for image styling (GIF)
        video_animation = QLabel(self)
        video_animation.setStyleSheet(animation_style)
        video_animation.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        v_movie = QMovie("Data/test_video_annimation_2.gif")  # Replace with actual GIF file path
        video_animation.setMovie(v_movie)
        video_animation.setScaledContents(True)  # Scale the GIF to fit the label
        v_movie.start()

        # Add click event to image styling animation
        video_animation.mousePressEvent = self.on_image_styling_click

        # Add click event to video styling animation
        video_animation.mousePressEvent = self.on_video_styling_click

        # Create a label below for "Video Styling"
        video_label = QLabel("Video Styling", self)
        video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_label.setStyleSheet("background-color: gray;border-radius: 10px;")

        # Create a vertical layout to stack the video animation and its label
        video_layout = QVBoxLayout()
        video_layout.addWidget(video_animation)
        video_layout.addWidget(video_label)

        video_layout.setSpacing(20)

        # Add both layouts (image and video) to the horizontal layout
        animation_layout.addLayout(image_layout)
        animation_layout.addLayout(video_layout)

        # Add the animation layout to the parent layout
        parent_layout.addLayout(animation_layout)

    def on_image_styling_click(self, event): # Event is just a extra parameter
        print("Image Styling clicked!")

    def on_video_styling_click(self, event): # event just a extra parameter
        print("Video Styling clicked!")

# Initialization of application
app = QApplication(sys.argv)

# window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())





