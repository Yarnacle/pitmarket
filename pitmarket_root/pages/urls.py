from django.urls import path
from . import views
from .views import Register,LoginView,RegisterSuccess
from django.contrib.auth.views import LogoutView
from django.urls import include

urlpatterns = [
	path('register/',Register.as_view(),name = 'register'),
	path('login/',LoginView.as_view(),name = 'login'),
	path('credit/',views.credit,name = 'credit'),
	path('logout/',LogoutView.as_view(),name = 'logout'),
	path('register/success/',RegisterSuccess.as_view(),name='register-success'),
]
