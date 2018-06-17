from django.contrib.auth.base_user import BaseUserManager

# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#custom-users-and-permissions
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = create_user(
            email,
            password=password
            )
        user.is_admin = True
        user.save(db=self._db)
        return user
