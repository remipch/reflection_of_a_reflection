import cv2 as cv
import numpy as np

IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

CANVAS_WIDTH = IMAGE_WIDTH
CANVAS_HEIGHT = 400

LINE_COLOR = (0, 0, 0)


CANVAS_BORDERS = [
    [
        [0, 0],
        [CANVAS_WIDTH, 0],
        [CANVAS_WIDTH, CANVAS_HEIGHT],
        [0, CANVAS_HEIGHT],
        [0, 0],
    ]
]

# Manually extracted from https://commons.wikimedia.org/wiki/File:WP20Symbols_brain.svg
# Thank you Jasmina El Bouamraoui and Karabo Poppy Moletsane
# fmt: off
BRAIN_CURVES = [ [[298, 320],[295, 345],[282, 350],[263, 329],[252, 297],[250, 275],[207, 276],[167, 263],[153, 242],[151, 227]] , [[192, 237],[216, 222],[222, 207],[223, 200],[213, 191],[188, 190],[165, 202],[150, 229],[128, 226],[108, 217],[95, 196],[94, 167],[111, 137],[142, 109],[176, 89],[219, 74],[244, 70],[281, 72],[310, 81],[327, 89],[354, 105],[380, 131],[393, 151],[408, 190],[407, 233],[391, 263],[367, 279],[371, 285],[367, 298],[341, 317],[313, 321],[298, 321],[278, 306],[275, 293],[289, 283],[313, 283],[334, 282],[337, 275]] , [[373, 189],[362, 213],[347, 228],[308, 238],[267, 233],[255, 230],[217, 222]] , [[256, 231],[258, 221],[268, 210]] , [[222, 200],[241, 186],[264, 175],[282, 174],[303, 179],[309, 185]] , [[290, 174],[272, 160],[269, 147],[274, 130]] , [[327, 90],[308, 84],[291, 90],[273, 107]] , [[243, 72],[223, 83],[214, 102],[211, 120]] , [[198, 121],[212, 121],[231, 129]] , [[178, 90],[161, 113],[158, 139],[160, 158]] , [[143, 167],[160, 159],[174, 161]] ]
# fmt: on

image = 255 * np.ones(shape=[IMAGE_WIDTH, IMAGE_HEIGHT, 3], dtype=np.uint8)

# (x,y,scale) parameters are expressed relatively to a canvas of full size (CANVAS_WIDTH,CANVAS_HEIGHT)
# and 'canvas' parameters are applied after that
def drawCurves(curves, x, y, scale, canvas_x, canvas_y, canvas_scale, canvas_flipped):
    for curve in curves:
        points = np.array(curve, np.float32)
        points *= scale
        points += np.float32((x, y))
        if canvas_flipped:
            points = np.float32((CANVAS_WIDTH, 0)) + (points * np.float32((-1, 1)))
        points *= canvas_scale
        points += np.float32((canvas_x, canvas_y))
        cv.polylines(image, [np.int32(points)], False, LINE_COLOR, lineType=cv.LINE_AA)


# (center,radius) parameters are expressed relatively to a canvas of full size (CANVAS_WIDTH,CANVAS_HEIGHT)
# and 'canvas' parameters are applied after that
def drawEllipse(
    center_x,
    center_y,
    radius_x,
    radius_y,
    canvas_x,
    canvas_y,
    canvas_scale,
    canvas_flipped,
):
    if canvas_flipped:
        center_x = CANVAS_WIDTH - center_x
    center = (np.float32((center_x, center_y)) * canvas_scale) + np.float32(
        (canvas_x, canvas_y)
    )
    radius = np.float32((radius_x, radius_y)) * canvas_scale
    cv.ellipse(
        image,
        np.int32(center),
        np.int32(radius),
        0,
        0,
        360,
        LINE_COLOR,
        lineType=cv.LINE_AA,
    )


drawCurves(CANVAS_BORDERS, 0, 0, 1, 0, 0, 1, False)
drawCurves(BRAIN_CURVES, 0, 0, 0.5, 0, 0, 1, False)
drawCurves(BRAIN_CURVES, 0, 0, 0.5, 0, 0, 1, True)

drawCurves(CANVAS_BORDERS, 0, 0, 1, 100, 200, 0.5, False)
drawCurves(BRAIN_CURVES, 0, 0, 0.5, 100, 200, 0.5, False)
drawCurves(BRAIN_CURVES, 0, 0, 0.5, 100, 200, 0.5, True)

drawEllipse(50, 100, 25, 50, 0, 0, 1, False)
drawEllipse(50, 100, 25, 50, 0, 0, 1, True)
drawEllipse(50, 100, 25, 50, 100, 200, 0.5, False)
drawEllipse(50, 100, 25, 50, 100, 200, 0.5, True)


cv.imshow("reflection of a reflection", image)
cv.waitKey(0)
