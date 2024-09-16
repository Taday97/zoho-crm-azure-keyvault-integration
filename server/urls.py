"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from server.views import leadsView
from server.views import zohoView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', zohoView.some_view),
    path('zoho/auth/', zohoView.zoho_auth, name='zoho/auth'),
    path('zoho/callback/', zohoView.zoho_callback, name='zoho_callback'),

    path('some/', zohoView.some_view, name='some_view'),
    path('products_group/', zohoView.get_products_group, name='get_products_group'),
    path('subscriptions/', zohoView.get_subscriptions, name='get_subscriptions'),
    path('plans/', zohoView.get_plans, name='get_plans'),
    path('quotes/', zohoView.get_quotes, name='get_quotes'),
     
    path('saveLeads', zohoView.saveLeads, name='saveLeads'),

    # Routes for'Leads'
    path('leads/', leadsView.GetAll.as_view()),
]
