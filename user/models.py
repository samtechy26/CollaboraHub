from django.db import models
from django.contrib.auth.models import User
from job.models import Bid, Job
from django.db.models.signals import post_save
from PIL import Image
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# class User(User):
#     pass
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(default = 'default.png', upload_to='profile_pics')
    tagline = models.CharField(max_length=200,  default='Enter your tagline here')
    bio = models.TextField(max_length=1000, default='Enter your bio here')
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


class Review(models.Model):
    employer = models.ForeignKey(Profile,related_name="employer_review", null=True, blank=True, on_delete=models.SET_NULL)
    freelancer = models.ForeignKey(Profile, related_name="freelancer_review" ,null = True,blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User,  null=True,blank=True, on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, null=True,blank=True, related_name='reviews' , on_delete=models.SET_NULL) 
    project = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviews")
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    timely = models.BooleanField(default=False)
    on_budget = models.BooleanField(default=False)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ('-created',)


    def clean(self):
        if (self.employer == None and self.freelancer == None) or (self.bid == None and self.project == None):
            raise ValidationError("Both Employer and freelancer cannot be empty")
            
    def __str__(self):
        if (self.employer is not None):
            return str(self.user.username + " reviewed " + self.employer.user.username)
        elif(self.freelancer is not None):
            return str(self.user.username +" reviewed " + self.freelancer.user.username)
        else:
            return str(self.id)



