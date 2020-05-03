from django.db import models
from users.models import CustomUser
from league.models import Leaguetype
# Create your models here.
STATUS = (
        (0,"Draft"),
        (1,"Publish")
        )

CONTENT_TYPE = (
        (0,"Free"),
        (1,"Paid")
        )

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(blank=True,upload_to='content_images')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    created_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    content_type = models.IntegerField(choices=CONTENT_TYPE,default=0)
    league = models.ForeignKey(Leaguetype,on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_on']
        db_table = 'tbl_post'

    def __str__(self):
        return self.title