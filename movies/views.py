from django.conf  import settings

from rest_framework             import generics
from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions  import ValidationError

from movies.models      import MovieList, Rating, Video
from movies.serializers import MovieListSerializer, RatingSerializer, VideoSerializer
from cores.storages     import FileUploader, s3


class MovieListView(generics.ListCreateAPIView):
    serializer_class   = MovieListSerializer
    queryset           = MovieList.objects.all()
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        poster = request.FILES.get('poster', None)

        if not poster:
            return Response({'you should upload a poster'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_type = poster.content_type.split('/')[0]
        if file_type != 'image':
            return Response({'this file is not an image'}, status=status.HTTP_400_BAD_REQUEST)

        poster_image = FileUploader(s3, settings.AWS_STORAGE_BUCKET_NAME).upload(poster, 'poster/')
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(poster=poster_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingView(generics.CreateAPIView):
    serializer_class   = RatingSerializer
    queryset           = Rating.objects.all()
    permission_classes = [IsAuthenticated]

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


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = MovieListSerializer
    queryset           = MovieList.objects.all()
    permission_classes = [IsAuthenticated]


class VideoListView(generics.CreateAPIView):
    serializer_class = VideoSerializer
    queryset         = Video.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        pk         = kwargs.get('pk')
        movie_list = MovieList.objects.get(pk=pk)

        videos = request.FILES.getlist('file')

        if not videos:
            raise ValidationError('you should add at least one video')
        
        if len(videos) > 4:
            raise ValidationError('you can add up to 4 videos')
        
        result = []
        for video in videos:
            file_type = video.content_type.split('/')[0]
            if file_type != 'video':
                raise ValidationError('this file is not a video')
            file = FileUploader(s3, settings.AWS_STORAGE_BUCKET_NAME).upload(video, 'video/')
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(movie_list=movie_list, file=file)
            result.append(serializer.data)
        return Response(result, status=status.HTTP_201_CREATED)