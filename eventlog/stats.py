from datetime import datetime, timedelta

from authentication.models import Account


def used_active(days):
    used = Account.objects.filter(
        log__timestamp__gt=datetime.now() - timedelta(days=days)
    ).distinct().count()

    active = Account.objects.filter(
        log__timestamp__gt=datetime.now() - timedelta(days=days)
    ).exclude(
        date_joined__gt=datetime.now() - timedelta(days=days)
    ).distinct().count()

    return used, active


def stats():
    used_seven, active_seven = used_active(7)
    used_thirty, active_thirty = used_active(30)

    return {
        "used_seven": used_seven,
        "used_thirty": used_thirty,
        "active_seven": active_seven,
        "active_thirty": active_thirty
    }
