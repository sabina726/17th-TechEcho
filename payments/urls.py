from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.index, name="index"),
    path("mentor", views.mentor, name="mentor"),
    path("payment_option", views.payment_option, name="payment_option"),
    path("ecpay", views.ecpay, name="ecpay"),
    path("after_pay", views.after_pay, name="after_pay"),
    path(
        "linepay_index", views.linepay_index, name="linepay_index"
    ),  # This is the root of the payments app
    path(
        "linepay_create/", views.linepay_create_payment, name="linepay_create_payment"
    ),
    path(
        "linepay_confirm/",
        views.linepay_confirm_payment,
        name="linepay_confirm_payment",
    ),
    path(
        "linepay_cancel/", views.linepay_cancel_payment, name="linepay_cancel_payment"
    ),
]
