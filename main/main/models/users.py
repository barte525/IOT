from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.name = name
        user.surname = surname
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
            name="admin",
            surname="admin"
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=50,
        unique=True,
    )
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_password(self, password):
        super(User, self).set_password(password)
        if CardOwner.objects.filter(user=self.id).exists():
            CardOwner.objects.filter(user=self.id).update(force_password_change=False)


class CardOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    force_password_change = models.BooleanField(default=True)

    def force_password_change_check(self):
        return self.force_password_change


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)