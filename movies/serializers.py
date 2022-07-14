from rest_framework import serializers

from movies.models import MovieList, Rating


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model  = MovieList
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Rating
        fields = ['point_rating']
