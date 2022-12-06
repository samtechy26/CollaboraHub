from django.db import models
from django.contrib.auth.models import User
from job.models import Bid
from django.db.models.signals import post_save
from PIL import Image
from django.urls import reverse




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(default = 'default.png', upload_to='profile_pics')
    tagline = models.CharField(max_length=200,  default='Enter your tagline here')
    bio = models.CharField(max_length=1000, default='Enter your bio here')
    favourite = models.ManyToManyField(User, related_name='favorited_by', blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'


    def get_absolute_url(self):
        return reverse("profile", kwargs={
            "id": self.id
        })
    
    def get_update_url(self):
        return reverse('profile-update', kwargs={
            "id": self.id
        })


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) 

class UserLibrary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Bid, blank=True)

    class Meta:
        verbose_name_plural = "UserLibraries"

    def __str__(self):
        return self.user.email

def post_save_user_receiver(sender, instance, created, **kwargs):
    if created:
        UserLibrary.objects.create(user=instance)


post_save.connect(post_save_user_receiver, sender=User)