# Neural Style Transfer Application 🚀

This is a PyQt-based application for performing Neural Style Transfer on images, videos, and live camera feeds. It leverages **TensorFlow Hub** for pre-trained models and **CUDA** for accelerated processing on compatible GPUs.

## Features

- **Image Styling:** Apply artistic styles to static images.
- **Video Styling:** Process and stylize videos frame by frame efficiently.
- **Live Camera Feed:** Real-time style transfer for live camera input.
- **Model Flexibility:** Select models from TensorFlow Hub or your system.
- **Interactive UI:** 
  - Select input images and videos via file dialogs.
  - Preview and process results directly in the application.
  - Output display with zoom for images and playback for videos.
- **Processing Status:** Animated popups indicating processing progress.

## Installation

### Prerequisites
- **Python 3.8+**
- **CUDA Toolkit** (if using GPU acceleration)
- Required Python libraries (install via `requirements.txt`)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/jayeshrdeotalu/Nest-Neural-Style-Transfer.git   
   cd Nest-Neural-Style-Transfer
2. Install the dependencies:
   ```bash
     pip install -r requirements.txt
3. Ensure CUDA is installed and properly configured for GPU acceleration (optional).

### Usage
1. Run the application:
   ```bash
   python app.py

2. Select the operation:
  - **Style an Image:** Choose an input image and a style model.
  - **Style a Video:** Select a video and apply the chosen style.

3. Process the selected input:
- Click on "Process the Styling" to apply the effect.
- View the results directly in the application.

4. Save outputs:
- Output is saved in the same input folder.

### License
  This project is licensed under the MIT License.

### Acknowledgments
-   TensorFlow Hub: For providing pre-trained models.
-   PyQt: For the UI framework.
-   CUDA: For GPU acceleration.
