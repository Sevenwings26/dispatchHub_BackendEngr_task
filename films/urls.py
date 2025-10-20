from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views

urlpatterns = [
    # Film endpoints
    path('', views.film_list, name='film-list'),
    path('films/<int:film_id>/comments/', views.film_comments, name='film-comments'),
    path('films/<int:film_id>/comments/add/', views.add_comment, name='add-comment'),
    
    # API Documentation
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/swagger-ui/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
