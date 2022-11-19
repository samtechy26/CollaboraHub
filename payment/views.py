import stripe
import logging
from coinbase_commerce.client import Client
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from job.models import Bid

stripe.api_key = settings.STRIPE_SECRET_KEY
coinbase_api_key = settings.COINBASE_COMMERCE_API_KEY
YOUR_DOMAIN = "http://127.0.0.1:8000"

class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"
    

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Bid.objects.get(id=product_id) 
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

# Coinbase crypto payment
def create_coinbase_payment(request, *args, **kwargs):
    product_id = kwargs["pk"]
    product = Bid.objects.get(id=product_id)
    client = Client(api_key=coinbase_api_key)
    product_details = {
        'name': product.job.title,
        'description': product.job.description,
        'local_price':{
            'amount':product.Amount,
            'currency':'USD'
        },
        'pricing_type':'fixed_price',
        'redirect_url': YOUR_DOMAIN + '/success/',
        'cancel_url': YOUR_DOMAIN + '/cancel/',
        'metadata':{
            'customer_id': request.user.id if request.user.is_authenticated else None,
            'customer_username': request.user.username if request.user.is_authenticated else None
        }

    }

    charge = client.charge.create(**product_details)
    return render(request, 'payment\coinbase.html', {
        "charge":charge
    })


@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(
            request_data, request_sig, webhook_secret)
        if event['type'] == 'charge:confirmed':
            logger.info('Payment confirmed.')
            customer_id = event['data']['metadata']['customer_id']
            customer_username = event['data']['metadata']['customer_username']

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)

    

