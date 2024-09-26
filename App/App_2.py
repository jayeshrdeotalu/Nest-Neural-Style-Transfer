import sys
from PyQt6.QtCore import QTimer, QPropertyAnimation, pyqtSlot, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QWidget, 
    QHBoxLayout, QGraphicsOpacityEffect, QGraphicsBlurEffect, QPushButton, QSizePolicy
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
        self.set_background_image(r"Data/Wallpaper_2.jpeg")  # Image path

        # Set up layout for the main content
        layout = QVBoxLayout(self)

        # Add a label at the top with fixed width
        title_label = QLabel("Please choose a method to perform styling", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 24px; color: black; background-color: #f0f0f0; padding: 10px; border-radius: 10px;")
        title_label.setFixedWidth(400)  # Fixed width for the label
        title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the label

        # Create the two clickable boxes
        self.create_styling_boxes(layout)

        # Set the main layout
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

    def create_styling_boxes(self, parent_layout):
        # Create a horizontal layout for the two boxes
        box_layout = QHBoxLayout()

        # Styling for the boxes and text inside
        box_style = """
        QPushButton {
            background-color: #3498db;
            color: white;
            font-size: 18px;
            border-radius: 20px;
            padding: 20px;
            border: 2px solid #2980b9;
            min-width: 200px;
            max-width: 300px;
            min-height: 100px;
            text-align: center;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        """

        # Create the first box for image styling
        image_box = QPushButton("Image Styling", self)
        image_box.setStyleSheet(box_style)
        image_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_box.clicked.connect(self.on_image_styling_click)

        # Create the second box for video styling
        video_box = QPushButton("Video Styling", self)
        video_box.setStyleSheet(box_style)
        video_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        video_box.clicked.connect(self.on_video_styling_click)

        # Add the boxes to the horizontal layout
        box_layout.addWidget(image_box)
        box_layout.addWidget(video_box)

        # Add the box layout to the parent layout
        parent_layout.addLayout(box_layout)

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
        QTimer.singleShot(2000, self.fade_out_welcome_message)

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

    def on_image_styling_click(self):
        print("Image Styling clicked!")

    def on_video_styling_click(self):
        print("Video Styling clicked!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
