from django.views import View
from job.models import Bid
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Bid.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = product.job.author.email,
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.Amount * 100,
                        'product_data': {
                            'name': product.job.title,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
