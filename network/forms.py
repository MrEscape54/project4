from django import forms
from .models import Post, User, Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')

class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'rows': 2})

    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'location')

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'rows': 2})

    class Meta:
        model = Post
        fields = ('message',)
        
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Write your message here'}),
            'author' : forms.HiddenInput(),
        }
