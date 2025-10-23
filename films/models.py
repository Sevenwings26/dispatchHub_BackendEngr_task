from django.db import models

# Create your models here.
class Film(models.Model): 
    title = models.CharField(max_length=200) 
    release_date = models.DateField() 
    swapi_id = models.IntegerField(unique=True)

    class Meta:
        ordering = ['release_date']

    def __str__(self):
        return self.title


class Comment(models.Model): 
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments') 
    text = models.CharField(max_length=500) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment on {self.film.title}: {self.text[:50]}"
