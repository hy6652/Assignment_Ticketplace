from django.forms import ValidationError

from rest_framework import generics

from movies.models      import MovieList, Rating
from movies.serializers import MovieListSerializer, RatingSerializer


class MoviewListView(generics.ListCreateAPIView):
    serializer_class = MovieListSerializer
    queryset         = MovieList.objects.all()


class RatingView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        try:
            pk         = self.kwargs.get('pk')
            user       = self.request.user
            movie_list = MovieList.objects.get(pk=pk)

            reviews = Rating.objects.filter(user=user, movie_list=movie_list)
            if reviews.exists():
                raise ValidationError('your rating already exists')
        except MovieList.DoesNotExist:
            raise ValidationError('movie does not exist')
        
        if movie_list.number_rating == 0:
            movie_list.avg_rating = serializer.validated_data['point_rating']

        movie_list.avg_rating = (movie_list.avg_rating + serializer.validated_data['point_rating']) / 2
        
        movie_list.number_rating = movie_list.number_rating + 1
        movie_list.save()

        serializer.save(user=user, movie_list=movie_list)