import argparse
import math
import os
import pickle
import sys
from typing import List, Tuple, Optional, Dict

import cv2
import numpy as np

from .drawer import getBoxFrames, getNeighborFrames, getTrajectoryFrames


DEMO_FRAMES = []


def loadContours() -> List[Dict]:
    with open(os.path.join("cached", "contours.pickle"), "rb") as file:
        allContours = pickle.load(file)

    return allContours


def loadBackground():
    return cv2.imread(os.path.join("cached", "background.jpg"))


def loadBoxImages() -> dict:
    with open(os.path.join("cached", "boxImages.pickle"), "rb") as file:
        boxImages = pickle.load(file)

    return boxImages


def overlaps(box1, box2) -> bool:
    minx1, maxx1, miny1, maxy1 = box1[0][0], box1[1][0], box1[0][1], box1[2][1]
    minx2, maxx2, miny2, maxy2 = box2[0][0], box2[1][0], box2[0][1], box2[2][1]

    if minx1 > maxx2 or maxx1 < minx2:
        return False
    if miny1 > maxy2 or maxy1 < miny2:
        return False
    return True


def combineAndWriteAbstraction(carTrajectories, length, frame_rate) -> list:
    mergedBoxes = [[] for _ in range(length)]

    background = loadBackground()
    newFrames = [background.copy() for _ in range(length)]

    boxImages = loadBoxImages()

    videoEndInd = 0

    for tInd, t in enumerate(carTrajectories):
        # print(tInd)
        for i in range(len(mergedBoxes)):  # looking for the insertion frame

            offset = t[0][0]

            allFramesCompatible = True
            for timeBox in t:
                tBox = timeBox[1:]
                insertionFrameInd = timeBox[0] - offset + i
                # if insertionFrameInd < 10:
                #     print(insertionFrameInd)
                frameMergedBoxes = mergedBoxes[insertionFrameInd]

                frameIntersects = False

                for mBox in frameMergedBoxes:

                    # print(mBox)
                    # print(tBox)

                    if overlaps(mBox, tBox):

                        frameIntersects = True
                        break

                if frameIntersects:
                    allFramesCompatible = False
                    break

            if allFramesCompatible:
                for timeBox in t:
                    box = timeBox[1:]
                    insertionFrameInd = timeBox[0] - offset + i
                    mergedBoxes[insertionFrameInd].append(box)
                    newFrames[insertionFrameInd][
                        box[0][1] : box[2][1], box[0][0] : box[1][0]
                    ] = boxImages[timeBox]
                    if insertionFrameInd > videoEndInd:
                        videoEndInd = insertionFrameInd
                break

    height, width, _ = newFrames[0].shape

    video = cv2.VideoWriter(
        "compressed_video.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        frame_rate,
        (width, height),
    )
    for frame in newFrames[: videoEndInd + 1]:
        # cv2.imshow('lol', frame)
        # cv2.waitKey()
        video.write(frame)
    video.release()
    return newFrames[: videoEndInd + 1]


