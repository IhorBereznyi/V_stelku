from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckoutView,
    MakeOrderView,
    LoginView,
    RegistrationView,
    ProfileView,
    Base_ViewPriceLow,
    Base_ViewPriceH,
    Base_ViewPrice_Sale,
    BaseView_data_new,
    BaseView_data_old

)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('base_price_low/', Base_ViewPriceLow.as_view(), name='base_price_low'),
    path('base_price_h/', Base_ViewPriceH.as_view(), name='base_price_h'),
    path('base_data_new/', BaseView_data_new.as_view(), name='base_data_new'),
    path('base_data_old/', BaseView_data_old.as_view(), name='base_data_old'),
    path('base_sale/', Base_ViewPrice_Sale.as_view(), name='base_sale'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile')
]
