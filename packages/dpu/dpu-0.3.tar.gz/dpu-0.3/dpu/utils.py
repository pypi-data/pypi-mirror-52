import os
from typing import Tuple, Dict

import cv2
import numpy as np


__all__ = [
    "get_augmentation_function_names", 
    "imshow",
    "get_face_part_to_landmark_indices",
]


def get_augmentation_function_names() -> Tuple[str]:
    return (
        "super_pixels",
        "change_colorspace",
        "grayscale",
        "gaussian_blue",
        "average_blue",
        "median_blue",
        "sharpen",
        "embos",
        "edge_detect",
        "directed_edge_detect",
        "add",
        "add_elementwise",
        "additive_gaussian_noise",
        "multiply",
        "multiply_elementwise",
        "dropout",
        "coarse_dropout",
        "invert",
        "constant_normalization",
        "elastic_transformation",
    )


def imshow(image: np.ndarray) -> None:
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_face_part_to_landmark_indices() -> Dict[str, tuple]:
    return {
        "chin": tuple(range(17)),
        "leyebrow": tuple(range(17, 22)),
        "reyebrow": tuple(range(22, 27)),
        "vnose": tuple(range(27, 31)),
        "hnose": tuple(range(31, 36)),
        "nose": tuple(range(27, 36)),
        "leye": tuple(range(36, 42)),
        "reye": tuple(range(42, 48)),
        "omouth": tuple(range(48, 60)),
        "imouth": tuple(range(60, 68)),
        "mouth": tuple(range(48, 68))
    }


# def get_new_face_part_to_landmark_indices(parts_order):
#     parts_indices = get_face_part_to_landmark_indices()
#     new_indices = {}
#     index = 0
#     for part in parts_order:
# 	new_indices[part] = list(range(index, index+len(parts_indices[part])))
# 	index += len(self.parts_indices[part]) 
#     return new_indices
