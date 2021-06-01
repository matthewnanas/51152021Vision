import socket
import numpy as np
import cv2 as cv

addr = ("127.0.0.1", 5820)
buf = 512
cap = cv.VideoCapture(0)
cap.set(3, 640) # Width
cap.set(4, 480) # Height
cap.set(cv.CAP_PROP_FPS, 20) # Framerate
cap.set(cv.CAP_PROP_EXPOSURE,-8) # Exposure
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(cap.isOpened()):
        ret, frame = cap.read()
        contrast = 0
        brightness = 50
        img = np.int16(frame)
        img = img * (contrast/127+1) - contrast + brightness
        img = np.clip(img, 0, 255)
        img = np.uint8(img)
        #Added stuff from here to if
        #frame = cv.cvtColor(frame, cv.IMREAD_GRAYSCALE)
        if ret:
            temp = cv.resize(img, (320, 240), interpolation=cv.INTER_LINEAR)
            output = cv.resize(temp, (320, 240), interpolation=cv.INTER_NEAREST)
            s.sendto(code, addr)
            data = output.tostring()
            for i in range(0, len(data), buf):
                s.sendto(data[i:i+buf], addr)
            #cv.imshow('send', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    s.close()
    cap.release()
    cv.destroyAllWindows()
