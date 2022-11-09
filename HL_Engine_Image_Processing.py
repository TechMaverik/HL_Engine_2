"""
HL_Engine_Image_Processing.py
Author:Akhil P Jacob
HLDynamic-Integrations
"""
import cv2
from PIL import Image
import numpy as np
from vidgear.gears.stabilizer import Stabilizer
from vidgear.gears import WriteGear


class ImageProcessingEngine:
    """HL_Engine Image processing class"""

    def take_picture(self, location, frame_name, camera):
        """Take picture"""
        try:
            camera = cv2.VideoCapture(camera)
            while True:
                _, image = camera.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imshow(frame_name, gray)
                if cv2.waitKey(1) & 0xFF == ord("x"):
                    cv2.imwrite(location, gray)
                    break
            camera.release()
            cv2.destroyAllWindows()
        except:
            return False

    def show_image(self, location, frame_name):
        """Show image"""
        try:
            img = cv2.imread(location)
            cv2.imshow(frame_name, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            return False

    def track_object_from_video(self, cascade_path, camera, frame_name,mode):
        """Track objects from video"""
        try:
            cap = cv2.VideoCapture(camera)
            faceCascade = cv2.CascadeClassifier(cascade_path)
            framer = frame_name
            while True:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                net = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                if mode=="Catch":
                    if len(net) >= 2:
                        return True
                for (x, y, w, h) in net:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow(framer, frame)
                if cv2.waitKey(1) & 0xFF == ord("x"):
                    break
            cap.release()
            cv2.destroyAllWindows()
        except:
            return False

    def stabilize_camera_input(self, camera):
        """Stable Camera Input"""
        try:
            stream = cv2.VideoCapture(camera)
            stab = Stabilizer()
            while True:
                (grabbed, frame) = stream.read()
                if not grabbed:
                    break
                stabilized_frame = stab.stabilize(frame)
                if stabilized_frame is None:
                    continue
                cv2.imshow("Stabilized Frame", stabilized_frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("x"):
                    break
            stab.clean()
            stream.release()
        except:
            return False

    def track_element_from_image(self, main_image_path, sample_image_to_track_path, result_image_path):
        """Track element from image"""
        try:
            img_rgb = cv2.imread(main_image_path)
            template = cv2.imread(sample_image_to_track_path)
            w, h = template.shape[:-1]
            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt, (pt[0] + h, pt[1] + w), (255, 0, 0), 1)
            cv2.imwrite(result_image_path, img_rgb)
            return True
        except:
            return False
