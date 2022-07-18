from django.forms import ValidationError
from django.conf  import settings

from rest_framework             import generics
from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from movies.models      import MovieList, Rating
from movies.serializers import MovieListSerializer, RatingSerializer
from cores.storages     import FileUploader, s3


class MovieListView(generics.ListCreateAPIView):
    serializer_class   = MovieListSerializer
    queryset           = MovieList.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        poster = request.FILES.get('poster', None)

        if not poster:
            return Response({'you should upload one poster'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_type = poster.content_type.split('/')[0]
        if file_type != 'image':
            return Response({'file type is not an image'}, status=status.HTTP_400_BAD_REQUEST)

        poster_image = FileUploader(s3, settings.AWS_STORAGE_BUCKET_NAME).upload(poster, 'ticketplace/')
        
        serializer = MovieListSerializer(data=request.data)
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