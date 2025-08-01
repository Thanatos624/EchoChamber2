from django.urls import path
from .views import ContentRecommendationView, CollaborativeRecommendationView

urlpatterns = [
    # URL for content-based recommendations
    path('api/recommendations/content/<int:post_id>/', ContentRecommendationView.as_view(), name='content-recommendation'),
    # New URL for collaborative filtering recommendations
    path('api/recommendations/user/<int:user_id>/', CollaborativeRecommendationView.as_view(), name='collaborative-recommendation'),
]
