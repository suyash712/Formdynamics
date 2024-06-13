from datetime import timedelta
from django.utils import timezone
from grnentry.models import calibration, Notification

def generate_notifications():
    now = timezone.now()
    due_date = now + timedelta(days=2)
    calibrations_due_soon = calibration.objects.filter(next_calibration_due_date__lte=due_date, next_calibration_due_date__gt=now)

    for calibration in calibrations_due_soon:
        message = f"Calibration due for {calibration.inst_name} on {calibration.next_calibration_due_date.strftime('%Y-%m-%d')}"
        Notification.objects.create(message=message, calibration=calibration)