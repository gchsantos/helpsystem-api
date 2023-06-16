"""
URL configuration for helpsystem_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken

from users.views import CustomerCreate, SellerCreate, CommonUserView
from sales.views import PlanDescriptionView, SaleView, SalePaymentView, PlanView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', CustomerCreate.as_view(), name='Cadastrar Cliente'),
    path('seller/', SellerCreate.as_view(), name='Cadastrar Vendedor'),
    path('account/auth/', csrf_exempt(ObtainAuthToken.as_view()), name='Autenticar'),
    path('account/', CommonUserView.as_view(), name='CommonUser'),
    path('plans-description/', PlanDescriptionView.as_view(), name='Descricao de Planos'),
    path('plan/', PlanView.as_view(), name='Listagem de Planos'),
    path('plan/<uuid:plan_id>/', PlanView.as_view(), name='Alterar Plano'),
    path('sale/', SaleView.as_view(), name='Listagem de Vendas'),
    path('sale/<uuid:sale_id>/', SalePaymentView.as_view(), name='Pagamento da Venda'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.QRCODES_URL, document_root=settings.QRCODES_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
