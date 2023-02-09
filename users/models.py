from django.contrib.auth.models import User, AbstractUser
from django.db import models

# from order.models import Order
from cart.models import Cart


class CommonUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)


class Customer(models.Model):
    user = models.OneToOneField(CommonUser, related_name="customer", on_delete=models.CASCADE)
    telephone_number = models.CharField(max_length=20)
    cart = models.OneToOneField(Cart, related_name="customer", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return self.user.first_name


class Employee(models.Model):
    user = models.OneToOneField(CommonUser, on_delete=models.CASCADE)
    education = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.first_name


class Administrator(Employee):
    user = models.OneToOneField(CommonUser, related_name="admin", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Administrator"
        verbose_name_plural = "Administrators"


class ContentManager(Employee):
    user = models.OneToOneField(CommonUser, related_name="content_manager", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Content Manager"
        verbose_name_plural = "Content managers"


class Consult(Employee):
    user = models.OneToOneField(CommonUser, related_name="consult", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Consultant"
        verbose_name_plural = "Consultants"
