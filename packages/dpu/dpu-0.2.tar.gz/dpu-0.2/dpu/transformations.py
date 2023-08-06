import numbers

import cv2
import numpy as np


__all__ = ["AffineTransformation", "VectorTransformation"]


class Transformation:
    """Transformation parent class"""

    def __init__(self, angle, scale, translation, center):
        self.angle = angle
        self.scale = scale
        self.translation = translation
        self.center = center
        self._validate_transform_params()

    def _validate_transform_params(self):
        assert isinstance(self.angle, numbers.Number), "angle parameter must be a number"
        assert isinstance(self.scale, numbers.Number), "scale parameter must be a number"

        if isinstance(self.center, numbers.Number):
            self.center = (self.center, self.center)
        assert len(self.center) == 2,\
            "center parameter must be a number or 2D array"

        if isinstance(self.translation, numbers.Number):
            self.translation = (self.translation, self.translation)
        assert len(self.translation) == 2,\
            "translation parameter must be a number or 2D array"

    def augment_images(self, data):
        return self(images)

    def __call__(self, data):
        raise NotImplementedError


class AffineTransformation(Transformation):
    """2D affine transformation"""

    def __init__(self, angle, scale, translation, center):
        super().__init__(angle, scale, translation, center)
        self.angle = np.deg2rad(self.angle + 90)
        self.M = self.get_transformation_matrix()

    def get_transformation_matrix(self):
        T = np.asarray([
            [1, 0, self.translation[0]],
            [0, 1, self.translation[1]],
        ])

        alpha = self.scale * np.sin(self.angle)
        beta = self.scale * np.cos(self.angle)

        SR = np.asarray([
            [alpha, beta, (1-alpha)*self.center[0] - beta*self.center[1]],
            [-beta, alpha, beta*self.center[0] + (1-alpha)*self.center[1]],
            [0, 0, 1]
        ])

        return np.dot(T, SR)
    
    def __call__(self, data):
        data_copy = data.copy()
        data_copy = cv2.warpAffine(data_copy, self.M, data_copy.shape[:2][::-1])
        return data_copy


class VectorTransformation(Transformation):
    """2D vector transformation"""
    def __init__(self, angle, scale, translation, center):
        super().__init__(angle, scale, translation, center)
        self.angle = np.deg2rad(-self.angle)
        self.M = self.get_transformation_matrix()

    def get_transformation_matrix(self):
        R = np.array([
            [np.cos(self.angle), -np.sin(self.angle)],
            [np.sin(self.angle), np.cos(self.angle)],
        ])

        S = np.array([
            [self.scale, 0],
            [0, self.scale]
        ])

        return np.dot(S, R)

    def __call__(self, data):
        data_copy = data.copy()
        data_copy -= self.center
        data_copy = np.dot(data_copy, self.M)
        data_copy += self.center + np.asarray(self.translation)
        return data_copy

