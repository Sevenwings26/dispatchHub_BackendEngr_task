import requests
from rest_framework.exceptions import APIException
from .models import Film


def fetch_films_from_swapi():
    """Helper function to fetch films from SWAPI and save to database"""
    try:
        response = requests.get('https://swapi.dev/api/films/')
        response.raise_for_status()
        films_data = response.json()['results']
        
        for film_data in films_data:
            # save to database 
            Film.objects.get_or_create(
                swapi_id=film_data['episode_id'],
                defaults={
                    'title': film_data['title'],
                    'release_date': film_data['release_date']
                }
            )
        return True
    except requests.RequestException as e:
        raise APIException(detail=f"Failed to fetch films from SWAPI: {str(e)}")

"""
# # To close a webHook - use Status 200
# WebHooks will solidify integration between different services by allowing real-time data sharing and event-driven communication.@extend_schema(
#     summary="Add comment to film",
#     description=Add a new comment to a specific film. 
"""