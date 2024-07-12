import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import torchvision
import sys
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import os

def generate_masks(image_path, mask_folder):
    # Read the image
    image = plt.imread(image_path)

    def show_anns(anns):
        if len(anns) == 0:
            return
        sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
        ax = plt.gca()
        ax.set_autoscale_on(False)

        img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
        img[:, :, 3] = 0
        for ann in sorted_anns:
            m = ann['segmentation']
            color_mask = np.concatenate([np.random.random(3), [0.35]])
            img[m] = color_mask
        ax.imshow(img)

    # Generate masks
    sam_checkpoint = "sam_vit_h_4b8939.pth"
    model_type = "vit_h"

    device = "cuda"

    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)

    mask_generator = SamAutomaticMaskGenerator(sam)

    masks = mask_generator.generate(image)

    # Create image with masks
    plt.figure(figsize=(20, 20))
    plt.imshow(image)
    show_anns(masks)
    plt.axis('off')

    # Save the image with masks
    mask_image_path = os.path.join(mask_folder, os.path.basename(image_path))
    plt.savefig(mask_image_path)
    plt.close()

    return mask_image_path
