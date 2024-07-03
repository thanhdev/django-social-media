from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def validate_username(value):
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        raise ValidationError(
            "Username can only contain letters, numbers, and underscores."
        )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
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
