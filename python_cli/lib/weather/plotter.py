
import plotext as plt
from datetime import datetime

def plot_forecast(location , times, temperatures):
    times = [datetime.fromisoformat(time).strftime('%d/%m/%Y %H:%M:%S') for time in times]
    plt.date_form('d/m/Y H:M:S')
    plt.plot(times, temperatures, marker='o', label='Temperature')
    plt.title(f'Temperature forecast for {location}')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.show()