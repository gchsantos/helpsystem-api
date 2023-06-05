from typing import Iterable, Optional
import uuid

from django.db import models

from users.models import Customer, Seller


class PlanDescription(models.Model):
    ''' Descrição do Plano '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    value = models.FloatField()
    description = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Sale(models.Model):
    ''' Registro das Vendas \n
    Armazena historicamente todas as vendas realizadas, trazendo informações de vendedor/cliente'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_desc = models.ForeignKey(
        PlanDescription, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.customer.get_full_name()} - {self.plan_desc.name} - {self.created_at}"


class Plan(models.Model):
    ''' Planos dos Usuários \n
    Indica todos os planos gerados através de uma venda, é possível validar se o plano está ativo.'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_desc = models.ForeignKey(
        PlanDescription, on_delete=models.CASCADE, null=False)
    sale = models.OneToOneField(
        Sale, on_delete=models.CASCADE, null=False, related_name='sale')
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=False, related_name='plans')
    deactivated_at = models.DateField(null=True)

    @property
    def is_active(self) -> bool:
        return False if self.deactivated_at else True

    def __str__(self) -> str:
        return f"{'Ativo:' if self.is_active else 'Desativado:'} {self.customer.get_full_name()} - {self.plan_desc.name}"
