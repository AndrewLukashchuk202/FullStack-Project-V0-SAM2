from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Set up api endpoint and add it to the url link
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/images/', views.image_list, name='image_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
