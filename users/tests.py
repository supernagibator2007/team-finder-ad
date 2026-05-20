from django.test import TestCase

from .models import User


class UserModelTests(TestCase):
    def test_avatar_is_generated_when_not_provided(self):
        user = User.objects.create_user(
            email='test@example.com',
            name='Иван',
            surname='Иванов',
            password='password123',
        )

        self.assertTrue(user.avatar, 'Avatar should be generated when it is not provided')
        self.assertTrue(user.avatar.name.endswith('.png'), 'Generated avatar must be a PNG file')
