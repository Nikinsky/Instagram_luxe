from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now  # Используем для работы с временными зонами


class UserProfile(AbstractUser):
    bio = models.TextField()
    image = models.ImageField(upload_to='user_image', null=True, blank=True)
    website = models.URLField()


    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Ограничение: подписка уникальна

    def __str__(self):
        return f'{self.follower.username} подписан на {self.following.username}'





class Post(models.Model):
    user = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE)
    description = models.TextField()
    hashtag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.hashtag}'


class PostIMG(models.Model):
    post = models.ForeignKey(Post, related_name='post_photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')

class PostVideo(models.Model):
    post = models.ForeignKey(Post, related_name='post_videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='post_videos')

class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, related_name='post_likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='posts_like', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'like')  # Ограничение: подписка уникальна


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='user_comment', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', related_name='relies', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post} - {self.user}'



class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, related_name='comments_like', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_likes', on_delete=models.CASCADE)
    like = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user} - {self.comment}'


class Story(models.Model):
    user = models.ForeignKey(UserProfile, related_name='story', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_images', null=True, blank=True)
    video = models.FileField(upload_to='story_videos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def delete_expired(cls):
        """
        Удаляет истории, созданные более 24 часов назад.
        """
        expiration_time = now() - timedelta(minutes=1)
        expired_stories = cls.objects.filter(created_at__lt=expiration_time)
        expired_stories.delete()


class Save(models.Model):
    user = models.OneToOneField(UserProfile, related_name='saves', on_delete=models.CASCADE)


class SaveItem(models.Model):
    post = models.ForeignKey(Post, related_name='post_story', on_delete=models.CASCADE)
    save_reference = models.ForeignKey(Save, related_name='saves', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)



class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images_message', null=True, blank=True)
    video = models.FileField(upload_to='videos_message', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)




# .env
# filter(hashtag), search(username), order(post(created_at))
# translate(+2)
# pagination
# swagger
# permission
# jwt