# network/tasks.py
from celery import shared_task
from .models import NetworkDevice, TrafficData
from .snmp_utils import get_snmp_data

@shared_task
def collect_traffic_data():
    devices = NetworkDevice.objects.all()
    for device in devices:
        incoming_traffic = get_snmp_data(device.ip_address, device.snmp_community, '1.3.6.1.2.1.2.2.1.10.1')
        outgoing_traffic = get_snmp_data(device.ip_address, device.snmp_community, '1.3.6.1.2.1.2.2.1.16.1')
        TrafficData.objects.create(device=device, incoming_traffic=incoming_traffic, outgoing_traffic=outgoing_traffic)