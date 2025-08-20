from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    def __str__(self):
        return f"{self.user.username}'s Profile"
    


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="photos")  # 👈 Added
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')

    def __str__(self):
        return f"{self.user.username} likes {self.photo.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.photo.title}"


