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
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserCreate
from sales.views import PlanDescriptionView, SaleView, PlanView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', UserCreate.as_view(), name='Registrar'),
    path('account/auth', obtain_auth_token, name='Autenticar'),
    path('plans-description/', PlanDescriptionView.as_view(), name='Descricao de Planos'),
    path('plan/', PlanView.as_view(), name='Listagem de Planos'),
    path('plan/<uuid:plan_id>/', PlanView.as_view(), name='Alterar Plano'),
    path('sale/', SaleView.as_view(), name='Listagem de Vendas'),
    path('sale/<uuid:sale_id>/', SaleView.as_view(), name='Venda'),
]

if settings.DEBUG:
    urlpatterns += static(settings.QRCODES_URL,
                          document_root=settings.QRCODES_ROOT)
