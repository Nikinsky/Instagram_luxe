from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from django.contrib.auth import authenticate


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'bio', 'image', 'website']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'last_name']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']


class PostIMGSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostIMG
        fields = ['post', 'image']

class PostVideSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = ['post', 'video']


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = PostLike
        fields = ['user', 'post', 'like', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    post_photos = PostIMGSerializer(many=True)
    post_videos = PostVideSerializer(many=True)

    class Meta:
        model = Post
        fields = ['user', 'post_videos', 'post_photos', 'description', 'hashtag', 'created_at']



class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['user', 'comment', 'like', 'created_at']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'parent', 'created_at']




class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['user', 'image', 'video', 'created_at']



class SaveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveItem
        fields = ['post', 'save_reference', 'created_date']


class SaveSerializer(serializers.ModelSerializer):
    saves = SaveItemSerializer(many=True)
    class Meta:
        model = Save
        fields = ['user', 'saves']

#
# class SaveItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SaveItem
#         fields = ['post', 'save_reference', 'created_date']




