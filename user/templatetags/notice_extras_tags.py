from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def notice_count(request):
    user = request.user
    user_notification = user.notifications.filter(verb="application for bid")
    count = user_notification.count()
    return count