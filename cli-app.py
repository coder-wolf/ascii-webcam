import cv2
from rich import print as rprint
from rich.console import Console
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


def convertFrameGray(image, w, h):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.resize(gray, (w, h), interpolation= cv2.INTER_LINEAR)
    result = cv2.flip(result, 1)

    for rows in result:
        for pixel in rows:
            print(getASCII_Color(pixel), end='')
        print()
    time.sleep(0.25)
    clearConsole()


def convertFrameColor(image, w, h):
    console = Console()

    result = cv2.resize(image, (w, h), interpolation= cv2.INTER_LINEAR)
    cv2.flip(result, 1)
    for rows in result:
        for pixel in rows:
            gray_pixel = 0
            for val in pixel:
                gray_pixel += val
            gray_pixel = gray_pixel / 3
            b = pixel[0] 
            g = pixel[1] 
            r = pixel[2] 
            pixel_color = "rgb("+str(r)+","+str(g)+","+str(b)+")"

            console.print(getASCII_Color(gray_pixel), end='', style=pixel_color)
        print()
    time.sleep(0.23)
    clearConsole()


def AsciiWebcam():
    cam = cv2.VideoCapture(0)
    while True:
        check, frame = cam.read()

        #cv2.imshow('webcam feed', frame)

        size = os.get_terminal_size()
        convertFrameGray(frame, size[0], size[1])
        #convertFrameColor(frame, size[0], size[1])


        key = cv2.waitKey(1)
        if key == 27:
            break

    cam.release()
    #cv2.destroyAllWindows()

def main():
    #og_image = cv2.imread("ss.png")
    AsciiWebcam()
    #convertFrameColor(og_image)


if __name__ == '__main__':
    main()
