from django.contrib.auth.base_user import BaseUserManager

from Ticket.querysets import GeneralQueryset

class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_queryset(self):
        return GeneralQueryset(self.model, using=self._db)

    # def get(self):
    #     return self.get_queryset().active()

    def all(self):
        return self.get_queryset().active()

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        # elif not password:
        #     raise ValueError('The given password must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True and extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
