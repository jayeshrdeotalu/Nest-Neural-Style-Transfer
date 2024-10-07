from PyQt6.QtCore import QThread, pyqtSignal

from NST_Code.video_processing_2 import Video_Processing
from NST_Code.image_processing import ImageProcessing

class ProcessingWorker(QThread):
    finished = pyqtSignal(str)  # Signal emitted when processing is complete, sending the output file path.

    def __init__(self, is_image_processing, art_image_path, input_path):
        super().__init__()
        self.is_image_processing = is_image_processing
        self.art_image_path = art_image_path
        self.input_path = input_path

    def run(self):
        # Perform the image or video processing
        if self.is_image_processing:
            ip = ImageProcessing(self.art_image_path, self.input_path)
            output_file_path = ip.process_image()
        else:
            vp = Video_Processing(self.art_image_path, self.input_path)
            output_file_path = vp.process_video()
        
        # Emit the finished signal with the output path
        self.finished.emit(output_file_path)
