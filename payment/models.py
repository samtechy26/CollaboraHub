# from django.db import models
# from job.models import Bid
# from django.contrib.auth.models import User



# class OrderItem(models.Model):
#     order = models.ForeignKey(
#         "Order", related_name='item', on_delete=models.CASCADE)
#     product = models.ForeignKey(Bid, on_delete=models.CASCADE)


#     @property
#     def reference_number(self):
#         return f"#BID-{self.pk}"

#     def __str__(self):
#         return self.reference_number

#     def get_raw_total_item_price(self):
#         return self.product.price

#     def get_total_item_price(self):
#         price = self.get_raw_total_item_price()  # 1000
#         return "{:.2f}".format(price * 100)


# class Order(models.Model):
#     user = models.ForeignKey(
#         User, blank=True, null=True, on_delete=models.CASCADE)
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered_date = models.DateTimeField(blank=True, null=True)
#     ordered = models.BooleanField(default=False)

    

#     def __str__(self):
#         return self.reference_number

#     @property
#     def reference_number(self):
#         return f"ORDER-{self.pk}"

#     def get_raw_subtotal(self):
#         return self.get_raw_total_item_price()
        

#     def get_subtotal(self):
#         subtotal = self.get_raw_subtotal()
#         return "{:.2f}".format(subtotal * 100)

#     def get_raw_total(self):
#         subtotal = self.get_raw_subtotal()
#         # add tax, add delivery, subtract discounts
#         # total = subtotal - discounts + tax + delivery
#         return subtotal

#     def get_total(self):
#         total = self.get_raw_total()
#         return "{:.2f}".format(total * 100)



# class Payment(models.Model):
#     order = models.ForeignKey(
#         Order, on_delete=models.CASCADE, related_name='payments')
#     payment_method = models.CharField(max_length=20, choices=(
#         ('PayPal', 'PayPal'),
#         ('Stripe', 'Stripe')
#     ))
#     timestamp = models.DateTimeField(auto_now_add=True)
#     successful = models.BooleanField(default=False)
#     amount = models.FloatField()
#     raw_response = models.TextField()

#     def __str__(self):
#         return self.reference_number

#     @property
#     def reference_number(self):
#         return f"PAYMENT-{self.order}-{self.pk}"

