"""FindGene URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from system.views_user import IndexView, LoginView, LogoutView
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from system.views import SystemView
from NIPT.views import NIPTView
from NIPT.views import NIPTDataImportView
from NIPT.views import NIPTDataImportTableView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('system/', SystemView.as_view(), name='system'),
    path('NIPT/', NIPTView.as_view(), name='NIPT'),
    path('NIPT/DataImport/', NIPTDataImportView.as_view(), name='NIPT_DataImport'),
    path('NIPT/DataImport/DataTable', NIPTDataImportTableView.as_view(), name='NIPT_DataTable'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    ]