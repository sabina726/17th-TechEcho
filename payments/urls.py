from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "ecpay_create_payment/", views.ecpay_create_payment, name="ecpay_create_payment"
    ),
    path("ecpay_return/", views.ecpay_return, name="ecpay_return"),
    path("ecpay_after_pay/", views.ecpay_after_pay, name="ecpay_after_pay"),
    path(
        "linepay_create_payment/",
        views.linepay_create_payment,
        name="linepay_create_payment",
    ),
    path(
        "linepay_confirm/",
        views.linepay_confirm_payment,
        name="linepay_confirm_payment",
    ),
    path(
        "linepay_cancel/", views.linepay_cancel_payment, name="linepay_cancel_payment"
    ),
    path("disable_premium/", views.disable_premium, name="disable_premium"),
    path("delete_order/", views.delete_order, name="delete_order"),
    path("update_order/", views.update_order, name="update_order"),
]
