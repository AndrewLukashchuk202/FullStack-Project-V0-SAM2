# important Set-up
import os
# if using Apple MPS, fall back to CPU for unsupported ops
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import numpy as np
import torch
from PIL import Image
from imagifier.data_types import Coordinates
from pathlib import Path
from typing import Union, List, Tuple

# loading SAM2
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor


# Select device based on availability: CUDA, MPS (Apple), or CPU
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(f"using device: {device}")

# Device-specific optimizations (bfloat16 for CUDA and TF32 support for Ampere GPUs)
if device.type == "cuda":
    # use bfloat16 for the entire notebook
    torch.autocast("cuda", dtype=torch.bfloat16).__enter__()
    # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
    if torch.cuda.get_device_properties(0).major >= 8:
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
elif device.type == "mps":
    print(
        "\nSupport for MPS devices is preliminary. SAM 2 is trained with CUDA and might "
        "give numerically different outputs and sometimes degraded performance on MPS. "
        "See e.g. https://github.com/pytorch/pytorch/issues/84936 for a discussion."
    )


# Set up SAM2 model loading and prediction
base_path = Path(__file__).parent.parent
sam2_checkpoint = base_path / "checkpoints/sam2.1_hiera_large.pt"
model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"

# Build the SAM2 model based on configuration and checkpoint
sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=device)

# Initialize the image predictor
predictor = SAM2ImagePredictor(sam2_model)
# ------------------------------


def create_mask_for_image(image: Image.Image, coordinates: Coordinates) -> Image.Image:
    """
        Create a mask for the provided image based on the given coordinates.

        Args:
            image (Image.Image): The image to process.
            coordinates (Coordinates): The coordinates for included and excluded points.

        Returns:
            Image.Image: The image blended with the generated mask.
    """
    if isinstance(coordinates, dict):
        coordinates = get_include_coordinates(coordinates)

    # Convert the image to a NumPy array in RGB format
    image = np.array(image.convert("RGB"))

    # Set the image for the predictor to perform the prediction
    predictor.set_image(image)

    # Prepare the input points and labels for the mask generation
    # coordinates - 1=included, 0=excluded
    input_point = np.array(coordinates)
    input_label = np.array([1] * len(coordinates))

    # Generate the mask(s) using the predictor
    masks, _, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    mask = masks[0]   # Choose the first mask from the generated set

    # Create the final image with the mask applied
    return create_image_with_mask(image, mask)


def get_include_coordinates(coordinates: Coordinates) -> list[tuple[int, int], ...]:
    """
        Extract the coordinates that are marked as 'included' for mask generation.

        Args:
            coordinates (Coordinates): The coordinates data structure containing included and excluded points.

        Returns:
            List[Tuple[int, int]]: A list of tuples representing the included coordinates.
    """
    return coordinates['included']


def create_image_with_mask(image_array: np.ndarray, mask: np.ndarray, opacity: float = 0.5, mask_color: Tuple[int, int, int] = (0, 0, 255)) -> Image.Image:
    """
       Create a new image by blending the original image with the generated mask.

       Args:
           image_array (np.ndarray): The original image in NumPy array format.
           mask (np.ndarray): The mask to apply to the image (binary mask).
           opacity (float, optional): The opacity of the mask (default is 0.5).
           mask_color (Tuple[int, int, int], optional): The color of the mask (default is blue).

       Returns:
           Image.Image: The blended image with the mask applied.
   """
    image = Image.fromarray(image_array)
    mask = mask.astype(np.uint8)

    # Create a colored mask based on the mask values
    mask_colored = np.zeros_like(image_array)
    mask_colored[mask == 1] = mask_color

    # Convert the colored mask to an image
    mask_image = Image.fromarray(mask_colored)

    # Blend the original image and the mask image with the given opacity
    return Image.blend(image, mask_image, opacity)




























