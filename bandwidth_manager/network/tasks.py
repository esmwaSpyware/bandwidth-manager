# network/tasks.py
from celery import shared_task
from .models import Device
import requests

@shared_task
def check_device_health():
    devices = Device.objects.all()
    for device in devices:
        try:
            response = requests.get(f"http://{device.ip_address}/status", timeout=5)
            if response.status_code == 200:
                device.status = 'online'
                device.health = response.json().get('health', 'unknown')
            else:
                device.status = 'offline'
                device.health = 'unknown'
        except requests.RequestException:
            device.status = 'offline'
            device.health = 'unknown'
        device.save()
