# network/anomaly_detection.py
import numpy as np
from sklearn.ensemble import IsolationForest
from .models import TrafficData

def detect_anomalies():
    traffic_data = TrafficData.objects.all().values('incoming_traffic', 'outgoing_traffic')
    data = np.array([[td['incoming_traffic'], td['outgoing_traffic']] for td in traffic_data])
    model = IsolationForest(contamination=0.01)
    model.fit(data)
    anomalies = model.predict(data)
    anomaly_indices = [i for i, val in enumerate(anomalies) if val == -1]
    return anomaly_indices
