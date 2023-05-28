from django.db import models

from users.models import Customer, Seller


class PlanDescription(models.Model):
    ''' Descrição do Plano '''
    name = models.CharField(max_length=50)
    value = models.PositiveIntegerField()
    description = models.CharField(max_length=200)


class Sale(models.Model):
    ''' Registro das Vendas '''
    description = models.OneToOneField(
        PlanDescription, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class Plan(models.Model):
    ''' Planos dos Usuários '''
    description = models.OneToOneField(
        PlanDescription, on_delete=models.CASCADE, null=False)
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=False, related_name='plans')
    deactivated_at = models.DateField(null=True)
