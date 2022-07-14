from django.db                  import models
from django.contrib.auth.models import User

class MovieList(models.Model): 
    title          = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    year           = models.CharField(max_length=25)
    genre          = models.CharField(max_length=255)
    play_time      = models.CharField(max_length=255)
    director       = models.CharField(max_length=255)
    poster         = models.CharField(max_length=255)
    casts          = models.TextField()
    synopsis       = models.TextField()
    avg_rating     = models.FloatField(default=0)
    number_rating  = models.IntegerField(default=0)
    cast_list      = models.TextField()

    class Meta:
        db_table = 'movie_lists'

class Rating(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_list   = models.ForeignKey(MovieList, on_delete=models.CASCADE)
    point_rating = models.IntegerField(default=0)

    class Meta:
        db_table = 'raitings'

# class Video(models.Model):
#     movie_list = models.ForeignKey(MovieList, on_delete=models.CASCADE)
#     file       = models.FileField()

#     class Meta:
#         db_table = 'videos'