from rest_framework import serializers

from movies.models import MovieList, Rating, Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Video
        exclude = ['movie_list']


class MovieListSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True, many=True)

    class Meta:
        model  = MovieList
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Rating
        fields = ['point_rating']