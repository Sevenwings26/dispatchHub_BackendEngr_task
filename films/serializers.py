from rest_framework import serializers 
from .models import Film, Comment

class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment 
        fields = ['id', 'text', 'created_at'] 
        read_only_fields = ['created_at']

    def validate_text(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Comment cannot exceed 500 characters.")
        return value


class FilmSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ['id', 'title', 'release_date', 'comment_count']

    def get_comment_count(self, obj):
        return obj.comments.count()
    
    