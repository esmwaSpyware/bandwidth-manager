from rest_framework import serializers
from .models import NetworkDevice, TrafficData, Policy

class NetworkDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDevice
        fields = ['id', 'name', 'ip_address', 'snmp_community']

class TrafficDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficData
        fields = ['id', 'device', 'timestamp', 'incoming_traffic', 'outgoing_traffic']

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'name', 'bandwidth_limit', 'priority', 'device']
