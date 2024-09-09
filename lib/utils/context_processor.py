from random import seed
from django.conf import settings
from users.models import User

def fetch_user_notifications(request):
    if request.user.is_authenticated:
        user = User.objects.prefetch_related("notification_set").get(pk=request.user.id)
        return {"user_with_notifications": user}
    return {}