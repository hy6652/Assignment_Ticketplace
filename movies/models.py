from django.db                  import models
from django.contrib.auth.models import User

class MovieList(models.Model): 
    title          = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    year           = models.CharField(max_length=25)
    genre          = models.CharField(max_length=255)
    play_time      = models.CharField(max_length=255)
    director       = models.CharField(max_length=255)
    poster         = models.FileField(max_length=300, upload_to='poster/')
    cast_list      = models.TextField()
    synopsis       = models.TextField()
    avg_rating     = models.FloatField(default=0)
    number_rating  = models.IntegerField(default=0)

    class Meta:
        db_table = 'movie_lists'

class Rating(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_list   = models.ForeignKey(MovieList, on_delete=models.CASCADE)
    point_rating = models.IntegerField(default=0)

    class Meta:
        db_table = 'ratings'

class Video(models.Model):
    movie_list = models.ForeignKey(MovieList, on_delete=models.CASCADE, related_name='video')
    file       = models.FileField(max_length=300, upload_to='video/')

    class Meta:
        db_table = 'videos'