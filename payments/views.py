import os
import uuid

from django.http import HttpResponse
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from linepay import LinePayApi

from .ecpay.ecpay_create_order import ecpay_api
from .models import Payment


# ECPay
def index(request):
    return render(request, "payments/index.html")


def mentor(request):
    return render(request, "payments/mentor.html")


def payment_option(request):
    return render(request, "payments/payment_option.html")


def ecpay(request):
    return HttpResponse(ecpay_api())


@csrf_exempt
def after_pay(request):
    return render(request, "payments/after_pay.html")


# LinePay
def linepay_index(request):
    return render(request, "payments/linepay_index.html")


def linepay_create_payment(request):
    plan = request.GET.get("plan", "basic")

    # Set the amount based on the selected plan
    if plan == "premium":
        amount = 600  # Example amount for Premium VIP
    else:
        amount = 0  # Free for Basic plan

    currency = "TWD"
    order_id = str(uuid.uuid4())

    # Create payment object in your database
    payment = Payment.objects.create(
        order_id=order_id,
        amount=amount,
        currency=currency,
    )

    # Initialize the LINE Pay API client
    line_pay = LinePayApi(
        channel_id=os.getenv("LINE_PAY_CHANNEL_ID", "your_channel_id"),
        channel_secret=os.getenv("LINE_PAY_CHANNEL_SECRET", "your_channel_secret"),
        is_sandbox=True,  # Set to False for production
    )

    # Set up the payment request payload for LINE Pay
    payload = {
        "amount": amount,
        "currency": currency,
        "orderId": order_id,
        "packages": [
            {
                "id": "package_id",
                "amount": amount,
                "name": f"{plan.capitalize()} VIP Plan",
                "products": [
                    {
                        "name": f"TechEcho {plan.capitalize()} Plan",
                        "quantity": 1,
                        "price": amount,
                    }
                ],
            }
        ],
        "redirectUrls": {
            "confirmUrl": request.build_absolute_uri(
                reverse("payments:linepay_confirm_payment")
            ),
            "cancelUrl": request.build_absolute_uri(
                reverse("payments:linepay_cancel_payment")
            ),
        },
    }

    # Make the payment request using the SDK
    try:
        response = line_pay.request(payload)
        if response["returnCode"] == "0000":
            # Save transaction ID to the payment object
            payment.transaction_id = response["info"]["transactionId"]
            payment.save()

            # Redirect the user to the LINE Pay payment page
            return redirect(response["info"]["paymentUrl"]["web"])
        else:
            return render(
                request,
                "payments/payment_error.html",
                {"error": response["returnMessage"]},
            )
    except Exception as e:
        return render(request, "payments/payment_error.html", {"error": str(e)})


def linepay_confirm_payment(request):
    return HttpResponse("Payment confirmed!")


def linepay_cancel_payment(request):
    return HttpResponse("Payment canceled!")
