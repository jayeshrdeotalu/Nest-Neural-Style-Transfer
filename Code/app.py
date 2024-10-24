import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QStackedWidget, QPushButton
from PyQt6.QtGui import QPixmap, QMovie, QImage
from PyQt6.QtCore import QTimer, QPropertyAnimation, pyqtSlot, Qt
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtWidgets import * 

import cv2

#import additional
from NST_Code.video_processing_2 import Video_Processing
from NST_Code.image_processing import ImageProcessing

# Import multi-treading 
from NST_Code.Worker import ProcessingWorker

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("NEST")
        self.resize(1000, 800)

        self.input_image_path = None
        self.art_image_path = None
        self.input_video_path = None
        self.output_file_path = None
        
        self.input_box_style = '''
        QLabel {
                border: 4px solid black; 
                padding: 20px;
                min-height : 450px;
                max-height : 450px;
                min-width : 300px;
                max-width : 300px;
                border-color: beige;
                border-radius: 20px;
                font: bold 18px;
            }
        '''

        self.back_button_style = '''
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
            '''

        # Create a QStackedWidget to handle multiple pages
        self.stacked_widget = QStackedWidget(self)

        # Add pages to QStackedWidget
        self.animation_page = QWidget()  # New page for the animation
        self.page1 = QWidget()
        self.image_styling_page = QWidget()
        self.video_styling_page = QWidget()
        self.final_page = QWidget()

        # Initialize the background label to handle background images
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)  # Ensure the background image scales
        self.background_label.lower()  # Move background to behind the stacked widget

        self.setup_animation_page()  # Setup the animation page
        self.setup_page1()
        self.setup_image_styling_page()
        self.setup_video_styling_page()
        self.setup_final_page()

        self.stacked_widget.addWidget(self.animation_page)
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.image_styling_page)
        self.stacked_widget.addWidget(self.video_styling_page)
        self.stacked_widget.addWidget(self.final_page)

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
        QTimer.singleShot(1400, self.fade_out_welcome_message)  # Animation duration

    def fade_out_welcome_message(self):
        # Create a fade-out animation for the welcome label
        self.opacity_effect = QGraphicsOpacityEffect()
        self.welcome_label.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(self.go_to_main_page)
        self.fade_animation.start()

    def go_to_main_page(self):
        # Remove the animation page and switch to the main menu
        self.stacked_widget.setCurrentWidget(self.page1)
        self.set_background_image("Data/Wallpaper_2.jpeg")

    def go_to_previous_page(self):
        current_index = self.stacked_widget.currentIndex()
        
        if current_index > 0:
            # Go to the previous page
            self.stacked_widget.setCurrentIndex(current_index - 1)
        else:
            # Optional: Handle the case when you are at the first page
            print("Already on the first page.")

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

        input_box_layout = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        back_button.clicked.connect(self.go_to_main_page)
        layout.addWidget(back_button)

        back_button.setStyleSheet(self.back_button_style)

        self.input_image_label = QLabel("Select input image", self.image_styling_page)
        self.art_image_label = QLabel("Select art image", self.image_styling_page)

        self.input_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_image_label.setStyleSheet(self.input_box_style)
        self.input_image_label.mousePressEvent = lambda x: self.select_input_image(None, True)

        self.art_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.art_image_label.setStyleSheet(self.input_box_style)
        self.art_image_label.mousePressEvent = lambda x : self.select_art_image(None, True)

        # Button to process the styling
        process_button = QPushButton("Process the styling")
        process_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border-radius: 10px; 
                padding: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        process_button.clicked.connect(lambda x : self.process_nst(is_image_processing = True))

        # Add widgets to layout
        input_box_layout.addWidget(self.input_image_label)
        input_box_layout.addWidget(self.art_image_label)
        layout.addLayout(input_box_layout)
        layout.addWidget(process_button)

    def setup_video_styling_page(self):
        """Set layout for video styling page"""
        
        layout = QVBoxLayout(self.video_styling_page)

        input_box_layout = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        back_button.clicked.connect(self.go_to_main_page)
        layout.addWidget(back_button)

        back_button.setStyleSheet(self.back_button_style)

        self.input_video_label = QLabel("Select input video", self.image_styling_page)
        self.art_video_label = QLabel("Select art image", self.image_styling_page)

        self.input_video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_video_label.setStyleSheet(self.input_box_style)
        self.input_video_label.mousePressEvent = lambda x : self.select_input_image(None, False)

        self.art_video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.art_video_label.setStyleSheet(self.input_box_style)
        self.art_video_label.mousePressEvent = lambda x : self.select_art_image(None, False)

        # Button to process the styling
        process_button = QPushButton("Process the styling")
        process_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border-radius: 10px; 
                padding: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        process_button.clicked.connect(lambda x : self.process_nst(is_image_processing = False))

        # Add widgets to layout
        input_box_layout.addWidget(self.input_video_label)
        input_box_layout.addWidget(self.art_video_label)
        layout.addLayout(input_box_layout)
        layout.addWidget(process_button)

    def setup_final_page(self):

        layout = QVBoxLayout(self.final_page)

        back_button = QPushButton("Back")
        back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        back_button.clicked.connect(self.go_to_previous_page)
        layout.addWidget(back_button)

        back_button.setStyleSheet(self.back_button_style)

        self.display_widget = QWidget(self)
        self.display_widget.setFixedSize(640, 480)  # Fixed size for the media widget
        self.display_layout = QVBoxLayout(self.display_widget)

        # Video Widget
        self.video_widget = QVideoWidget(self.final_page)
        self.display_layout.addWidget(self.video_widget)

        # Image Widget (QLabel)
        self.image_label = QLabel(self.display_widget)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)  # Ignore to allow scaling
        self.image_label.setScaledContents(True)  # Make image scale to fit
        self.display_layout.addWidget(self.image_label)

        # Media Player for video
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)

        output_label_layout = QHBoxLayout()
        output_label_layout.addStretch()
        output_label_layout.addWidget(self.display_widget)
        output_label_layout.addStretch()

         # Placeholder for image zooming
        self.current_pixmap = None
        self.original_pixmap = None

        # Button to process the styling
        main_menu_button_layout = QHBoxLayout()
        main_menu_button_layout.addStretch()
        main_menu_button = QPushButton("Back to main menu")
        main_menu_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        main_menu_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border-radius: 10px; 
                padding: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        main_menu_button_layout.addWidget(main_menu_button)
        main_menu_button_layout.addStretch()

        main_menu_button.clicked.connect(self.go_to_main_page)

        # Add widgets to layout
        layout.addLayout(output_label_layout)
        layout.addLayout(main_menu_button_layout)

        # Initially hide video widget
        self.video_widget.hide()

        # self.connect_output()
    
    def show_image(self, image_path):
        # Hide video widget if showing image
        self.video_widget.hide()
        self.media_player.stop()

        # Show image
        self.image_label.show()
        self.original_pixmap = QPixmap(image_path)
        self.image_label.setPixmap(self.original_pixmap)
        self.current_pixmap = self.original_pixmap
        return
    
    def play_video(self, video_path):
         # Hide image widget if showing video
        self.image_label.hide()

        # Show video
        self.video_widget.show()
        
        # Play video (convert path to QUrl)
        video_url = QUrl.fromLocalFile(video_path)
        self.media_player.setSource(video_url)
        self.media_player.play()

    
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
        v_movie = QMovie("Data/playable_video_112_diff.gif")
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

    def set_selection_box_ui(self, layout,  is_image_styling = True):
        """To set selection UI of art and input image, returns path to art, input."""

        return
    
    def select_art_image(self, event, is_img_styling):
        # Open file dialog to select image
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Art Image", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if file_name:
            self.art_image_path = file_name
            if is_img_styling:
                self.update_label_with_image(self.art_image_label, file_name)
            else:
                self.update_label_with_image(self.art_video_label, file_name)

    def select_input_image(self, event, is_img_styling):
        #TODO : Add error, exception
        # Open file dialog to select image or video
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Images and Videos (*.png *.jpg *.jpeg *.bmp *.gif *.mp4 *.avi *.mov *.mkv)"
        )   
        if file_name:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.xpm')):
                self.input_image_path = file_name
                self.update_label_with_image(self.input_image_label, file_name)
            else:
                self.input_video_path = file_name
                self.set_video_thumbnail(self.input_video_label, file_name)

    def update_label_with_image(self, label, file_name):
        # Load and set the image as wallpaper for the label
        pixmap = QPixmap(file_name)
        label.setPixmap(pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def set_video_thumbnail(self, label, video_file):
        # Set a placeholder or default thumbnail for video selection
        capture = cv2.VideoCapture(video_file)
        success, frame = capture.read()
        capture.release()

        if success:
            # Convert the frame to a QPixmap
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale the pixmap to fit the label and set it as the label's pixmap
            label.setPixmap(pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        else:
            print("Error: Could not read frame from video.")

    def process_nst(self, is_image_processing):
        # Show the loading popup
        self.show_loading_popup(is_image_processing)

        # Determine the input path based on whether it's an image or video
        input_path = self.input_image_path if is_image_processing else self.input_video_path

        # Create and start the worker thread
        self.worker = ProcessingWorker(is_image_processing, self.art_image_path, input_path)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.start()
    
    def on_processing_finished(self, output_file_path):
        # Hide the loading popup
        self.hide_loading_popup()

        # Continue with the execution
        self.output_file_path = output_file_path
        if self.output_file_path:
            self.connect_output()
            self.stacked_widget.setCurrentWidget(self.final_page)

    def show_loading_popup(self, is_image_processing):

        if is_image_processing:
            self.loading_dialog = QDialog(self.image_styling_page)
        else :
            self.loading_dialog = QDialog(self.video_styling_page)

        self.loading_dialog.setWindowTitle("Processing")
        self.loading_dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # self.loading_dialog.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_dialog.setModal(True)
        self.loading_dialog.setFixedSize(600, 300)

        # Create a layout and center the content
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a label with a message
        label = QLabel("Image/Video is processing...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add a QLabel to display the loading animation
        movie_label = QLabel()
        movie = QMovie("Data/loading_gif.gif") 
        movie_label.setMovie(movie)
        movie_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        movie.start()
        layout.addWidget(movie_label)

        self.loading_dialog.setLayout(layout)

        self.loading_dialog.show()

    def hide_loading_popup(self):
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.close()

    def connect_output(self):
        
        if not self.output_file_path:
            return
        
        if self.output_file_path:
            if self.output_file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.show_image(self.output_file_path)
            elif self.output_file_path.lower().endswith(('.mp4', '.avi')):
                print("Directing to video play")
                self.play_video(self.output_file_path)
        return

# Initialization of application
app = QApplication(sys.argv)

# Create window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())
