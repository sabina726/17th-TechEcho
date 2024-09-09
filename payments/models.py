from django.conf import settings
from django.db import models


class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    STATUS_CHOICES = [
        ("pending", "Pending"),  # 訂單已建立但未支付
        ("paid", "Paid"),  # 訂單已支付
        ("failed", "Failed"),  # 訂單支付失敗
        ("refunded", "Refunded"),  # 訂單已退款
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    PAYMENT_CHOICES = [
        ("ecpay", "ECPAY"),  # 綠界支付
        ("linepay", "Linepay"),  # Linepay支付
    ]
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 訂單創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 訂單更新時間
    transaction_id = models.CharField(
        max_length=64, null=True, blank=True
    )  # 交易號碼 (主要是給linepay的專屬交易ID)
    payment_info = models.JSONField(null=True, blank=True)  # 保留作為後續其他用途

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
