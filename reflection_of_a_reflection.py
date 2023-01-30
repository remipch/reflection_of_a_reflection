import cv2 as cv
import numpy as np

# Virtual canvas size in which levels are drawn
# they are scaled after that depending on actual level depth and window size
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800

# Output image resolution
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

IMAGE_SCALE = IMAGE_WIDTH / CANVAS_WIDTH

BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (5, 5, 5)

image = np.zeros(shape=[IMAGE_WIDTH, IMAGE_HEIGHT, 3], dtype=np.uint8)

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

MIRROR_CURVES = [
    [
        [50, 50],
        [500, 200],
        [500, 600],
        [50, 750],
        [50, 50],
    ]
]

# (x,y,scale) parameters are expressed in virtual canvas (CANVAS_WIDTH,CANVAS_HEIGHT)
# and 'canvas' parameters are applied after that
# (canvas_scale=1 means that canvas take whole image width)
def drawCurves(curves, x, y, scale, canvas_x, canvas_y, canvas_scale, canvas_flipped):
    for curve in curves:
        points = np.array(curve, np.float32)
        points *= scale
        points += np.float32((x, y))
        if canvas_flipped:
            points = np.float32((CANVAS_WIDTH, 0)) + (points * np.float32((-1, 1)))
        points *= canvas_scale
        points += np.float32((canvas_x, canvas_y))
        cv.polylines(
            image,
            [np.int32(points * IMAGE_SCALE)],
            False,
            LINE_COLOR,
            lineType=cv.LINE_AA,
        )


# (center,radius) parameters are expressed in virtual canvas (CANVAS_WIDTH,CANVAS_HEIGHT)
# and 'canvas' parameters are applied after that
# (canvas_scale=1 means that canvas take whole image width)
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
    center = np.float32((center_x, center_y)) * canvas_scale
    center += np.float32((canvas_x, canvas_y))
    radius = np.float32((radius_x, radius_y)) * canvas_scale
    cv.ellipse(
        image,
        np.int32(center * IMAGE_SCALE),
        np.int32(radius * IMAGE_SCALE),
        0,
        0,
        360,
        LINE_COLOR,
        lineType=cv.LINE_AA,
    )


# Compte the offset to apply to a given level of canvas_scale
# to recenter progressively on the next level while zooming in
def computeOffsetToRecenter(next_level_x, canvas_scale):
    return next_level_x * (
        (INTER_LEVEL_SCALE - canvas_scale) / (INTER_LEVEL_SCALE - 1) - canvas_scale
    )


def drawBrainLevel(canvas_x, canvas_y, canvas_scale, canvas_flipped):
    drawCurves(
        CANVAS_BORDERS, 0, 0, 1, canvas_x, canvas_y, canvas_scale, canvas_flipped
    )
    drawCurves(
        CANVAS_BORDERS, 480, 90, 1 / 3, canvas_x, canvas_y, canvas_scale, canvas_flipped
    )
    drawCurves(
        BRAIN_CURVES, -30, 420, 1, canvas_x, canvas_y, canvas_scale, canvas_flipped
    )
    drawEllipse(430, 560, 20, 20, canvas_x, canvas_y, canvas_scale, canvas_flipped)
    drawEllipse(500, 480, 40, 40, canvas_x, canvas_y, canvas_scale, canvas_flipped)
    drawEllipse(650, 220, 340, 200, canvas_x, canvas_y, canvas_scale, canvas_flipped)


def drawMirrorLevel(canvas_x, canvas_y, canvas_scale, canvas_flipped):
    if canvas_scale < MINIMAL_LEVEL_SCALE:
        return
    next_level_flipped_x = 110
    next_level_x = 620
    next_level_y = 260

    if canvas_flipped:
        next_level_flipped_x = (
            CANVAS_WIDTH - next_level_flipped_x - CANVAS_WIDTH / INTER_LEVEL_SCALE
        )
        next_level_x = CANVAS_WIDTH - next_level_x - CANVAS_WIDTH / INTER_LEVEL_SCALE

    if canvas_scale > 1:
        canvas_x += computeOffsetToRecenter(next_level_flipped_x, canvas_scale)
        canvas_y += computeOffsetToRecenter(next_level_y, canvas_scale)
    next_level_flipped_x = canvas_x + next_level_flipped_x * canvas_scale
    next_level_x = canvas_x + next_level_x * canvas_scale
    next_level_y = canvas_y + next_level_y * canvas_scale
    drawCurves(
        CANVAS_BORDERS,
        0,
        0,
        1,
        canvas_x,
        canvas_y,
        canvas_scale,
        canvas_flipped,
    )
    drawCurves(
        MIRROR_CURVES,
        0,
        0,
        1,
        canvas_x,
        canvas_y,
        canvas_scale,
        canvas_flipped,
    )
    drawMirrorLevel(
        next_level_flipped_x,
        next_level_y,
        canvas_scale / INTER_LEVEL_SCALE,
        not canvas_flipped,
    )
    drawMirrorLevel(
        next_level_x, next_level_y, canvas_scale / INTER_LEVEL_SCALE, canvas_flipped
    )

INTER_LEVEL_SCALE = 3
FRAME_PER_LEVEL = 8
FRAME_DURATION_MS = 0  # set 0 to wait a key press
INTER_FRAME_SCALE = INTER_LEVEL_SCALE / FRAME_PER_LEVEL
MINIMAL_LEVEL_SCALE = 0.01

frame_index = 0

main_canvas_flipped = False

for main_level_index in range(len(LEVELS)):
    for level_frame_index in range(FRAME_PER_LEVEL):
        main_level_scale = (
            1 + (INTER_LEVEL_SCALE - 1) * level_frame_index / FRAME_PER_LEVEL
        )
        cv.rectangle(
            image, (0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND_COLOR, cv.FILLED
        )

        print(
            f"paint frame {frame_index} ; level {main_level_index} ; scale {main_level_scale}",
            flush=True,
        )
        drawMirrorLevel(0, 0, main_level_scale, main_canvas_flipped)

        cv.imshow("reflection of a reflection", image)

        # Wait and test escape key
        if cv.waitKey(FRAME_DURATION_MS) == 27:
            exit(1)
        frame_index += 1
    main_canvas_flipped = not main_canvas_flipped
