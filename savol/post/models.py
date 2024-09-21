from django.db import models
from shared.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.constraints import UniqueConstraint
from django.core.validators import FileExtensionValidator, MaxLengthValidator


User = get_user_model()


class Topic(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='topic_images')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics")
    
    class Meta:
        db_table = 'topics'
        verbose_name = 'topic'
        verbose_name_plural = 'topics'

    def __str__(self):
        return self.name
    
    
class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image1 = models.ImageField(upload_to='post_images', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
        ], blank=True)
    image2 = models.ImageField(upload_to='post_images', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
        ], blank=True)
    image3 = models.ImageField(upload_to='post_images', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
        ], blank=True)
    caption = models.TextField(validators=[MaxLengthValidator(2000)])
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    
    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return f"{self.author}'s post"
    

class PostComment (BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "comments")
    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        null = True,
        blank = True,
    )


class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'post'],
                name='PostLikeUniqunessl'
            )
        ]


class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'comment'],
                name='CommentLikeUniqunessl'

            )
        ]



