# network/models.py
from django.contrib.auth.models import User
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.JSONField(default=dict)  # Permissions can be stored in a JSON format

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
class NetworkDevice(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    snmp_community = models.CharField(max_length=100)

class TrafficData(models.Model):
    device = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    incoming_traffic = models.BigIntegerField()
    outgoing_traffic = models.BigIntegerField()

class Policy(models.Model):
    name = models.CharField(max_length=100)
    max_bandwidth = models.IntegerField()
    conditions = models.JSONField(default=dict)  # Conditions stored as JSON
    ...

    def apply(self):
        # Logic to apply the policy based on conditions
        devices = Device.objects.all()
        for device in devices:
            if self.evaluate_conditions(device):
                # Apply policy to device
                pass

    def evaluate_conditions(self, device):
        for condition, value in self.conditions.items():
            if getattr(device, condition) != value:
                return False
        return True


class Device(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=50, default='unknown')
    last_checked = models.DateTimeField(auto_now=True)
    health = models.CharField(max_length=100, default='unknown')

class TrafficData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    incoming_traffic = models.BigIntegerField()
    outgoing_traffic = models.BigIntegerField()

