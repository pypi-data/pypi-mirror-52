"""Basic utility functions for folder/file management operations"""

from glob import iglob
import logging
import os
import shutil
from typing import Iterator, List

import cv2
import numpy as np


__all__ = [
    "get_files", 
    "make_dirs", 
    "save_pts",
    "load_pts",
    "imwrite",
    "image_paths_to_images",
    "landmarks_paths_to_landmarks",
    "copy_file",
]
    

def get_files(folder_path: str, extension: str="*", recursive: bool=False) -> Iterator[str]:
    """
    Get all file paths in a given directory, and all its sub directories if recursive is True
    
    :param str folder_path: Path to folder
    :param str extension: File extensions (without dot) that wants to be got
    :param bool recursive: Whether or not to search sub-directories
    :return collections.Iterable[str]
    """ 

    extension = f"*.{extension}"
    if recursive:
        file_paths = iglob(os.path.join(folder_path, "**", extension), recursive=True)
    else:
        file_paths = iglob(os.path.join(folder_path, extension), recursive=False)
    return file_paths
    


def make_dirs(path:str) -> None:
    """
    Creates directory at the given path if it already does not exists 
    :param str path: Path to the directory to be created
    """
    if not os.path.exists(path):
        os.makedirs(path)


def load_pts(path:str) -> np.ndarray:
    landmarks = np.genfromtxt(path, skip_header=3, skip_footer=1)
    return landmarks


def save_pts(path: str, landmarks: np.ndarray) -> None:
    make_dirs(os.path.dirname(path))
    """Saves .pts files"""
    landmarks_pts = "version: 1\nn_points: 68\n{\n"
    for pts in landmarks:
        landmarks_pts += str(pts[0]) + " " + str(pts[1]) + "\n"
    landmarks_pts += "}"
    with open(path, "w") as file_:
        print(landmarks_pts, file=file_)


def imwrite(path: str, image: np.ndarray) -> None:
    make_dirs(os.path.dirname(path))
    cv2.imwrite(path, image)


def image_paths_to_images(image_paths: List[str]) -> Iterator[np.ndarray]:
    for image_path in image_paths:
        yield cv2.imread(image_path)


def landmarks_paths_to_landmarks(landmarks_paths: List[str]) -> Iterator[np.ndarray]:
    for landmarks_path in landmarks_paths:
        yield load_pts(landmarks_path)


def copy_file(src, dst):
    make_dirs(os.path.dirname(dst))
    shutil.copyfile(src, dst)
