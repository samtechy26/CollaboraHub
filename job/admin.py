from django.contrib import admin
from .models import Category, Type, Job, Skill, Bid, denom
# Register your models here.
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Job)
admin.site.register(Skill)
admin.site.register(Bid)
admin.site.register(denom)

