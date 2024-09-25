# Just Checking the version...
from PyQt6.QtCore import QT_VERSION_STR
print("Just Checking the version..." + QT_VERSION_STR)

# Basic code
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QScreen

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

    def on_button_click(self):
        print("Button clicked!")

# Initialization of application
app = QApplication(sys.argv)

# window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())





