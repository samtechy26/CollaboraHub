import stripe
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, UserWallet

stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        account = stripe.Account.create(
            type='express',
        )
        stripe_id = account["id"]
        Profile.objects.create(user=instance, stripe_customer_id=stripe_id)
        
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
   instance.profile.save()


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        UserWallet.objects.create(owner=instance, amount=0)


@receiver(post_save, sender=User)
def save_wallet(sender, instance, **kwargs):
   instance.userwallet.save()
