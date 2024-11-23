from django.db import models
from typing import Dict, Any


class Image(models.Model):
    """
        Model representing an image that is uploaded by the user.

        Attributes:
            image (ImageField): The actual image file uploaded by the user.
            uploaded_at (DateTimeField): The timestamp when the image was uploaded.
    """
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded at {self.uploaded_at}"


class Mask(models.Model):
    """
       Model representing a mask created for an image with coordinates and a confidence score.

       Attributes:
           image (ForeignKey): The related Image object that this mask belongs to.
           coordinates (JSONField): The coordinates defining the mask (included/excluded points).
           label (CharField): The label for the mask (e.g., 'object' or 'region').
           confidence (FloatField): The confidence score of the mask's accuracy.
   """
    image = models.ForeignKey(Image, related_name='masks', on_delete=models.CASCADE)
    coordinates = models.JSONField()
    label = models.CharField(max_length=100)
    confidence = models.FloatField()

    def __str__(self):
        return f"Mask {self.id} for Image {self.image_id}"
