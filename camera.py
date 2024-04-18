# camera.py

import cv2
import PIL.Image
from PIL import Image
import numpy as np
import shutil
from time import sleep
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        ff11=open("video.txt","r")
        title=ff11.read()
        ff11.close()
    
        self.video = cv2.VideoCapture("static/upload/"+title)
        self.k=1

        self.largura_min = 80
        self.altura_min = 80
        self.offset = 6
        self.pos_linha = 550

        # FPS to vídeo
        self.delay = 60

        self.detec = []
        self.carros = 0
        self.subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

            
    def pega_centro(self,x, y, w, h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        cx = x + x1
        cy = y + y1
        return cx, cy   
        
        def __del__(self):
            self.video.release()
        
    
    def get_frame(self):
        ret, frame1 = self.video.read()
        tempo = float(1/self.delay)
        sleep(tempo) 
        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3, 3), 5)
        img_sub = self.subtracao.apply(blur)
        dilat = cv2.dilate(img_sub, np.ones((5, 5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        # The morphologyEx() of the method of the class Imgproc accepts src, dst, op, kernel as parameters
        dilatada = cv2.morphologyEx(dilat, cv2. MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilatada, cv2. MORPH_CLOSE, kernel)

        # OpenCV has findContour() function that helps in extracting the contours from the image.
        # It works best on binary images, so we should first apply thresholding techniques, Sobel edges, etc.
        contorno, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        # it will create a line
        # Parameters:
        # image: It is the image on which line is to be drawn.
        # start_point: It is the starting coordinates of line.
        # end_point: It is the ending coordinates of line.
        # color: It is the color of line to be drawn.
        # thickness: It is the thickness of the line in px.
        cv2.line(frame1, (25, self.pos_linha), (1200, self.pos_linha), (176, 130, 39), 2)
        for(i, c) in enumerate(contorno):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contorno = (w >= self.largura_min) and (h >= self.altura_min)
            if not validar_contorno:
                continue

            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            centro = self.pega_centro(x, y, w, h)
            self.detec.append(centro)
            cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

            for (x, y) in self.detec:
                if (y < (self.pos_linha + self.offset)) and (y > (self.pos_linha-self.offset)):
                    self.carros += 1
                    cv2.line(frame1, (25, self.pos_linha), (1200, self.pos_linha), (0, 127, 255), 3)
                    self.detec.remove((x, y))
                    print("No. of cars detected : " + str(self.carros))

        # cv2.putText() method is used to draw a text string on any image.
        # Parameters: image, text, org(coordinate), font, color, thickness
        cv2.putText(frame1, "VEHICLE COUNT : "+str(self.carros), (320, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 4)
        #cv2.imshow("Video Original", frame1)
        #cv2.imshow(" Detectar ", dilatada)
                    
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', frame1)
        return jpeg.tobytes()
