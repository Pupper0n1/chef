from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    likes = models.ManyToManyField("users.Profile", related_name="likes", blank=True)

    def __str__(self):
        return self.title