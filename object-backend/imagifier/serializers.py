from rest_framework import serializers
from .models import Image, Mask


class MaskSerializer(serializers.ModelSerializer):
    """
       Serializer for the Mask model.

       Serializes the fields of the Mask model, allowing for JSON representation
       of mask-related data such as coordinates, label, and confidence.

       Fields:
           id (int): The unique identifier of the mask.
           coordinates (dict): The coordinates associated with the mask.
           label (str): A label describing the mask.
           confidence (float): The confidence score of the mask.
   """
    class Meta:
        model = Mask
        fields = ['id', 'coordinates', 'label', 'confidence']


class ImageSerializer(serializers.ModelSerializer):
    """
        Serializer for the Image model.

        Serializes the fields of the Image model and includes nested serialization
        for related Mask objects.

        Fields:
            id (int): The unique identifier of the image.
            image (ImageField): The uploaded image file.
            uploaded_at (datetime): The timestamp when the image was uploaded.
            masks (list[MaskSerializer]): A list of related masks, serialized using MaskSerializer.
    """
    masks = MaskSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_at', 'masks']
