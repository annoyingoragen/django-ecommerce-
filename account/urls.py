from django.urls import path

from .import views

urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('forgotpassword',views.forgotpassword,name="forgotpassword"),
    path('activate/<uidb64>/<token>/', views.activate,name='activate'),
    path('resetpassword_token/<uidb64>/<token>/', views.resetpassword_token,name='resetpassword_token'),
    path('resetpassword',views.resetpassword,name='resetpassword'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('my_order_detail/<int:order_id>',views.my_order_detail,name='my_order_detail'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('changepassword',views.changepassword,name='changepassword')
]