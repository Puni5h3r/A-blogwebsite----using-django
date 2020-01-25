from .models import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Post


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content','status')