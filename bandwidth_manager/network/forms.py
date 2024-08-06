# network/forms.py
from django import forms
from .models import NetworkDevice, Policy

class NetworkDeviceForm(forms.ModelForm):
    class Meta:
        model = NetworkDevice
        fields = ['name', 'ip_address', 'snmp_community']

class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['name', 'max_bandwidth', 'conditions']

    conditions = forms.CharField(widget=forms.Textarea, help_text='Enter conditions in JSON format.')