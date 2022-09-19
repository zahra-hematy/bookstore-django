from argparse import Namespace
from unicodedata import name
from django.urls import path
from . import views

app_name = 'store'
urlpatterns =[

    path('', views.StoreHome, name='index' ),
    path('about', views.hello_world, name='about' ),#store:about
    path('contact', views.contact, name='contact'),
    path('bookreq', views.BookRequestView.as_view(), name='bookreq'),
    path('cart/add/<int:bid>', views.Cart.as_view(),name='add_cart'),
    path('cart', views.CartDetail.as_view(), name='show_cart'),
    path('cart/remove/<int:pk>', views.CartRemoveView.as_view(),name='remove_cart'),
    path('cart/complete', views.InvoiceCreateView.as_view(), name='cart_complete'),
    path('invoice/<int:id>', views.InvoiceView.as_view(), name='invoce_show'),
    path('invoice/<int:invoice_id>/pay', views.PaymentView.as_view(), name='pay'),
    path('invoice/verify', views.PaymentVerifyView.as_view(), name='payverify')
]

