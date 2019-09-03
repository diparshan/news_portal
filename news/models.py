from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class News(models.Model):
    CATEGORY = (("0","Politics"), ("1", "Sports"), ("2", "Fashion"), ("3", "Technology"), ("4", "Business"))
    title = models.CharField(max_length=250)
    story = models.TextField()
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    slug = models.SlugField(max_length=270)
    cover_image = models.ImageField(upload_to="uploads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"category": self.get_category_display(), "pk": self.pk, "slug": self.slug})
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name= "news_comment")
    comment_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)