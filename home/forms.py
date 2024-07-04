from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

from .models import User, Post


def validate_username(value):
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        raise ValidationError(
            "Username can only contain letters, numbers, and underscores."
        )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}),
    )
    username = forms.CharField(
        validators=[validate_username],
        widget=forms.TextInput(attrs={"placeholder": "Choose a username"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"placeholder": "Enter your password"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Confirm your password"}
        )
        self.fields[
            "password1"
        ].help_text = "Your password must contain at least 8 characters."
        self.fields[
            "password2"
        ].help_text = "Enter the same password as before, for verification."
        self.fields[
            "username"
        ].help_text = "Username can only contain letters, numbers, and underscores."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        image = cleaned_data.get("image")

        if not content and not image:
            raise ValidationError(
                {"content": "You must enter a message or upload an image."}
            )

        return cleaned_data

    class Meta:
        model = Post
        fields = ["content", "image"]
