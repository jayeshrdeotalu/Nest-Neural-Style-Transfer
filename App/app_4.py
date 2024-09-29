import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QStackedWidget, QPushButton
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import QTimer, QPropertyAnimation, pyqtSlot, Qt
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtWidgets import * 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("NEST")
        self.resize(1000, 800)

        # Create a QStackedWidget to handle multiple pages
        self.stacked_widget = QStackedWidget(self)

        # Add pages to QStackedWidget
        self.animation_page = QWidget()  # New page for the animation
        self.page1 = QWidget()
        self.image_styling_page = QWidget()
        self.video_styling_page = QWidget()

        # Initialize the background label to handle background images
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)  # Ensure the background image scales
        self.background_label.lower()  # Move background to behind the stacked widget

        self.setup_animation_page()  # Setup the animation page
        self.setup_page1()
        self.setup_image_styling_page()
        self.setup_video_styling_page()

        self.stacked_widget.addWidget(self.animation_page)
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.image_styling_page)
        self.stacked_widget.addWidget(self.video_styling_page)

        # Create a layout for the main window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        # Start with the animation page
        self.show_animation_page()

    def set_background_image(self, image_path):
        """ Set the background image for the window. """
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():  # Check if the pixmap is valid
            self.background_label.setPixmap(pixmap)
            self.background_label.resize(self.size())  # Ensure background label resizes

    def setup_animation_page(self):
        """ Setup the animation page. """
        # Set layout for the animation page
        layout = QVBoxLayout(self.animation_page)

        # Set a background image for the animation page
        #TODO : change the image...
        self.set_background_image("Data/Wallpaper_2.jpeg")  # Background for animation page

        # Create a label for the animation text
        self.welcome_label = QLabel("Welcome to NEST", self.animation_page)
        self.welcome_label.setStyleSheet(
            "QLabel { font-size: 30px; color: white; background-color: black; border-radius: 15px; padding: 20px;}"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.resize(300, 100)
        layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set up a timer to transition after the animation is done
        #TODO : Make it 1500 at the time of deployment
        QTimer.singleShot(2, self.fade_out_welcome_message)  # Animation duration

    def fade_out_welcome_message(self):
        # Create a fade-out animation for the welcome label
        self.opacity_effect = QGraphicsOpacityEffect()
        self.welcome_label.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)  # Duration of the fade effect
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(self.go_to_main_page)
        self.fade_animation.start()

    def go_to_main_page(self):
        # Remove the animation page and switch to the main menu
        self.stacked_widget.setCurrentWidget(self.page1)
        self.set_background_image("Data/Wallpaper_2.jpeg")  # Set background for main page

    def setup_page1(self):
        '''Set layout for page 1'''
        self.page1_layout = QVBoxLayout(self.page1)

        # Add title label
        title_label = QLabel("Please choose a method to perform styling", self.page1)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;                           /* Larger font size for the title */
                color: white;                              /* White text for contrast */
                background-color: qlineargradient(
                    spread: pad, x1:0, y1:0, x2:1, y2:1, 
                    stop: 0 #BA55D3, stop: 1 #FFB6C1);     /* Gradient from medium orchid to light pink */
                padding: 15px 30px;                        /* Extra padding for a title-like appearance */
                border-radius: 15px;                       /* Rounded corners matching the button */
                font-family: 'Segoe UI', sans-serif;       /* Matching font */
                font-weight: 600;                          /* Semi-bold for emphasis */
            }
        """)

        self.page1_layout.addStretch(1)

        self.page1_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.page1_layout.addStretch(1)

        # Create clickable boxes for image and video styling
        self.create_styling_boxes(self.page1_layout)

    def setup_image_styling_page(self):
        """Set layout for image styling page"""
        
        # Create layout for the image styling page
        layout = QVBoxLayout(self.image_styling_page)

        # Create and style the back button
        back_button = QPushButton("<")
        back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        back_button.clicked.connect(self.go_to_main_page)
        layout.addWidget(back_button)

        back_button.setStyleSheet("""
            QPushButton {
                background-color: darkgray;  
                color: white;              
                border-style: outset;
                border-width: 2px;
                border-color: beige;             
                padding: 10px 20px;         
                font-size: 16px;            
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;  
            }
            QPushButton:pressed {
                background-color: black;
            }
        """)

        # Label for the page title
        label = QLabel("Image Styling Page", self.image_styling_page)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add the selection UI (art image and input image selection boxes)
        self.art_label = QLabel("Select art image", self.image_styling_page)
        self.input_label = QLabel("Select input image", self.image_styling_page)

        self.art_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.art_label.setStyleSheet("border: 2px solid black; padding: 20px;")
        self.art_label.mousePressEvent = self.select_art_image

        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_label.setStyleSheet("border: 2px solid black; padding: 20px;")
        self.input_label.mousePressEvent = self.select_input_image

        # Button to process the styling
        process_button = QPushButton("Process the styling")
        process_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border-radius: 10px; 
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Add widgets to layout
        layout.addWidget(self.art_label)
        layout.addWidget(self.input_label)
        layout.addWidget(process_button)

    def select_art_image(self, event):
        # Open file dialog to select image
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Art Image", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if file_name:
            self.update_label_with_image(self.art_label, file_name)

    def select_input_image(self, event):
        # Open file dialog to select image or video
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input Image/Video", "", "Images (*.png *.xpm *.jpg *.jpeg);;Videos (*.mp4 *.avi *.mkv)")
        if file_name:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.xpm')):
                self.update_label_with_image(self.input_label, file_name)
            else:
                # Use a placeholder wallpaper for video selection
                self.set_video_thumbnail(self.input_label)

    def update_label_with_image(self, label, file_name):
        # Load and set the image as wallpaper for the label
        pixmap = QPixmap(file_name)
        label.setPixmap(pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def set_video_thumbnail(self, label):
        # Set a placeholder or default thumbnail for video selection
        placeholder_image = "path/to/video_thumbnail.png"  # Replace with actual path to a video placeholder image
        pixmap = QPixmap(placeholder_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def setup_video_styling_page(self):
        """Set layout for video styling page"""
        
        layout = QVBoxLayout(self.video_styling_page)

        back_button = QPushButton("<")
        back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        back_button.clicked.connect(self.go_to_main_page)
        layout.addWidget(back_button)

        # Set the style of the button
        back_button.setStyleSheet("""
            QPushButton {
                background-color: darkgray;  
                color: white;              
                border-style: outset;
                border-width: 2px;
                border-color: beige;             
                padding: 10px 20px;         
                font-size: 16px;            
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;  
            }
            QPushButton:pressed {
                background-color: lightblack;
            }
        """)
        
        label = QLabel("Video Styling Page", self.video_styling_page)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # set_selection_box_ui(is_image_styling = False)

        
    def on_image_styling_click(self, event):
        self.stacked_widget.setCurrentWidget(self.image_styling_page)
        self.set_background_image("Data/image_styling_background.jpeg")  # Set background for image styling page

    def on_video_styling_click(self, event):
        self.stacked_widget.setCurrentWidget(self.video_styling_page)
        self.set_background_image("Data/video_styling_background.jpeg")  # Set background for video styling page

    def create_styling_boxes(self, parent_layout):
        """Create a horizontal layout for image and video styling options"""
        animation_layout = QHBoxLayout()

        animation_style = """
        QPushButton {
            background-color: qlineargradient(
                spread: pad, x1:0, y1:0, x2:1, y2:1, 
                stop: 0 #8A2BE2, stop: 1 #FF69B4);  /* Gradient from purple (violet) to pink */
            color: white;                          /* White text */
            border-radius: 15px;                   /* Rounded corners */
            padding: 12px 24px;                    /* Padding for space */
            font-family: 'Segoe UI', sans-serif;   /* Clean font */
            font-size: 16px;                       /* Font size */
            border: none;                          /* No border */
            font-weight: 600;                      /* Semi-bold font */
        }
        QPushButton:hover {
            background-color: qlineargradient(
                spread: pad, x1:0, y1:0, x2:1, y2:1, 
                stop: 0 #9370DB, stop: 1 #FF82AB);  /* Lighter purple to pink on hover */
        }
        QPushButton:pressed {
            background-color: qlineargradient(
                spread: pad, x1:0, y1:0, x2:1, y2:1, 
                stop: 0 #6A0DAD, stop: 1 #FF1493);  /* Darker purple to pink when pressed */
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

        image_label = QPushButton("Image Styling", self)
        # image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet(animation_style)
        image_label.clicked.connect(self.on_image_styling_click)

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

        video_label = QPushButton("Video Styling", self)
        # video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_label.setStyleSheet(animation_style)
        video_label.clicked.connect(self.on_video_styling_click)

        video_layout = QVBoxLayout()
        video_layout.addWidget(video_animation)
        video_layout.addWidget(video_label)
        video_layout.setSpacing(20)

        # Add image and video layouts to animation layout
        animation_layout.addLayout(image_layout)
        animation_layout.addLayout(video_layout)

        # Add animation layout to parent layout
        parent_layout.addLayout(animation_layout)
        parent_layout.addStretch(2)

    def resizeEvent(self, event):
        # Ensure the background image resizes with the window
        self.background_label.resize(self.size())

    def show_animation_page(self):
        # Set the initial page to be the animation page
        self.stacked_widget.setCurrentWidget(self.animation_page)

    def set_selection_box_ui(self, is_image_styling = True):
        """To set selection UI of art and input image"""
        return


# Initialization of application
app = QApplication(sys.argv)

# Create window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())
