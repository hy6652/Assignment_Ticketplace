from django.urls import path

from movies.views import RatingView, MoviewListView

urlpatterns = [
    path('/<int:pk>/rating', RatingView.as_view(), name='rating'),
    path('/api/v1/movies', MoviewListView.as_view(), name='movie-list'),
]
