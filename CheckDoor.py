import cv2
import numpy as np
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
                help="Path to the video to be scanned")
args = vars(ap.parse_args())


def show_wait_destroy(winname, img):
    cv2.imshow(winname, img)
    cv2.moveWindow(winname, 500, 0)
    cv2.waitKey(0)
    cv2.destroyWindow(winname)


def door_is_open(lines):
    if lines is None:
        return True
    for i in range(lines.shape[0]):
        if 200 < lines[i][0][0] < 350 or 200 < lines[i][0][2] < 350:
            if abs(lines[i][0][1] - lines[i][0][3]) > 120:
                return False
    return True


print("reading video ...")

count = 0
answers = []
PATH_TO_VIDEO = args["video"]
cap = cv2.VideoCapture(PATH_TO_VIDEO)
skipSecond = 1  # you can change it
frameInSecond = int(cap.get(cv2.CAP_PROP_FPS))
skippedFrames = skipSecond * frameInSecond

count = 0
while True:
    frameId = int(round(cap.get(1)))
    ret, frame = cap.read()
    if ret:
        if frameId % skippedFrames == 0:

            frame = cv2.resize(frame, (500, 500))
            show_wait_destroy("Original", frame)

            """If a pixel gradient is higher than the upper threshold, the pixel is accepted as an edge If a pixel 
            gradient value is below the lower threshold, then it is rejected. If the pixel gradient is between the 
            two thresholds, then it will be accepted only if it is connected to a pixel that is above the upper 
            threshold. """
            edges = cv2.Canny(frame, 200, 250)
            show_wait_destroy("Canny", edges)

            lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100,
                                    minLineLength=100, maxLineGap=50)
            if lines is None:
                continue
            a, b, c = lines.shape
            for i in range(a):
                cv2.line(frame, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3,
                         cv2.LINE_AA)
                if (count==312):
                    print(labels[count])
                    show_wait_destroy("lines", frame)
            if door_is_open(lines):
                if labels[count] != '0\n':
                    print(count)
                answers.append('0\n')
            else:
                answers.append('1\n')

            count += 1
    else:
        break
cap.release()


