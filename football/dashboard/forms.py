from django.forms import ModelForm
from content.models import Post
from league.models import Leaguetype
#post form model
class AddPosts(ModelForm):
    class Meta:
        model = Post
        fields = ('title','image','slug','content','status','content_type','league')

#league form model
class AddLeagues(ModelForm):
    class Meta:
        model = Leaguetype
        fields = ('league',)
    