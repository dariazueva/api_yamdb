from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма создания пользователя для Django."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
