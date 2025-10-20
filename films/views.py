import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .models import Film
from .serializers import FilmSerializer, CommentSerializer



# def home()


@extend_schema(
        tags=["System"],
        summary="Health Check", 
        description="Basic liveness probe", 
        responses={200:dict}
)
@api_view(['GET'])
def health_check(request):
    return Response({'Status':"Ok"}, status=status.HTTP_200_OK)


def fetch_films_from_swapi():
    """Helper function to fetch films from SWAPI and save to database"""
    try:
        response = requests.get('https://swapi.dev/api/films/')
        response.raise_for_status()
        films_data = response.json()['results']
        
        for film_data in films_data:
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


@extend_schema(
    summary="Get all films",
    description="""Retrieve a list of all Star Wars films.
    **Features:**
    - Automatically fetches films from SWAPI if database is empty
    - Includes ID, title, release date, and comment count for each film
    - Films are sorted by release date in ascending order
    - Each film includes a count of associated comments
    
    **Note:** The first time this endpoint is called, it may take longer as it populates the database from SWAPI.
    """,
    responses={
        200: FilmSerializer(many=True),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Internal server error when fetching from SWAPI",
            examples=[
                OpenApiExample(
                    "SWAPI Error Example",
                    value={"detail": "Failed to fetch films from SWAPI: Connection error"},
                )
            ]
        )
    }
)
@api_view(['GET'])
def film_list(request):
    """
    Get list of all films with comment counts, sorted by release date.
    """
    # Fetch from SWAPI if no films in database
    if not Film.objects.exists():
        fetch_films_from_swapi()
    
    films = Film.objects.all().order_by('release_date')
    serializer = FilmSerializer(films, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Get film comments",
    description="Retrieve all comments for a specific film. Comments are sorted by creation date in ascending order.",
    parameters=[
        OpenApiParameter(
            name='film_id', 
            type=OpenApiTypes.INT, 
            location=OpenApiParameter.PATH, 
            description='Film ID'
        )
    ],
    responses={
        200: CommentSerializer(many=True),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Film not found",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"detail": "Not found."},
                )
            ]
        )
    }
)
@api_view(['GET'])
def film_comments(request, film_id):
    """
    Get all comments for a specific film, sorted by creation date.
    """
    film = get_object_or_404(Film, pk=film_id)
    comments = film.comments.all().order_by('created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Add comment to film",
    description="""Add a new comment to a specific film.
    **Constraints:**
    - Comment text is limited to 500 characters
    - Film must exist
    - Comment text is required
    **Note:** The created_at field is automatically set to the current timestamp.
    """,
    request=CommentSerializer,
    parameters=[
        OpenApiParameter(
            name='film_id', 
            type=OpenApiTypes.INT, 
            location=OpenApiParameter.PATH, 
            description='Film ID'
        )
    ],
    examples=[
        OpenApiExample(
            "Valid Comment Example",
            value={"text": "This is a great film!"},
            request_only=True
        ),
        OpenApiExample(
            "Invalid Comment Example",
            value={"text": ""},
            request_only=True
        )
    ],
    responses={
        201: CommentSerializer,
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Bad request - validation error",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value={"text": ["This field may not be blank."]},
                )
            ]
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Film not found",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"detail": "Not found."},
                )
            ]
        )
    }
)
@api_view(['POST'])
def add_comment(request, film_id):
    """
    Add a comment to a specific film.
    """
    film = get_object_or_404(Film, pk=film_id)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(film=film)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)