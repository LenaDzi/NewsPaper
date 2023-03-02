from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from .models import Post
from .models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categoryType',
            'title',
            'text',
            'postCategory',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст статьи или новости не может быть менее 20 символов."
            })

        return cleaned_data

class ProfileUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

