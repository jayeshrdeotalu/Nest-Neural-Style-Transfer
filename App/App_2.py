import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QStackedWidget to hold the pages
        self.stack = QStackedWidget()

        # Create the first page (main page)
        self.page1 = QWidget()
        self.page1_layout = QVBoxLayout()
        self.page1_button = QPushButton("Go to Page 2")
        self.page1_button.clicked.connect(self.go_to_page2)
        self.page1_layout.addWidget(self.page1_button)
        self.page1.setLayout(self.page1_layout)

        # Create the second page
        self.page2 = QWidget()
        self.page2_layout = QVBoxLayout()
        self.page2_button = QPushButton("Go Back to Page 1")
        self.page2_button.clicked.connect(self.go_to_page1)
        self.page2_layout.addWidget(self.page2_button)
        self.page2.setLayout(self.page2_layout)

        # Add the pages to the QStackedWidget
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        # Set the initial page (page 1)
        self.stack.setCurrentWidget(self.page1)

        # Create a layout for the main window and add the QStackedWidget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def go_to_page2(self):
        self.stack.setCurrentWidget(self.page2)

    def go_to_page1(self):
        self.stack.setCurrentWidget(self.page1)


# Initialize the application
app = QApplication(sys.argv)

# Create the main window and show it
window = MainWindow()
window.show()

# Run the application event loop
sys.exit(app.exec())
