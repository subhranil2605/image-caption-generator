from PIL import Image
import numpy as np
from urllib.parse import urlparse
from typing import List, Iterable


def all_contains(iter_1: Iterable, iter_2: Iterable) -> bool:
    """
    Checks if iter_2 contains all the elements that iter_1 has
    """
    
    if not isinstance(iter_1, set):
        iter_1 = set(iter_1)
    if not isinstance(iter_2, set):
        iter_2 = set(iter_2)
    return iter_1.issubset(iter_2)


def get_augment_image(img, n_aug: int = 1) -> List:
    """
    Create n_aug number of augmented images to create several
    other captions from the same image.

    :param img: Image object
    :param n_aug: number of augmented images
    :return: list of images
    """
    img_width: int = img.width
    img_height: int = img.height

    aug_images: List = []

    for _ in range(n_aug):
        rand_width: int = np.random.randint(int(img_width * 0.3), int(img_width * 0.8))
        rand_height: int = np.random.randint(int(img_height * 0.3), int(img_height * 0.8))

        # define the coordinates to crop the image
        left: int = np.random.randint(int(img_width * 0.2))
        top: int = np.random.randint(int(img_height * 0.2))
        right: int = left + rand_width
        bottom: int = top + rand_height

        # crop the image
        mod_image = img.crop((left, top, right, bottom))

        # flip the image horizontally 
        if np.random.rand() < 0.5:
            mod_image = mod_image.transpose(Image.FLIP_LEFT_RIGHT)

        aug_images.append(mod_image)

    return aug_images


def check_if_url(strng: str) -> bool:
    """
    Checks if a given string is a path or url
    :param strng: given string
    :return: True if the string is a url
    """
    parsed_url = urlparse(strng)
    return parsed_url.scheme in ['http', 'https']
