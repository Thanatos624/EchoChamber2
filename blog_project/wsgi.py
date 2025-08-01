import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Get the standard Django application
application = get_wsgi_application()

# Wrap the application with WhiteNoise and tell it to serve media files
application = WhiteNoise(application, root=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media'))
