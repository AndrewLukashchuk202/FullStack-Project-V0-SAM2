from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import Image
import json
import base64
from PIL import Image as PILImage
from io import BytesIO
from imagifier.data_types import Coordinates
from imagifier.sam2 import create_mask_for_image
from typing import Union, List, Dict, Any


@csrf_exempt
def image_list(request: HttpRequest) -> JsonResponse:
    """
       Handles the list and creation of images.

       - GET: Retrieves all images stored in the database.
       - POST: Uploads a new image, processes it, and returns both the original and processed images.

       Args:
           request (HttpRequest): The HTTP request object.

       Returns:
           JsonResponse: A JSON response with the image data or an error message.
       """
    if request.method == 'GET':
        # Retrieve all images
        images = Image.objects.all()
        return JsonResponse({
            'images': [{'id': img.id, 'url': img.image.url} for img in images]
        })
    elif request.method == 'POST':
        # Handle image upload and processing
        image_file = request.FILES.get('image') # Uploaded image file
        tags = json.loads(request.POST.get('tags', '[]')) # Tag coordinates in JSON format

        # Initialize coordinate types for inclusion and exclusion
        includes:Coordinates = {'included': [], 'excluded': []}
        for coordinates in tags:
            x, y, type_ = coordinates.values()
            includes[type_].append((int(x), int(y)))  # type:ignore

        # Ensure an image file is provided
        if not image_file:
            return JsonResponse({'error': 'No image file provided'}, status=400)

        # Save the original image
        image = Image.objects.create(image=image_file)

        # Process the image (this is a placeholder, replace with your actual image processing logic)
        img = PILImage.open(image_file)
        img = create_mask_for_image(img, includes)

        # Save the processed image
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return JsonResponse({
            'id': image.id,
            'original_image': request.build_absolute_uri(image.image.url),
            'processed_image': f"data:image/png;base64,{encoded_image}"
        })


@csrf_exempt
def image_detail(request: HttpRequest, pk: int) -> JsonResponse:
    """
        Handles retrieval and deletion of a specific image.

        - GET: Retrieves the original and processed image for the given ID.
        - DELETE: Deletes the image with the given ID.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key (ID) of the image.

        Returns:
            JsonResponse: A JSON response with the image data or an error message.
    """
    try:
        # Retrieve the image by primary key
        image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        # Return error if image is not found
        return JsonResponse({'error': 'Image not found'}, status=404)

    if request.method == 'GET':
        # Return the image data for the given ID
        return JsonResponse({
            'id': image.id,
            'original_image': image.image.url,
            'processed_image': image.processed_image.url
        })
    elif request.method == 'DELETE':
        # Delete the image and return a success message
        image.delete()
        return JsonResponse({'message': 'Image deleted successfully'})
