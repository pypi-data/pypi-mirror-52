from typing import Tuple

import cv2
import numpy as np
import pandas as pd

from dpu import AffineTransformation, VectorTransformation

__all__ = [
    "AffineCropWL", "NormalizeCanonicalWL", 
    "TransformAffineWL", "MirrorWL",
]


class DataPreprocessorWithLandmarks:
    def __iter__(self):
        raise NotImplementedError

    def __call__(self):
        raise NotImplementedError


class AffineCropWL(DataPreprocessorWithLandmarks):
    def __init__(self, images, all_landmarks, bboxes, output_shape, margin):
        self.images = images
        self.all_landmarks = all_landmarks
        self.bboxes = bboxes
        self.output_shape = np.asarray(output_shape)
        self.margin = margin

    def __iter__(self):
        for image, landmarks, bbox in zip(self.images, self.all_landmarks, self.bboxes):
            yield self(image, landmarks, bbox)

    def __call__(self, image, landmarks, bbox):
        ymin, xmin, ymax, xmax = bbox
        
        center = np.mean(landmarks, axis=0)
        image_center = np.asarray([x/2 for x in image.shape[:2]][::-1])
        offset = center - image_center

        bbox_size = max(ymax-ymin, xmax-xmin)
        desired_size = 1 - 2 * self.margin
        desired_size *= min(self.output_shape)
        scale = desired_size / bbox_size

        landmark_resizer = VectorTransformation(0, scale, -offset, center)
        image_resizer = AffineTransformation(0, scale, -offset, center)
        
        resized_landmarks = landmark_resizer(landmarks)
        resized_image = image_resizer(image)

        min_xy = (image_center - self.output_shape / 2).astype(int)
        max_xy = (image_center + self.output_shape / 2).astype(int)
        resized_image = resized_image[min_xy[1]:max_xy[1], min_xy[0]:max_xy[0]]
        resized_landmarks -= min_xy

        return resized_image, resized_landmarks


class NormalizeCanonicalWL(DataPreprocessorWithLandmarks):
    def __init__(self, images, all_landmarks):
        self.images = images
        self.all_landmarks = all_landmarks

    def __iter__(self):
        for image, landmarks in zip(self.images, self.all_landmarks):
            yield self(image, landmarks)

    def __call__(self, image, landmarks):
        left_eye_center = np.mean(landmarks[36:42], axis=0)
        right_eye_center = np.mean(landmarks[42:48], axis=0)
        dY = right_eye_center[1] - left_eye_center[1]
        dX = right_eye_center[0] - left_eye_center[0]
        angle = -np.degrees(np.arctan2(dY, dX))

        center = np.mean(landmarks, axis=0)

        landmark_transformer = VectorTransformation(angle, 1, 0, center)
        image_transformer = AffineTransformation(angle, 1, 0, center)
        
        transformed_landmarks = landmark_transformer(landmarks)
        transformed_image = image_transformer(image)

        return transformed_image, transformed_landmarks


class TransformAffineWL(DataPreprocessorWithLandmarks):
    def __init__(self, images, all_landmarks, rotation_std, scale_std, translation_std):
        self.images = images
        self.all_landmarks = all_landmarks
        self.rotation_std = rotation_std
        self.scale_std = scale_std
        self.translation_std = translation_std

    def __iter__(self):
        for image, landmarks in zip(self.images, self.all_landmarks):
            yield self(image, landmarks)

    def __call__(self, image, landmarks):
        img_shape = np.asarray(image.shape[:2])
        translation_std = np.asarray(self.translation_std) * img_shape

        angle = np.random.normal(0, self.rotation_std)
        offset = (np.random.normal(0, translation_std[0]), np.random.normal(0, translation_std[1]))
        scale = np.random.normal(1, self.scale_std)
        center = tuple(img_shape/2)

        landmark_transformer = VectorTransformation(angle, scale, offset, center)
        image_transformer = AffineTransformation(angle, scale, offset, center)
        
        augmented_landmarks = landmark_transformer(landmarks)
        augmented_image = image_transformer(image)

        return augmented_image, augmented_landmarks


class MirrorWL(DataPreprocessorWithLandmarks):
    def __init__(self, images, all_landmarks):
        self.images = images
        self.all_landmarks = all_landmarks

    def __iter__(self):
        for image, landmarks in zip(self.images, self.all_landmarks):
            yield self(image, landmarks)

    def __call__(self, image, landmarks):
        mirrored_image = np.fliplr(image)
        mirrored_landmarks = self.mirror_landmarks(landmarks, image.shape)

        return mirrored_image, mirrored_landmarks

    def mirror_landmarks(self, landmarks, img_shape):
        clandmarks = landmarks.copy()
        left_eye_indices = np.arange(36, 42)
        right_eye_indices = np.arange(42, 48) 
        left_eyebrow_indices = np.arange(17, 22)
        reft_eyebrow_indices = np.arange(22, 27)
        left_nose_indices = np.asarray([31, 32])
        right_nose_indices = np.asarray([34, 35])
        left_mouth_indices = np.asarray([48, 49, 50, 58, 59, 60, 61, 67])
        right_mouth_indices = np.asarray([54, 53, 52, 56, 55, 64, 63, 65])
        left_chin_indices = np.arange(8)
        right_chin_indices = np.arange(9, 17)

        clandmarks[:, 0] = img_shape[1] - clandmarks[:, 0]
        clandmarks[left_eye_indices], clandmarks[right_eye_indices] = clandmarks[right_eye_indices],\
                                                                    clandmarks[left_eye_indices]
        clandmarks[[36, 37, 41]], clandmarks[[39, 38, 40]] = clandmarks[[39, 38, 40]],\
                                                            clandmarks[[36, 37, 41]]
        clandmarks[[42, 43, 47]], clandmarks[[45, 44, 46]] = clandmarks[[45, 44, 46]],\
                                                            clandmarks[[42, 43, 47]]
        clandmarks[left_eyebrow_indices], clandmarks[reft_eyebrow_indices] = clandmarks[reft_eyebrow_indices][::-1],\
                                                                            clandmarks[left_eyebrow_indices][::-1]
        clandmarks[left_nose_indices], clandmarks[right_nose_indices] = clandmarks[right_nose_indices][::-1],\
                                                                        clandmarks[left_nose_indices][::-1]
        clandmarks[left_mouth_indices], clandmarks[right_mouth_indices] = clandmarks[right_mouth_indices],\
                                                                        clandmarks[left_mouth_indices]
        clandmarks[left_chin_indices], clandmarks[right_chin_indices] = clandmarks[right_chin_indices][::-1],\
                                                                        clandmarks[left_chin_indices][::-1]
        return clandmarks

