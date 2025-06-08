"""
URL configuration for site_constructor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from constructor.views import RegisterView, GreetView, SampleView, SamplesView, ImageView,\
    VerifyCodeView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('greet', GreetView.as_view(), name='greet'),
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/verify-email', VerifyCodeView.as_view(), name='verify-email'),
    path('api/sample', SampleView.as_view(), name='sample'),
    path('api/sample/<int:id>', SampleView.as_view(), name='sample_get'),
    path('api/sample/list', SampleView.as_view(), name='sample_list'),
    path('api/sample/state', SampleView.as_view(), name='sample_state'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/samples', SamplesView.as_view(), name='samples'),
    path('api/image', ImageView.as_view(), name='image_save')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
