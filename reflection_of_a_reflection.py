import cv2 as cv
import numpy as np

IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

image = 255 * np.ones(shape=[IMAGE_WIDTH, IMAGE_HEIGHT, 3], dtype=np.uint8)

cv.imshow("reflection of a reflection", image)
cv.waitKey(0)
