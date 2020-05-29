from django.forms import ModelForm
from content.models import Post

class AddPosts(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'