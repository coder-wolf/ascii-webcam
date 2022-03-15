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
    # density = "Ñ@#W$9876543210?!abc;:+=-,._   "
    #density = density[::-1]

    density = '       .:-i|=+%\O#@'

    return density[int(color/len(density))]


def convertFrameGray(image):
    clearConsole()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.resize(gray, os.get_terminal_size(),
                        interpolation=cv2.INTER_LINEAR)
    #result = cv2.flip(result, 1)

    for rows in result:
        for pixel in rows:
            print(getASCII_Color(pixel), end='')
        print()
    time.sleep(0.25)


def convertFrameColor(image, ch='a'):
    clearConsole()

    console = Console()

    result = cv2.resize(image, os.get_terminal_size(),
                        interpolation=cv2.INTER_LINEAR)
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

        if arg[-1:] == 'c' or arg[-3:] == 'col' or arg[-5:] == 'color':
            convertFrameColor(frame, ch=ch)
        else:
            convertFrameGray(frame)

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
    window_aspect_ratio = window_w / window_h

    # Stretching image a bit on the side, because, the fonts aren't exactly square
    # They are a bit narrower than square shape.
    image_aspect_ratio /= 2.1

    crop_w = window_w
    crop_h = window_h
    # there can be two problems that might occur
    # 1. The width is more stretched
    # 2. The height is more stretched

    # Let's solve each of them.
    # 1. Solution:
    #    reduce the width, down to the amount when it matches the aspect ratio
    if window_aspect_ratio > image_aspect_ratio:
        # Case 1
        crop_w = window_w
        crop_h = crop_w * image_aspect_ratio
        # pass
    else:  # TODO fix needed here. Not working as expected.
        crop_h = window_h
        crop_w = crop_h * image_aspect_ratio
        # pass

    # 2. Solution:
    #    reduce the height, down to the amount when it matches the aspect ratio

    result = cv2.resize(image, (int(crop_w), int(crop_h)),
                        interpolation=cv2.INTER_LINEAR)

    return result


def saveWebcamVideo():
    # TODO complete this function
    pass


def main():
    arg = "----"
    second = 'a'

    if len(sys.argv) >= 3:
        second = sys.argv[2]
    if len(sys.argv) >= 2:
        arg = sys.argv[1]

    if arg[-5:] == 'image':
        if second != 'a':
            size = os.get_terminal_size()
            img = cv2.imread(second)
            convertFrameColor(img, )
        else:
            print("Error: No file input")

    else:
        clearConsole()
        AsciiWebcam(arg, second)


if __name__ == '__main__':

    main()
