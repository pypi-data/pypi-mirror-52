"""Data preprocessing utilities"""
import imgaug.augmenters as iaa
import numpy as np

from dpu import AffineTransformation, VectorTransformation


__all__ = ["ImageAugmentation", "augment_images"]


def augment_images(images, method_names_to_n):
    augmenter = ImageAugmentation(method_names_to_n)
    return augmenter.run(images)


class ImageAugmentation:
    def __init__(self, method_name_to_n=None):
        self.augs = []
        self.aug_names = []
        self.method_name_to_n = method_name_to_n

    def get_methods(self):
        methods = [method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("__")]
        methods.remove("run")
        return methods

    def run(self, images):
        self()
        for aug in self.augs:
            yield aug.augment_images(images), aug.name

    def __call__(self):
        for method_name, n in self.method_name_to_n.items():
            getattr(self, method_name)(n)

    def super_pixels(self, n=10):
        aug = iaa.Superpixels(p_replace=(0.1, 1.0), n_segments=(16, 128), name="super_pixels")
        self.augs.extend([aug for _ in range(n)]) 
        return aug

    def change_colorspace(self, n=10):
        color_spaces = ["HSV", "Lab", "HLS"]
        for i in range(n):
            color_space = color_spaces[i%len(color_spaces)]
            channel = np.random.randint(3)
            aug = iaa.Sequential([
                iaa.ChangeColorspace(from_colorspace="BGR", to_colorspace=color_space), 
                iaa.WithChannels(channel, iaa.Add((50, 100))),
                iaa.ChangeColorspace(from_colorspace=color_space, to_colorspace="BGR")
            ], name="change_colorspace")

            self.augs.append(aug)
        return aug
    
    def grayscale(self, n=10):
        aug = iaa.Grayscale(alpha=(0.0, 1.0), name="grayscale")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def gaussian_blur(self, n=10):
        aug = iaa.GaussianBlue(sigma=(0.0, 3.0), name="gausian_blur")
        self.augs.extend([aug for _ in range(n)]),
        return aug

    def average_blur(self, n=10):
        aug = iaa.AverageBlur(k=(2, 11), name="average_blue")
        self.augs.extend([aug for _ in range(n)])
        return aug
        
    def median_blur(self, n=10):
        aug = iaa.MedianBlue(k=(3, 11), name="median_blur")
        self.augs.extend([aug for _ in range(n)])
        return aug
        
    def sharpen(self, n=10):
        aug = iaa.Sharpen(alpha=(0.0, 1.0), lightness=(0.75, 2.0), name="sharpen")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def emboss(self, n=10):
        aug = iaa.Emboss(alpha=(0.0, 1.0), strength=(0.5, 1.5), name="emboss")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def edge_detect(self, n=10):
        aug = iaa.EdgeDetect(alpha=(0.0, 1.0), name="edge_detect")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def directed_edge_detect(self, n=10):
        aug = iaa.DirectedEdgeDetect(alpha=(0.0, 1.0), direction=(0.0, 1.0), name="directed_edge_detect")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def add(self, n=10):
        aug = iaa.Add((-50, 50), name="add")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def add_elementwise(self, n=10):
        aug = iaa.AddElementwise((-50, 50), name="add_elementwise")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def additive_gaussian_noise(self, n=10):
        aug = iaa.AdditiveGaussianNoise(scale=(0, 0.05*255), name="additive_gaussian_noise")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def multiply(self, n=10):
        aug = iaa.Multiply((0.5, 1.5), name="multiply") 
        self.augs.extend([aug for _ in range(n)])
        return aug

    def multiply_elementwise(self, n=10):
        aug = iaa.MultiplyElementwise((0.5, 1.5), name="multiply_elementwise")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def dropout(self, n=10):
        aug = iaa.Dropout(p=(0, 0.2), name="dropout")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def coarse_dropout(self, n=10):
        aug = iaa.CoarseDropout(0.02, size_percent=0.5, name="coarse_dropout")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def invert(self, n=10):
        aug = iaa.Invert(0.25, per_channel=0.5, name="invert")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def contrast_normalization(self, n=10):
        aug = iaa.ContrastNormalization((0.5, 1.5), per_channel=0.5, name="contrast_normalization")
        self.augs.extend([aug for _ in range(n)])
        return aug

    def elastic_transformation(self, n=10):
        aug = iaa.ElasticTransformation(alpha=(0, 5.0), sigma=0.25, name="elastic_transformation")
        self.augs.extend([aug for _ in range(n)])
        return aug

    # def transform_2d(self, n=10):
    #     for _ in range(n):
    #         angle = np.random.normal(0, rotation_std)
    #         offset = (np.random.normal(0, translation_std[0]), np.random.normal(0, translation_std[1]))
    #         scale = np.random.normal(1, scale_std)
    #         center = tuple(self.img_shape/2)
    #         aug = AffineTransformation(angle, scale, offset, center)
    #         self.augs.append(aug)
    #     return aug


class AugmentAffineWL:
    def __call__(self, image, landmarks):  
        pass
