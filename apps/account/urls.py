from django.urls import path
from apps.account.views import (
                                CustomerRegistrationView,
                                ActivateAccountView, 
                                UserLoginView,
                                SellerRegistrationView,
                                CustomerRetrieveUpdateDestroyView,
                                SellerRetrieveUpdateDestroyView
                                )


urlpatterns = [
    path("register/", CustomerRegistrationView.as_view(), name='customer_register'),
    path("register/seller/", SellerRegistrationView.as_view(), name='seller_register'),
    path('active/<str:uid64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('customerprofile/me', CustomerRetrieveUpdateDestroyView.as_view(), name='customerprofile'),
    path('customerprofile/<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='update_customerprofile'),
    path('sellerprofile/me', SellerRetrieveUpdateDestroyView.as_view(), name='sellerprofile'),
    path('sellerprofile/<int:pk>/', SellerRetrieveUpdateDestroyView.as_view(), name='update_sellerprofile')
]
