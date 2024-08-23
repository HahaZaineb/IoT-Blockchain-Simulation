import random
import time

def generate_sensor_data():
    temperature = random.uniform(20.0, 30.0)  # Simulate temperature between 20°C and 30°C
    humidity = random.uniform(30.0, 50.0)  # Simulate humidity between 30% and 50%
    return {"temperature": temperature, "humidity": humidity}

while True:
    data = generate_sensor_data()
    print(f"Temperature: {data['temperature']:.2f}°C, Humidity: {data['humidity']:.2f}%")
    time.sleep(2)  # Wait for 2 seconds before generating new data
