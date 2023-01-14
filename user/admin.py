from django.contrib import admin
from .models import Profile, UserLibrary,Review
admin.site.register(Profile)
admin.site.register(UserLibrary)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['freelancer', 'employer','comment' ,'project','bid','rating', 'created', 'active']
    list_filter = ['freelancer', 'created', 'active']
    list_editable = ['active']

