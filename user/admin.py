from django.contrib import admin
from .models import Profile, UserLibrary,Review

admin.site.register(Profile)
admin.site.register(UserLibrary)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['freelancer','employer','user','comment' ,'rating', 'bid','project','created', 'active']
    list_filter = ['created', 'active']
    list_editable = ['active']
