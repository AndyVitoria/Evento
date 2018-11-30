from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('eventos/', views.get_eventos, name='eventos'),
    path('register/', views.criar_conta, name='register'),
    path('evento/<int:id>/', views.get_evento, name='evento'),
    path('carrinho/', views.get_carrinho, name='carrinho'),
    path('login/', views.login_evento, name='login'),
    path('logout/', views.logout_evento, name='logout'),
    path('evento/novo/', views.criar_evento, name='criar_evento')
]