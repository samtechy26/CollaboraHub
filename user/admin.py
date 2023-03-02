from django.contrib import admin
from .models import Profile, UserLibrary,Review, UserNotes,Priority, Testimonial, TrackedProfile, UserWallet
admin.site.register(Profile)
admin.site.register(UserLibrary)
admin.site.register(UserNotes)
admin.site.register(Priority)
admin.site.register(Testimonial)
admin.site.register(TrackedProfile)
admin.site.register(UserWallet)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['freelancer', 'employer','comment' ,'project','rating', 'created', 'active']
    list_filter = ['freelancer', 'created', 'active']
    list_editable = ['active']