def putTextWithCenter(demoFrame, text, center: Tuple[int, int], font_scale: float):
    font = cv2.FONT_HERSHEY_COMPLEX
    thickness = 2
    color = (0, 0, 0)

    size, _ = cv2.getTextSize(text, font, font_scale, thickness)

    cv2.putText(
        demoFrame,
        text,
        (center[0] - size[0] // 2, center[1] - size[1] // 2),
        font,
        font_scale,
        color,
        thickness,
    )


# ALL (ROW, COL)
PADDING = 35
DEMO_SHAPE = [0 * 2 + PADDING * 4, 0 * 2 + PADDING * 4, 3]
CENTER = [0 + 2 * PADDING, 0 + 2 * PADDING]


def createCenteredDemoFrame(frame, title="", footnote=""):
    demoFrame = np.full(DEMO_SHAPE, 255, dtype=np.uint8)
    half_h = frame.shape[0] // 2
    half_w = frame.shape[1] // 2

    demoFrame[
        CENTER[0] - half_h : CENTER[0] - half_h + frame.shape[0],
        CENTER[1] - half_w : CENTER[1] - half_w + frame.shape[1],
    ] = frame

    if title:
        putTextWithCenter(
            demoFrame, title, (CENTER[1], CENTER[0] - half_h - PADDING // 2), 1.5
        )
    if footnote:
        putTextWithCenter(
            demoFrame, footnote, (CENTER[1], CENTER[0] + half_h + 2 * PADDING), 1
        )
    return demoFrame


def create4PaneDemoFrame(panes, titles=("", "", "", ""), footnote=""):
    demoFrame = np.full(DEMO_SHAPE, 255, dtype=np.uint8)
    h = panes[0].shape[0]
    w = panes[0].shape[1]
    half_h = panes[0].shape[0] // 2
    half_w = panes[0].shape[1] // 2

    demoFrame[PADDING : PADDING + h, PADDING : PADDING + w] = panes[0]
    demoFrame[PADDING : PADDING + h, PADDING * 3 + w : PADDING * 3 + 2 * w] = panes[1]
    demoFrame[PADDING * 3 + h : PADDING * 3 + 2 * h, PADDING : PADDING + w] = panes[2]
    demoFrame[
        PADDING * 3 + h : PADDING * 3 + 2 * h, PADDING * 3 + w : PADDING * 3 + 2 * w
    ] = panes[3]

    putTextWithCenter(demoFrame, titles[0], (PADDING + half_w, PADDING), 0.8)
    putTextWithCenter(demoFrame, titles[1], (PADDING * 3 + half_w + w, PADDING), 0.8)
    putTextWithCenter(demoFrame, titles[2], (PADDING + half_w, PADDING * 3 + h), 0.8)
    putTextWithCenter(
        demoFrame, titles[3], (PADDING * 3 + half_w + w, PADDING * 3 + h), 0.8
    )

    if footnote:
        putTextWithCenter(
            demoFrame, footnote, (PADDING * 2 + w, PADDING * 4 + 2 * h), 0.8
        )

    # if title:
    #     putTextWithCenter(demoFrame, title, (CENTER[1], CENTER[0] - half_h - PADDING // 2), 1.5)
    # if footnote:
    #     putTextWithCenter(demoFrame, footnote, (CENTER[1], CENTER[0] + half_h + 2 * PADDING), 1)
    return demoFrame


def demoOriginal(video_file) -> list:
    video = cv2.VideoCapture(video_file)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    frames = []
    while 1:
        ret, frame = video.read()

        # cv2.imshow("demo", demoFrame)
        if ret:
            frames.append(frame)
        else:
            break
    video.release()

    demoFrame = createCenteredDemoFrame(
        frames[0], "Original Video", "paused, any key to play"
    )
    cv2.imshow("demo", demoFrame)
    DEMO_FRAMES.append(demoFrame)
    cv2.waitKey()

    for frame in frames[1:]:

        demoFrame = createCenteredDemoFrame(
            frame, "Original Video", "ESC to finish video"
        )

        cv2.imshow("demo", demoFrame)
        DEMO_FRAMES.append(demoFrame)
        k = cv2.waitKey(1000 // 30)
        if k & 0xFF == 27:
            break

    demoFrame = createCenteredDemoFrame(
        frames[0], "Original Video", "any key to proceed"
    )
    cv2.imshow("demo", demoFrame)
    DEMO_FRAMES.append(demoFrame)
    cv2.waitKey()

    return frames


def trajectory_algorithm_four_pane_demo(
    allBoxes, allNeighbors, trajectories, carTrajectories, videoFrames, length
):
    boxFrames = getBoxFrames(allBoxes, videoFrames)
    neighborFrames = getNeighborFrames(allBoxes, allNeighbors, videoFrames)
    trajectoryFrames = getTrajectoryFrames(trajectories, videoFrames)
    carTrajectoryFrames = getTrajectoryFrames(carTrajectories, videoFrames)

    # select frame from the middle to demo

    demoFrame = None
    for i in range(int(length * 0.555), len(videoFrames)):
        demoFrame = create4PaneDemoFrame(
            [
                boxFrames[i],
                neighborFrames[i],
                trajectoryFrames[i],
                carTrajectoryFrames[i],
            ],
            (
                "1.Non-background boxes",
                "2.Neighboring boxes between frames",
                "3.Constructed trajectories",
                "4.Filter noise by trajectory length",
            ),
            "hold any key to play, ESC to proceed",
        )

        cv2.imshow("demo", demoFrame)
        DEMO_FRAMES.append(demoFrame)
        k = cv2.waitKey() & 0xFF
        if k == 27:
            break


def twoPaneDemo(videoFrames, compressedFrames, video_file, width, height):
    for i, frame in enumerate(videoFrames):

        demoFrame = np.full(DEMO_SHAPE, 255, dtype=np.uint8)
        h = frame.shape[0]
        w = frame.shape[1]
        half_h = frame.shape[0] // 2
        half_w = frame.shape[1] // 2

        demoFrame[PADDING * 3 + h : PADDING * 3 + 2 * h, PADDING : PADDING + w] = frame
        if i < len(compressedFrames):
            rightsideFrame = compressedFrames[i]
        else:
            rightsideFrame = np.zeros((height, width, 3), dtype=np.uint8)

        demoFrame[
            PADDING * 3 + h : PADDING * 3 + 2 * h, PADDING * 3 + w : PADDING * 3 + 2 * w
        ] = rightsideFrame

        frameDiff = "Frame count: %d -> %d" % (len(videoFrames), len(compressedFrames))
        sizeDiff = "Video size: %.1f MB -> %.1f MB" % (
            os.path.getsize(video_file) / 1000000,
            os.path.getsize("compressed_video.mp4") / 1000000,
        )
        putTextWithCenter(demoFrame, "Result Comparison", (PADDING + w, PADDING), 1)

        putTextWithCenter(demoFrame, frameDiff, (PADDING + w, PADDING + h // 3), 0.8)

        putTextWithCenter(demoFrame, sizeDiff, (PADDING + w, PADDING + h * 2 // 3), 0.8)

        putTextWithCenter(
            demoFrame, "original", (PADDING + half_w, PADDING * 3 + h), 0.8
        )
        putTextWithCenter(
            demoFrame, "abstracted", (PADDING * 3 + half_w + w, PADDING * 3 + h), 0.8
        )

        putTextWithCenter(
            demoFrame, "ESC to end", (PADDING * 2 + w, PADDING * 4 + 2 * h), 0.8
        )

        cv2.imshow("demo", demoFrame)
        DEMO_FRAMES.append(demoFrame)
        k = cv2.waitKey(1000 // 30) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()


def main(args):
    global DEMO_SHAPE, CENTER

    video_file = args.video

    assert os.path.isfile(video_file), "Can not find specified video file"

    video = cv2.VideoCapture(video_file)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video.get(cv2.CAP_PROP_FPS)

    DEMO_SHAPE[0] = height * 2 + PADDING * 4
    DEMO_SHAPE[1] = width * 2 + PADDING * 4

    CENTER[0] = height + 2 * PADDING
    CENTER[1] = width + 2 * PADDING

    if args.mode == "abstract":

        allBoxes = processVideo(video_file, width, height, length)
        # allContours = loadContours()

        allNeighbors = computeAllNeighbors(allBoxes)

        trajectories = getTrajectories(allBoxes, allNeighbors)

        # keep those trajectories that are longer than 1 second (for a 30 fps video)
        bound = 30
        carTrajectories = list(filter(lambda x: len(x) > bound, trajectories))

        print("%d car trajectories found" % len(carTrajectories))

        # generate gifs of individual trajectories
        # generateFreakingGIFs(carTrajectories)

        # get average velocity across the video
        # vels = getBlockVels(allBoxes, allNeighbors)

        combineAndWriteAbstraction(carTrajectories, len(allBoxes), frame_rate)

    else:  # demo
        frames = demoOriginal(video_file)

        # shows background subtraction progress and subtracted background
        allBoxes = processVideo(video_file, width, height, length, demo=True)

        allNeighbors = computeAllNeighbors(allBoxes)

        trajectories = getTrajectories(allBoxes, allNeighbors)

        bound = 30
        carTrajectories = list(filter(lambda x: len(x) > bound, trajectories))
        compressedFrames = combineAndWriteAbstraction(
            carTrajectories, len(allBoxes), frame_rate
        )

        trajectory_algorithm_four_pane_demo(
            allBoxes, allNeighbors, trajectories, carTrajectories, frames, length
        )

        twoPaneDemo(frames, compressedFrames, video_file, width, height)

        demo_video = cv2.VideoWriter(
            "demo_video.mp4",
            cv2.VideoWriter_fourcc(*"mp4v"),
            frame_rate,
            (DEMO_SHAPE[1], DEMO_SHAPE[0]),
        )
        for frame in DEMO_FRAMES:
            demo_video.write(frame)
        demo_video.release()


def computeBoxMSE(box1, box2):
    s = 0
    for i in range(4):
        s += (box1[i][0] - box2[i][0]) ** 2 + (box1[i][1] - box2[i][1]) ** 2

    return math.sqrt(s) / 4


def computeMinNeighborForBox(box, nextFrameBoxes, bound, neighbor_scores) -> List[int]:
    """
    error := mse(corresponding vertex distance), boxes within an error of bound will be considered neighbors

    :param box:
    :param nextFrameBoxes:
    :param bound:
    """
    neighbors = []
    # counter = 0

    minNeighbor = None
    minMSE = None
    for i, checkingBox in enumerate(nextFrameBoxes):

        mse = computeBoxMSE(box, checkingBox)
        if mse <= bound:

            if minMSE is not None:
                if mse <= minMSE:
                    minMSE = mse
                    minNeighbor = i

            else:
                minMSE = mse
                minNeighbor = i

    if minNeighbor is not None:
        if minNeighbor in neighbor_scores:
            if minMSE < neighbor_scores[minNeighbor]:
                neighbor_scores[minNeighbor] = minMSE
                return [minNeighbor]
        else:
            neighbor_scores[minNeighbor] = minMSE
            return [minNeighbor]

    return []


# empirical bound: 60
def computeAllNeighbors(allBoxes, bound=60) -> List[List[List[int]]]:
    allNeighbors = []

    for i in range(len(allBoxes) - 1):
        currentFrameBoxes, nextFrameBoxes = allBoxes[i : i + 2]

        frameNeighbors = []

        neighbor_scores = {}
        for box in currentFrameBoxes:
            boxNeighbor = computeMinNeighborForBox(
                box, nextFrameBoxes, bound, neighbor_scores
            )
            frameNeighbors.append(boxNeighbor)
        allNeighbors.append(frameNeighbors)

    return allNeighbors


def getTrajectories(allBoxes, allNeighbors):
    trajectories = []
    trajectoryHeads = dict()

    # includedBoxeInds = set()

    for frameInd in range(len(allBoxes) - 1):
        frameBoxes = allBoxes[frameInd]
        for boxInd, box in enumerate(frameBoxes):

            timeBox = (frameInd,) + box
            if allNeighbors[frameInd][boxInd]:

                futureTimeBox = (frameInd + 1,) + allBoxes[frameInd + 1][
                    allNeighbors[frameInd][boxInd][0]
                ]
                if timeBox in trajectoryHeads:
                    trajectories[trajectoryHeads[timeBox]].append(futureTimeBox)
                    trajectoryHeads[futureTimeBox] = trajectoryHeads[timeBox]
                    trajectoryHeads.pop(timeBox)
                else:
                    trajectories.append([timeBox, futureTimeBox])
                    trajectoryHeads[futureTimeBox] = len(trajectories) - 1

    return trajectories


def retrieveComputed() -> Tuple[Optional[List[List[Tuple]]], bool]:
    file = os.path.join("cached", "trafficVideoBoxes.pickle")
    contourFile = os.path.join("cached", "contours.pickle")
    backgroundImg = os.path.join("cached", "background.jpg")
    boxImages = os.path.join("cached", "boxImages.pickle")

    if (
        os.path.isfile(file)
        and os.path.isfile(contourFile)
        and os.path.isfile(backgroundImg)
        and os.path.isfile(boxImages)
    ):
        print("cached result found, skipping GMG background detection")
        with open(file, "rb") as file:
            allBoxes = pickle.load(file)
        return allBoxes, False
    else:
        print("cached result not found, proceeding to GMG background detection")
        return None, True


def processVideo(
    video_file, width, height, length, demo=False
) -> List[
    List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]]
]:
    """
    Get non-background bounding boxes every frame by GMG algorithm.
    Some initial filtering is used to filter boxes too small, (smaller than 100 square pixels)

    in the meantime, both background and contours are extracted and cached for later use.

    :return: boxes
    """

    allContrours = []

    allBoxes, caching = retrieveComputed()
    if allBoxes is None or demo:
        allBoxes = []
        caching = True
    else:
        return allBoxes

    assert os.path.isfile(video_file), "video file not found"

    video = cv2.VideoCapture(video_file)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    demoFrame = np.full((height * 2, width * 2, 3), 255, dtype=np.uint8)

    boxImages = dict()

    backgroundFrequencies = [[dict() for _ in range(width)] for _ in range(height)]
    background = np.full((height, width, 3), 255, dtype=np.uint8)
    counter = 0

    sampling_min = int(0.136 * length)
    sampling_max = int(0.2 * length)

    while 1:
        ret, frame = video.read()

        print(
            "Video processing progress: %d\r" % ((counter + 1) * 100 / length), end=""
        )

        if ret:
            frameBoxes = []
            frameContours = dict()

            fgmask = fgbg.apply(frame)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            _, th1 = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
            a, contours, *_ = cv2.findContours(
                th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )  # showing the masked result
            # if counter // 50 == 0:
            if sampling_min <= counter <= sampling_max:

                bgmask = np.logical_not(fgmask)

                # cv2.waitKey()
                bg = cv2.bitwise_and(frame, frame, mask=bgmask.astype(np.uint8))
                if demo:
                    demoFrame = createCenteredDemoFrame(
                        bg,
                        "Processing Video: %d%%" % ((counter + 1) * 100 / length),
                        "sampling background",
                    )

                for r in range(height):
                    for c in range(width):
                        if bgmask[r][c]:
                            p = tuple(bg[r][c])
                            k = backgroundFrequencies[r][c]
                            if p in k:
                                k[p] += 1
                            else:
                                k[p] = 1
            elif demo:
                showingFrame = np.full((height, width, 3), 255, dtype=np.uint8)

                demoFrame = createCenteredDemoFrame(
                    showingFrame,
                    "Processing Video: %d%%" % ((counter + 1) * 100 / length),
                    "",
                )
            if demo:
                cv2.imshow("demo", demoFrame)
                DEMO_FRAMES.append(demoFrame)
                cv2.waitKey(1)

            for i in range(len(contours)):
                if len(contours[i]) >= 5:

                    # geting the 4 points of rectangle

                    x, y, w, h = cv2.boundingRect(contours[i])
                    if w * h >= 100:
                        # upper-left upper-right lower-left lower-right
                        box = ((x, y), (x + w, y), (x, y + h), (x + w, y + h))
                        frameBoxes.append(box)
                        boxImages[(counter,) + box] = frame[y : y + h, x : x + w]
                        frameContours[box] = contours[i]
            allContrours.append(frameContours)
            allBoxes.append(frameBoxes)

        else:
            break
        counter += 1
    print("Video processing progress: 100")

    video.release()

    for r in range(height):
        for c in range(width):
            px = tuple(backgroundFrequencies[r][c].items())
            if px:
                maxP = max(
                    tuple(backgroundFrequencies[r][c].items()), key=lambda x: x[1]
                )[0]
            else:
                maxP = (255, 255, 255)
            background[r][c] = maxP

    if caching:
        if not os.path.exists("cached"):
            os.makedirs("cached")
        filename = os.path.join("cached", "trafficVideoBoxes.pickle")

        contoursFilename = os.path.join("cached", "contours.pickle")
        backgroundFilename = os.path.join("cached", "background.jpg")
        boxImagesFilename = os.path.join("cached", "boxImages.pickle")

        with open(filename, "wb") as file:
            pickle.dump(allBoxes, file)

        with open(contoursFilename, "wb") as file:
            pickle.dump(allContrours, file)

        with open(boxImagesFilename, "wb") as file:
            pickle.dump(boxImages, file)

        # print(background[0:10, 0:10])
        cv2.imwrite(backgroundFilename, background)

        print("bounding boxes, contours, extracted background cached for later use")

        print("video frame count: %d" % length)

    return allBoxes


def cmd_entry(argv=sys.argv):
    # todo: fill command line functionality

    parser = argparse.ArgumentParser(
        description="Video Abstraction By Bounding Box And Trajectory"
    )

    # todo: demo on arbitrary video. Remove average analysis
    parser.add_argument("video", help="The video file you want to do abstraction on")

    parser.add_argument(
        "-m",
        "--mode",
        default="abstract",
        type=str,
        required=False,
        choices=("abstract", "demo"),
        help="'abstract' to do video abstraction. 'demo' to include show intermediate steps.",
    )

    argv = parser.parse_args(argv[1:])

    main(argv)
