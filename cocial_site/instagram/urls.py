from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'user', UserProfileViewSet, basename='user-list')

router.register(r'follow', FollowViewSet, basename='follow-list')

router.register(r'post', PostViewSet, basename='post-list')

router.register(r'comment', CommentViewSet, basename='comment-list')

router.register(r'comment_like', CommentLikeViewSet, basename='comment_like-list')

router.register(r'story', StoryViewSet, basename='story-list')

router.register(r'save', SaveViewSet, basename='save_list')

router.register(r'save_item', SaveItemViewSet, basename='save_item_list')



urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
