# Added scaling factor support for overlays
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def overlay_on_markers(image: np.ndarray, poster: np.ndarray) -> np.ndarray:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()
    corners, ids, _ = cv2.aruco.detectMarkers(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), aruco_dict, parameters=parameters)
    if ids is None:
        return image

    poster_h, poster_w = poster.shape[:2]
    source = np.float32([[0, 0], [poster_w, 0], [poster_w, poster_h], [0, poster_h]])

    for marker in corners:
        target = marker[0].astype(np.float32)
        matrix = cv2.getPerspectiveTransform(source, target)
        warped = cv2.warpPerspective(poster, matrix, (image.shape[1], image.shape[0]))
        mask = np.zeros_like(image, dtype=np.uint8)
        cv2.fillPoly(mask, [target.astype(np.int32)], (255, 255, 255))
        image = cv2.bitwise_or(cv2.bitwise_and(image, cv2.bitwise_not(mask)), warped)

    return image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Overlay a poster image onto detected ArUco markers.")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--poster", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    poster = cv2.imread(str(args.poster))
    if poster is None:
        raise FileNotFoundError(args.poster)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for image_path in sorted(args.input_dir.glob("*.jpg")):
        image = cv2.imread(str(image_path))
        if image is None:
            continue
        cv2.imwrite(str(args.output_dir / image_path.name), overlay_on_markers(image, poster))


if __name__ == "__main__":
    main()
