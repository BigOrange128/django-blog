from django.db import models
# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    #当打印类实例时调用
    def __str__(self):
        return self.text[:20]
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    drop_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]