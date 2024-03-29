from django.contrib import admin
from .models import Profile, UserLibrary,Review, UserNotes,Priority, Testimonial, TrackedProfile, UserWallet

admin.site.register(UserLibrary)
admin.site.register(UserNotes)
admin.site.register(Priority)
admin.site.register(Testimonial)
admin.site.register(TrackedProfile)

@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_customer_id']

@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['owner', 'amount']



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['freelancer', 'employer','comment' ,'project','rating', 'created', 'active']
    list_filter = ['freelancer', 'created', 'active']
    list_editable = ['active']

