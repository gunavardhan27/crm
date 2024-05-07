from django.urls import path
from account.views import Home,Con,Products,create_order,update_order,delete_order,Login,Register,logoutUser,Profile,profile_settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user/',Profile,name='user_profile'),
    path('settings/',profile_settings,name='profilesetting'),
    path('login/',Login,name='login_page'),
    path('logout/',logoutUser,name='logout_page'),
    path('register/',Register,name='register_page'),
    path('Customers/<str:pk>/',Con,name='customers'),
    path('Products/',Products,name='products'),
    path('',Home,name='home'),
    path('crt_order/<str:pk>/',create_order,name='createorder'),
    path('upd_order/<str:pk>/',update_order,name='updateorder'),
    path('del_order/<str:pk>/',delete_order,name='deleteorder'),


    path('reset_password/', auth_views.PasswordResetView.as_view(), name ='reset_password'),
  path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
  path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
]


