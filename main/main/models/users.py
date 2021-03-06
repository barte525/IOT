from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
import random
import string


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    @staticmethod
    def generate_random_password(length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))


class CardOwner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    force_password_change = models.BooleanField(default=True)

    def force_password_change_check(self):
        return self.force_password_change

    @staticmethod
    def check_permissions(request):
        try:
            CardOwner.objects.get(user=request.user.id)
            return True
        except CardOwner.DoesNotExist:
            return False


class Seller(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    @staticmethod
    def check_permissions(request):
        try:
            Seller.objects.get(user=request.user.id)
            return True
        except Seller.DoesNotExist:
            return False


def create_init_users():
    bartek = User.objects.create_user(email='bartek@gmail.com', password='Oo', name='Bartek', surname='Nowak')
    bartek.save()
    CardOwner(user=bartek).save()
    martyna = User.objects.create_user(email='martyna@gmail.com', password='Oo', name='Martyna', surname='Grzegorczyk')
    martyna.save()
    Seller(user=martyna).save()
    martyna = User.objects.create_user(email='pawel@gmail.com', password='Oo', name='pawel', surname='pawel')  #Haslo123
    martyna.save()
    CardOwner(user=martyna).save()
    #martynka@gmail.com Nowe1234 - uzytkownik z karta o id 12345678901234567890


def create_user(email, password, name, surname):
    user = User.objects.create_user(email=email, password=password, name=name, surname=surname)
    user.save()
    return user


def create_card_owner(email, password, name, surname):
    user = CardOwner(user=create_user(email, password, name, surname))
    user.save()
    return user


def create_seller(email, password, name, surname):
    user = Seller(user=create_user(email, password, name, surname))
    user.save()
    return user


