"""image_processing_operation_sample"""
from HL_Engine_2 import HL_Engine_Image_Processing


class ImageProcess:
    """Image processing"""

    def __init__(self):
        self.processor = HL_Engine_Image_Processing.ImageProcessingEngine()  # Initializing the ImageProcessing Class from HL_Engine2

    def take_picture(self):
        """take picture"""
        self.processor.take_picture("SampleImage.jpg", "Sample Picture", 0)

    def show_image(self):
        """show image"""
        self.processor.show_image("SampleImage.jpg", "SNAPSHOT")

    def face_detection(self):
        """face detection"""
        self.processor.track_object_from_video(
            "HL_Engine_2/HL_Cascades/haarcascade_frontalface_default.xml",
            0,
            "Live Video",
            "",
        )

    def track_object(self):
        """track bottle"""
        result = self.processor.track_element_from_image("SampleImage.jpg", "1.JPG", "TrackedPath.jpg")
        print(result)


"""Action Calls"""
IP = ImageProcess()
# IP.take_picture()
# IP.show_image()
# IP.track_object()
# IP.face_detection()
