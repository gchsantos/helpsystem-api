import time
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status
from pypix import Pix

from sales.models import PlanDescription, Sale, Plan
from sales.serializers import PlanDescriptionSerializer, PlanSerializer
from sales.constants import ErrorMessages, SuccessMessages, PERMITTED_OPERATIONS
from users.models import Customer, Seller
from helpsystem_api.messages import ReturnBaseMessage
from utils.qrcode import generate_qr


class PlanDescriptionView(APIView):
    '''View de descrição dos Planos'''

    def get(self, request, **kwargs):
        '''Serve para listar a descrição de todos os tipos de planos'''
        plans = PlanDescription.objects.all()
        plans_serialized = PlanDescriptionSerializer(plans, many=True)
        return ReturnBaseMessage(detail=plans_serialized.data).message


class SaleView(APIView):
    ''' View de vendas '''

    def post(self, request, **kwargs):
        '''Criação de uma venda '''
        try:
            data_customer = request.data['customer']
            data_plan = request.data['plan']
            data_seller = request.data['seller']
        except KeyError as err:
            return ReturnBaseMessage(
                success=False,
                detail=f"{ErrorMessages.MISSING_VALUE_MESSAGE}'{err}'").message

        # Validações
        try:
            customer = Customer.objects.get(common_id=data_customer)
            plan = PlanDescription.objects.get(id=data_plan)
            seller = Seller.objects.get(common_id=data_seller)

            if customer.get_activated_plan():
                return ReturnBaseMessage(
                    False, ErrorMessages.PLAN_ALREADY_EXIST, status.HTTP_400_BAD_REQUEST).message

        except Customer.DoesNotExist:  # Quando o cliente não existe
            return ReturnBaseMessage(
                success=False, details=ErrorMessages.CUSTOMER_DOES_NOT_EXIST,
                code=status.HTTP_400_BAD_REQUEST).message
        except Seller.DoesNotExist:  # Quando o vendedor não existe
            return ReturnBaseMessage(
                success=False, detail=ErrorMessages.SELLER_DOES_NOT_EXIST,
                code=status.HTTP_400_BAD_REQUEST).message
        except PlanDescription.DoesNotExist:  # Quando o plano não existe
            return ReturnBaseMessage(
                success=False, detail=ErrorMessages.PLAN_DESC_DOES_NOT_EXIST,
                code=status.HTTP_400_BAD_REQUEST).message

        with transaction.atomic():
            # Criação de venda
            created_sale = Sale(
                plan_desc=plan,
                customer=customer,
                seller=seller,
            )
            created_sale.save()

            # Criação do plano e relacionamento com a venda
            Plan(
                plan_desc=plan,
                sale=created_sale,
                customer=customer
            ).save()

        return ReturnBaseMessage(
            code=status.HTTP_201_CREATED, detail=SuccessMessages.SELL_CREATED,
            plan_id=created_sale.id).message

    def get(self, request, sale_id, **kwargs):

        # Validações
        try:
            sale = Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:  # Quando o plano não existe
            return ReturnBaseMessage(
                success=False, detail=ErrorMessages.SALE_DOES_NOT_EXIST,
                code=status.HTTP_400_BAD_REQUEST).message

        pix = Pix()
        pix.pixkey = settings.PIX_KEY
        pix.description = f"{settings.PIX_DESCRIPTION}{sale.plan_desc.name}"
        pix.merchant_name = settings.PIX_MERCHANT_NAME
        pix.merchant_city = settings.PIX_MERCHANT_CITY
        pix.txid = settings.PIX_MERCHANT_NAME
        pix.amount = str(sale.plan_desc.value)

        qr_name = f"{sale.id}"
        qr_url = generate_qr(str(pix), qr_name)

        return render(
            request, 'sale_success.html',
            {'qrcode_path': qr_url, 'pix_code': str(pix)})


class PlanView(APIView):
    ''' View para os planos dos usuários'''

    def get(self, request, **kwargs):
        '''Serve para listar os planos ativos dos usuários'''
        filters = {}
        active = request.GET.get('active')
        if active:
            if active.lower() == 'true':
                filters['deactivated_at__isnull'] = True
            if active.lower() == 'false':
                filters['deactivated_at__isnull'] = False

        plans = Plan.objects.filter(**filters)
        plans_serialized = PlanSerializer(plans, many=True)
        return ReturnBaseMessage(detail=plans_serialized.data).message

    def put(self, request, plan_id, **kwargs):
        '''Alteração de plano '''

        try:
            operation = request.data['operation']
        except KeyError as err:
            return ReturnBaseMessage(
                success=False,
                detail=f"{ErrorMessages.MISSING_VALUE_MESSAGE}'{err}'").message

        # Validações
        if operation not in PERMITTED_OPERATIONS:
            return ReturnBaseMessage(
                False, ErrorMessages.NOT_PERMITTED_OPERATION, status.HTTP_400_BAD_REQUEST).message

        try:
            customer_plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:  # Quando o plano do cliente não existe
            return ReturnBaseMessage(
                success=False, detail=ErrorMessages.CUSTOMER_PLAN_DOES_NOT_EXIST,
                code=status.HTTP_400_BAD_REQUEST).message

        if operation == 'deactivate':
            if not customer_plan.deactivated_at:
                customer_plan.deactivated_at = datetime.now()
                customer_plan.save()

        return ReturnBaseMessage(
            code=status.HTTP_201_CREATED,
            detail=SuccessMessages.PLAN_DESACTIVATED).message
