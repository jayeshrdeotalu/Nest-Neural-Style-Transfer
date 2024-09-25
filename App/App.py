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

        # Create a button
        button = QPushButton("Click Me!", self)
        button.clicked.connect(self.on_button_click)

        # Set layout
        layout = QVBoxLayout(self)
        layout.addWidget(button)
        self.setLayout(layout)

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
            "QLabel { font-size: 30px; color: black; background-color: white; border-radius: 15px; padding: 20px; }"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.resize(300, 100)
        self.welcome_label.move(self.rect().center() - self.welcome_label.rect().center())

        # Create a blur effect for the background
        self.blur_effect = QGraphicsBlurEffect()
        self.background_label.setGraphicsEffect(self.blur_effect)

        # Set up a timer to fade out the welcome label
        QTimer.singleShot(600, self.fade_out_welcome_message)

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

# Initialization of application
app = QApplication(sys.argv)

# window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())





