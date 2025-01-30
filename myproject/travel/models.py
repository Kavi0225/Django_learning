from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = RichTextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DestinationDetail(models.Model):
    destination = models.ForeignKey(Destination, related_name='details', on_delete=models.CASCADE)
    place_name = models.CharField(max_length=100)
    place_description = RichTextField()
    place_image = models.ImageField(upload_to='destination_details/')

    def __str__(self):
        return self.place_name
    
class Comments(models.Model):
    DestinationDetail = models.ForeignKey(DestinationDetail, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user.username} to {self.parent.user.username}"
        return f"Comment by {self.user.username}"
