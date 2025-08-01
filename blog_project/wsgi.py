import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Get the standard Django application
application = get_wsgi_application()

# Define the media root
media_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')

# Only add WhiteNoise for media files if the directory exists
if os.path.isdir(media_root):
    application = WhiteNoise(application, root=media_root)
