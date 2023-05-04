from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import os
import requests
from io import BytesIO
from dataclasses import dataclass, asdict
from typing import Dict

from .utils import get_augment_image, check_if_url, all_contains
from .logger import logging

# import logging
# logging.basicConfig(level=logging.INFO, format='%(process)d-%(levelname)s-%(message)s')


@dataclass(frozen=True)
class Constants:
    MODEL: str = "image_captioning_model"
    FEATURE_EXTRACTOR: str = "image_captioning_feature_extractor"
    TOKENIZER: str = "image_captioning_tokenizer"

    @property
    def model_names(self):
        return asdict(self).values()


class ImageCaptionGenerator:
    def __init__(self):
        self.model = None
        self.feature_extractor = None
        self.tokenizer = None
        self.__initialize_models()

    def __initialize_models(self):

        try:

            if not os.path.exists("models"):
                os.makedirs("models", exist_ok=True)

            # checks if the models are saved in the local
            if not all_contains(Constants().model_names, os.listdir("models")):
                logging.info("Could not find the models in local directory! Downloading the Models")

                # download the models
                self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
                self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
                self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

                logging.info("Saving the models in the local folder")
                # then save them in the models/
                self.model.save_pretrained(f"models/{Constants.MODEL}")
                self.feature_extractor.save_pretrained(f"models/{Constants.FEATURE_EXTRACTOR}")
                self.tokenizer.save_pretrained(f"models/{Constants.TOKENIZER}")

            else:  # else load from the local
                logging.info("Loading models from the local directory")
                self.model = VisionEncoderDecoderModel.from_pretrained(f"models/{Constants.MODEL}")
                self.feature_extractor = ViTImageProcessor.from_pretrained(f"models/{Constants.FEATURE_EXTRACTOR}")
                self.tokenizer = AutoTokenizer.from_pretrained(f"models/{Constants.TOKENIZER}")

            # set the device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)

            max_length: int = 16
            num_beams: int = 5

            self.gen_kwargs: Dict[str, int] = {
                "max_length": max_length,
                "num_beams": num_beams
            }

        except Exception as e:
            logging.warning(str(e))

    def generate_caption(self, image_path: str, n_other_captions: int = 0):

        try:
            # checks if the image_path is url or only path
            if check_if_url(image_path):
                logging.info("The given string is a URL")
                response = requests.get(image_path)  # download the content
                image = Image.open(BytesIO(response.content))  # convert it to Image object
            else:
                logging.info("The given string is a local Image path")
                # opens the image from the local path
                image = Image.open(image_path)

            if image.mode != "RGB":
                image = image.convert(mode="RGB")

            # list representation
            images = [image]

            # generate augmented images if more than one caption required
            if n_other_captions != 0:
                for aug_img in get_augment_image(image, n_other_captions):
                    images.append(aug_img)

            # convert to tensor
            pixel_values = self.feature_extractor(images=images, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)

            # encode
            output_ids = self.model.generate(pixel_values, **self.gen_kwargs)

            # decode
            captions = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)

            # generated captions
            captions = [cap.strip() for cap in captions]
            return captions
        
        except Exception as e:
            logging.warning(str(e))
