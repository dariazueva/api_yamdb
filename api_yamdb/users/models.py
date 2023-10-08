from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
USER_ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
]


class CustomUser(AbstractUser):
    # Your custom fields and modifications go here

    # Add related_name to groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users'  # Choose a related_name that makes sense
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users_permissions'  # Choose a related_name that makes sense
    )
