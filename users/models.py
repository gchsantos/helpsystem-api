import uuid

from django.db import models

from django.contrib.auth.models import User


class CommonUser(User):
    common_id = models.UUIDField(default=uuid.uuid4, editable=False)
    GENDER_CHOICES = (
        (0, "Male"),
        (1, "Famale"),
        (2, "Other"),
    )
    cpf = models.CharField(max_length=11, null=False, blank=False)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    birth = models.DateField()

    class Meta:
        db_table = 'User'
        ordering = ['date_joined']


class Phones(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CommonUser, on_delete=models.CASCADE, null=True, related_name='phones')
    number = models.CharField(null=True, max_length=10)


class Adress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CommonUser, on_delete=models.CASCADE, null=True,
        related_name='adresses')
    neighborhood = models.CharField(null=True, max_length=100)
    number = models.CharField(null=True,  max_length=100)
    complement = models.CharField(null=True, max_length=100)
    city = models.CharField(null=True, max_length=100)


class Customer(CommonUser):
    class Meta:
        db_table = 'Customer'

    def get_activated_plan(self):
        return self.plans.filter(deactivated_at__isnull=True).order_by(
            '-sale__created_at').first()


class Seller(CommonUser):
    class Meta:
        db_table = 'Seller'
