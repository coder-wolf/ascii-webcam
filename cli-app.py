import cv2
import os
import time 
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def getASCII_Color(color):
    density = "Ñ@#W$9876543210?!abc;:+=-,._   ";
    density = density[::-1]

    density = '       .:-i|=+%O#@'
    return density[int(color/len(density))]


def convertSingleFrame(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.resize(gray, (1250,230), interpolation= cv2.INTER_LINEAR)
    cv2.flip(result, 1)

    for rows in result:
        for pixel in rows:
            print(getASCII_Color(pixel), end='')
        print()



def AsciiWebcam():
    cam = cv2.VideoCapture(0)
    while True:
        check, frame = cam.read()

        #cv2.imshow('webcam feed', frame)

        convertSingleFrame(frame)

        time.sleep(0.3)
        clearConsole()

        key = cv2.waitKey(1)
        if key == 27:
            break

    cam.release()
    #cv2.destroyAllWindows()

def main():
    # og_image = Image.open('mia.png')
    AsciiWebcam()
    # convertSingleFrame(og_image)


if __name__ == '__main__':
    main()
