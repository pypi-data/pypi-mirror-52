import augmentation.augmentation_2d as aug2d
import augmentation.augmentation_3d as aug3d
from torchvision.transforms import Compose


def get_augmenter2d(shape, deformation_scale=0.01, sigma_max=0.1, include_segmentation=False):
    """
    Default augmenter for 2D data
    :param shape: shape of the inputs that the augmenter will receive
    :param deformation_scale: scale of the deformations
    :param sigma_max: maximum noise standard deviation
    :param include_segmentation: flag that specifies whether the second half of the batch are segmentations
    :return: the augmenter
    """
    augmenter = Compose([
        aug2d.ToFloatTensor(cuda=True),
        aug2d.Rotate90(shape),
        aug2d.FlipX(shape, prob=0.5),
        aug2d.FlipY(shape, prob=0.5),
        aug2d.RandomDeformation(shape, sigma=deformation_scale, include_segmentation=include_segmentation),
        aug2d.AddNoise(sigma_max=sigma_max, include_segmentation=include_segmentation)
    ])

    return augmenter


def get_augmenter3d(shape, deformation_scale=0.01, sigma_max=0.1, include_segmentation=False):
    """
    Default augmenter for 3D data
    :param shape: shape of the inputs that the augmenter will receive
    :param deformation_scale: scale of the deformations
    :param sigma_max: maximum noise standard deviation
    :param include_segmentation: flag that specifies whether the second half of the batch are segmentations
    :return: the augmenter
    """
    augmenter = Compose([
        aug3d.ToFloatTensor(cuda=True),
        aug3d.Rotate90(shape),
        aug3d.FlipX(shape, prob=0.5),
        aug3d.FlipY(shape, prob=0.5),
        aug3d.RandomDeformation(shape, sigma=deformation_scale, include_segmentation=include_segmentation),
        aug3d.AddNoise(sigma_max=sigma_max, include_segmentation=include_segmentation)
    ])

    return augmenter
