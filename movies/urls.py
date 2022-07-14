from django.urls import path

from movies.views import RatingView, MovieListView, MovieDetailView

urlpatterns = [
    path('/<int:pk>/rating', RatingView.as_view(), name='rating'),
    path('/api/v1/movies', MovieListView.as_view(), name='movie-list'),
    path('/api/v1/movies/<int:pk>', MovieDetailView.as_view(), name='movie-detail'),
]
