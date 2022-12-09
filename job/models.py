from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404


User = get_user_model()
# Create your models here.
Experience = range(1, 60)
Gender = ['male', 'female','Any']
Shift = ['Day', 'Night', 'Any']


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, default=None, unique=True)
    img = models.ImageField(default = 'default.png', upload_to='category_images')

    def __str__(self):
        return self.title

class Type(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Skill(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title





class Job(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    job_type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    job_category = models.ManyToManyField(Category)
    cost = models.IntegerField(default=100)
    skill = models.ManyToManyField(Skill, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=10000)
    favourite = models.ManyToManyField(User, related_name='fav_task', blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('dashboard')
        # return reverse('post-detail', kwargs={'pk':self.pk})


class denom(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Bid(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Amount = models.IntegerField(default=1000)
    stripe_payment_intent = models.CharField(max_length=200, default="completed")
    has_paid = models.BooleanField( default=False,verbose_name='Payment Status')
    ordered_date = models.DateTimeField(blank=True, null=True)
    time = models.IntegerField(default=1)
    denom = models.ForeignKey(denom, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    


    @property
    def reference_number(self):
         return f"#BID-{self.pk}#{self.job.title}"

    
    def __str__(self):
        return self.reference_number

    def get_absolute_url(self):
        return reverse("bid-detail", kwargs={
            "id": self.pk
        })
    
    def get_update_url(self):
        return reverse('job:bid-update', kwargs={
            "id": self.pk
        })

    def get_delete_url(self):
        return reverse('job:bid-delete', kwargs={
            "id": self.pk
        })

    


    def __str__(self):
        return f'{self.job} bidded for by {self.user}'



# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
#     comment = models.TextField(max_length=500)
#     rate = models.IntegerField(default=0)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Review by {self.user} on {self.bid}'

