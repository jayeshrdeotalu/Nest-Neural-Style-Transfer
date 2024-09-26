import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, QTimer, QPropertyAnimation, pyqtSlot, Qt

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
        self.resize(1000, 800)

        # Center the window on the screen
        self.center_window()

        # Create a background label
        self.background_label = QLabel(self)
        self.set_background_image(r"Data/Wallpaper_2.jpeg")  # Change the path as needed

        # Set main layout
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.addStretch(2)

        # Front setup
        self.front_setup()
        self.main_layout.addStretch(3)

        # Start the welcome animation
        self.show_welcome_animation()

    def set_background_image(self, image_path):
        # Load the image
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
        else:
            print("Error: Background image not found.")

        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())

    def resizeEvent(self, event):
        # Ensures the background image resizes when the window is resized
        self.background_label.resize(self.size())

    def center_window(self):
        # Center the window on the screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def show_welcome_animation(self):
        # Create the welcome message label
        self.welcome_label = QLabel("Welcome to NEST", self)
        self.welcome_label.setStyleSheet(
            "QLabel { font-size: 30px; color: black; background-color: white; border-radius: 15px; padding: 20px; }"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.resize(300, 100)
        self.welcome_label.move(self.rect().center() - self.welcome_label.rect().center())

        # Create a blur effect for the background
        self.blur_effect = QGraphicsBlurEffect()
        self.background_label.setGraphicsEffect(self.blur_effect)

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

    def front_setup(self):
        # Add a label at the top
        title_label = QLabel("Please choose a method to perform styling", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: black; background-color: #f0f0f0; padding: 10px; border-radius: 10px;")
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
        }
        """

        # Create the first label for image styling (GIF)
        image_animation = QLabel(self)
        image_animation.setStyleSheet(animation_style)
        image_animation.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        movie = QMovie("Data/image_styling_animation_2.gif")  # Replace with actual GIF file path
        if movie.isValid():
            image_animation.setMovie(movie)
            movie.start()
        else:
            print("Error: GIF not found.")

        # Add click event to image styling animation
        image_animation.mousePressEvent = self.on_image_styling_click

        # Create a label below for "Image Styling"
        image_label = QLabel("Image Styling", self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a vertical layout to stack the image animation and its label
        image_layout = QVBoxLayout()
        image_layout.addWidget(image_animation)
        image_layout.addWidget(image_label)

        # Create the second label for video styling (video widget)
        video_animation = QLabel(self)
        video_animation.setStyleSheet(animation_style)
        video_animation.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create video playback widget inside the video animation label
        video_widget = QVideoWidget(video_animation)
        video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        video_widget.setMinimumSize(300, 200)  # Set a minimum size for the video

        media_player = QMediaPlayer(self)
        audio_output = QAudioOutput(self)
        media_player.setAudioOutput(audio_output)
        media_player.setSource(QUrl.fromLocalFile(r"Data/test_video_styling_animation.mp4"))  # Replace with actual video file path

        # Ensure the video plays in a loop
        media_player.setLoops(QMediaPlayer.Loops.Infinite)
        media_player.setVideoOutput(video_widget)
        media_player.play()

        # Add click event to video styling animation
        video_animation.mousePressEvent = self.on_video_styling_click

        # Create a label below for "Video Styling"
        video_label = QLabel("Video Styling", self)
        video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a vertical layout to stack the video animation and its label
        video_layout = QVBoxLayout()
        video_layout.addWidget(video_animation)
        video_layout.addWidget(video_label)

        # Add both layouts (image and video) to the horizontal layout
        animation_layout.addLayout(image_layout)
        animation_layout.addLayout(video_layout)

        # Add the animation layout to the parent layout
        parent_layout.addLayout(animation_layout)

    def on_image_styling_click(self, event):
        print("Image Styling clicked!")

    def on_video_styling_click(self, event):
        print("Video Styling clicked!")

# Initialization of application
app = QApplication(sys.argv)

# window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())
