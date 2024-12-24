from rest_framework import viewsets, generics, status
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import *
from .permisssions import *


from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializers
    permission_classes = [CheckProfile]

    # def get_queryset(self):
    #     return UserProfile.objects.filter(id=self.request.user.id)
    #



class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'hashtag']
    ordering_fields = ['created_at']
    pagination_class = PostPagination


class PostIMGViewSet(viewsets.ModelViewSet):
    queryset = PostIMG.objects.all()
    serializer_class = PostIMGSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [CheckComment]

class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class SaveViewSet(viewsets.ModelViewSet):
    serializer_class = SaveSerializer

    def get_queryset(self):
        return Save.objects.filter(user=self.request.user)

    # def retrieve(self, request, *args, **kwargs):
    #     cart, created = Save.objects.get_or_create(user=request.user)
    #     serializer = self.get_serializer(cart)
    #     return Response(serializer.data)


class SaveItemViewSet(viewsets.ModelViewSet):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer
