from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('detail/', views.account_detail_and_change_password, name='detail'),
    path('delete_account/', views.delete_account, name='delete_account'),
]