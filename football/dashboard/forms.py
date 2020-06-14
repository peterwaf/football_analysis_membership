from django.forms import ModelForm
from django import forms
from content.models import Post
from league.models import Leaguetype
from users.models import CustomUser
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

#user form model
class editUsers(ModelForm):
    username = forms.CharField(max_length=50, required=False)
    class Meta:
        model = CustomUser
        fields = ('username',
        'email',
        'first_name',
        'last_name',
        'mobile_number',
        'is_staff',
        'is_active',
        'subscribed',
        'subscription_start',
        'subscription_end',
        'date_joined')
