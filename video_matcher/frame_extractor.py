"""Utilities for extracting frame features from videos."""

from typing import List
import cv2


def extract_frame_features(video_path: str, stride: int = 1) -> List[float]:
    """Extract simple frame features from ``video_path``.

    Parameters
    ----------
    video_path:
        Path to the video file.
    stride:
        Interval between frames. Defaults to 1 (use every frame).

    Returns
    -------
    List[float]
        Sequence of grayscale average intensities for each sampled frame.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")

    features = []
    index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if index % stride == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            features.append(float(gray.mean()))
        index += 1

    cap.release()
    return features
