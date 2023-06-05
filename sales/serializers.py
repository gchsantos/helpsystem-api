from rest_framework import serializers

from sales.models import PlanDescription, Plan, Sale


class PlanDescriptionSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    valor = serializers.SerializerMethodField()
    descricao = serializers.SerializerMethodField()

    class Meta:
        model = PlanDescription
        fields = ('nome', 'valor', 'descricao')

    def get_nome(self, instance: PlanDescription):
        return instance.name

    def get_valor(self, instance: PlanDescription):
        return f'R$ {instance.value}'

    def get_descricao(self, instance: PlanDescription):
        return instance.description


class SaleSerializer(serializers.ModelSerializer):
    vendedor = serializers.SerializerMethodField()
    realizada_em = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ('vendedor', 'realizada_em')

    def get_vendedor(self, instance: Sale):
        return instance.seller.get_full_name()

    def get_realizada_em(self, instance: Sale):
        return instance.created_at


class PlanSerializer(serializers.ModelSerializer):
    descricao = serializers.SerializerMethodField()
    cliente = serializers.SerializerMethodField()
    venda = SaleSerializer(read_only=True, source='sale')

    class Meta:
        model = Plan
        fields = ('descricao', 'cliente', 'venda')

    def get_descricao(self, instance: Plan):
        return instance.plan_desc.name

    def get_cliente(self, instance: Plan):
        return instance.customer.get_full_name()
