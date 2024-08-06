# network/predictive_analytics.py
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import TrafficData

def predict_traffic():
    traffic_data = TrafficData.objects.all().order_by('timestamp')
    timestamps = np.array([data.timestamp.timestamp() for data in traffic_data]).reshape(-1, 1)
    incoming_traffic = np.array([data.incoming_traffic for data in traffic_data])
    outgoing_traffic = np.array([data.outgoing_traffic for data in traffic_data])

    model_incoming = LinearRegression().fit(timestamps, incoming_traffic)
    model_outgoing = LinearRegression().fit(timestamps, outgoing_traffic)

    future_timestamp = np.array([max(timestamps) + 3600]).reshape(-1, 1)  # Predict for the next hour
    predicted_incoming = model_incoming.predict(future_timestamp)
    predicted_outgoing = model_outgoing.predict(future_timestamp)

    return predicted_incoming[0], predicted_outgoing[0]
