import cv2,os,urllib.request
import numpy as np
from django.conf import settings

face_detection_videocam = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR, 
                            'static/xml/haarcascade_frontalface_default.xml'))

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()

	def get_heart_rate(self):
		cap = self.video
		count=0
		i = 0
		arr = [0, 0, 0]
		while True:
			ret, frame = cap.read()
			cv2.imshow('Frame', frame)
			
			b = frame[:, :, :1]
			g = frame[:, :, 1:2]
			r = frame[:, :, 2:]

			b_mean = np.mean(b)
			g_mean = np.mean(g)
			r_mean = np.mean(r)
			
			arr.append(b_mean)
			
			if arr[-2] > arr[-1] and arr[-2] > arr[-3]:
				count+=1
				print(i, count)
					
			print(i, b_mean, g_mean, r_mean)
			i+=1
				
			k = cv2.waitKey(27) & 0xff
			if k == 27 or i==500:
				break
		cap.release()
		cv2.destroyAllWindows()
		return count