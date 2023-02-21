from decimal import Decimal

from django.db import models

from order.constants import (DELIVERY_METHODS,
                             PAYMENT_METHODS,
                             PAYMENT_STATUS)

from cart.models import Position

from users.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    positions = models.ManyToManyField(Position, related_name="order", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(choices=DELIVERY_METHODS, max_length=15, null=True, blank=True)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=20, null=True, blank=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    post_index = models.IntegerField(null=True, blank=True)

    @property
    def numb_of_positions(self) -> int:
        return self.positions.count()

    @property
    def total_price(self) -> Decimal:
        order_and_positions = self.positions.prefetch_related("product")  # simplified to only 3 requests
        amounts = [i.amount for i in order_and_positions.all()]
        prices = [i.product.price for i in order_and_positions.all()]
        return sum([i * j for i, j in zip(amounts, prices)])

    @property
    def key(self) -> str:
        return f"{(hash(self.date))}"[1::5]

    @property
    def url(self) -> str:
        return "http://127.0.0.1:8000/orders/{}/{}/".format(self.customer.id, self.id)

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.id} order"
