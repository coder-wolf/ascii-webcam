import os
import time
import sys
import cv2

from rich.console import Console


def clearConsole():
    command = 'clear'
    
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    
    os.system(command)


def getASCII_Color(color):
    #density = "Ñ@#W$9876543210?!abc;:+=-,._   "
    #density = density[::-1]

    density = '       .:-i|=+%\O#@'
    
    return density[int(color/len(density))]


def convertFrameGray(image, w, h):
    clearConsole()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.resize(gray, (w, h), interpolation=cv2.INTER_LINEAR)
    #result = cv2.flip(result, 1)

    for rows in result:
        for pixel in rows:
            print(getASCII_Color(pixel), end='')
        print()    
    time.sleep(0.25)


def convertFrameColor(image, w, h, ch='a'):
    clearConsole()
    
    console = Console()
    # TODO keep the aspect ratio.

    # result = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)
    result = cropKeepingAspectRatio(image)
    #result = cv2.flip(result, 1)
    
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

            console.print(ch, end='', style=pixel_color)
            #console.print(getASCII_Color(gray_pixel), end='', style=pixel_color)
        print()

    time.sleep(0.35)


def AsciiWebcam(arg, ch):
    cam = cv2.VideoCapture(0)
    while True:
        check, frame = cam.read()
        #cv2.imshow('webcam feed', frame)
        frame = cv2.flip(frame, 1)
        size = os.get_terminal_size()

        if arg == '-c' or arg == 'color' or arg == 'col' or arg == '--color' or arg == '--c' or arg == '-color':
            convertFrameColor(frame, size[0], size[1], ch=ch)
        else:
            convertFrameGray(frame, size[0], size[1])

        key = cv2.waitKey(1)
        
        if key == 27:
            break

    cam.release()
    # cv2.destroyAllWindows( )


def cropKeepingAspectRatio(image):
    size = os.get_terminal_size()
    
    window_w = size[0]
    window_h = size[1]

    img_w = image.shape[0]
    img_h = image.shape[1]
    
    image_aspect_ratio = img_w / img_h

    crop_w = w
    crop_h = h

    result = cv2.resize(image, (int(crop_w), int(crop_h)), interpolation=cv2.INTER_LINEAR)
    
    return result


def saveWebcamVideo():
    pass


def main():
    arg = "----"
    second = 'a'

    if len(sys.argv) >= 3:
        second = sys.argv[2]
    if len(sys.argv) >= 2:
        arg = sys.argv[1]

    if arg == 'image' or arg == '--image' or arg == '-image':
        if second != 'a':
            size = os.get_terminal_size()
            img = cv2.imread(second)
            convertFrameColor(img, size[0], size[1])
        else:
            print("Error: No file input")

    else:
        clearConsole()
        AsciiWebcam(arg, second)


if __name__ == '__main__':
    
    main()
