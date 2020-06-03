from django.forms import ModelForm
from content.models import Post

class AddPosts(ModelForm):
    """ 
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(blank=True,upload_to='content_images')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='blog_posts')
    created_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    content_type = models.IntegerField(choices=CONTENT_TYPE,default=0)
    league = models.ForeignKey(Leaguetype,null=False,on_delete=models.CASCADE)
    """
    class Meta:
        model = Post
        fields = ('title','image','slug','content','status','content_type','league')