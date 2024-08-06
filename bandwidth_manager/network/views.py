# network/views.py
from .notifications import send_notification
from .decorators.py import role_required
from asgiref.sync import async_to_sync
from .predictive_analytics import predict_traffic
from django.shortcuts import get_object_or_404, render
from .models import Device, TrafficData
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def send_websocket_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications_group',
        {
            'type': 'send_notification',
            'message': message
        }
    )

@role_required(['Admin', 'Network Manager'])
def add_policy(request):
    if request.method == 'POST':
        form = PolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.conditions = json.loads(request.POST.get('conditions'))
            policy.save()
            return redirect('policy_list')
    else:
        form = PolicyForm()
    return render(request, 'network/add_policy.html', {'form': form})


@role_required(['Admin', 'Network Manager', 'Viewer'])
def policy_list(request):
    policies = Policy.objects.all()
    return render(request, 'network/policy_list.html', {'policies': policies})

@login_required
def dashboard(request):
    traffic_data = TrafficData.objects.all().order_by('timestamp')
    labels = [data.timestamp.strftime('%Y-%m-%d %H:%M:%S') for data in traffic_data]
    incoming_traffic = [data.incoming_traffic for data in traffic_data]
    outgoing_traffic = [data.outgoing_traffic for data in traffic_data]

    plt.figure(figsize=(10, 5))
    plt.plot(labels, incoming_traffic, label='Incoming Traffic', color='blue')
    plt.plot(labels, outgoing_traffic, label='Outgoing Traffic', color='red')
    plt.xlabel('Time')
    plt.ylabel('Traffic')
    plt.title('Network Traffic Over Time')
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    return render(request, 'network/dashboard.html', {
        'graph': graph,
    })

    @role_required(['Admin'])
def manage_roles(request):
    roles = Role.objects.all()
    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        if role_id:
            role = get_object_or_404(Role, pk=role_id)
            role.permissions = request.POST.get('permissions')
            role.save()
    return render(request, 'network/manage_roles.html', {'roles': roles})

@login_required
@role_required(['Admin'])
def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_roles')
    else:
        form = RoleForm()
    return render(request, 'network/add_role.html', {'form': form})
    

def device_detail(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    traffic_data = TrafficData.objects.filter(device=device).order_by('-timestamp')[:10]
    return render(request, 'network/device_detail.html', {
        'device': device,
        'traffic_data': traffic_data
    })