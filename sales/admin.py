from django.contrib import admin

from .models import Sale, Plan, PlanDescription

admin.site.register([Sale, Plan, PlanDescription])
