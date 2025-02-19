import numpy as np
import paho.mqtt.client as mqtt
import time
from pylsl import StreamInlet, resolve_byprop

# Configuraci�n del broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "dron/senales"

# Inicializar cliente MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado exitosamente al broker MQTT")
    else:
        print(f"Error de conexi�n MQTT con c�digo {rc}")

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Definir umbrales adaptativos
THRESHOLD_FACTOR = 3
MIN_AMPLITUDE_CHANGE = 50.293
VARIABILITY_THRESHOLD = 35
DURATION_LEFT_RANGE = (1.40, 2.20)
DURATION_RIGHT_THRESHOLD = 2.20
STABILITY_WINDOW = 12
SUSTAINED_THRESHOLD = 5
WINDOW_SIZE = 500  # Tama�o de la ventana deslizante para la desviaci�n est�ndar

def detect_large_excitations():
    print("Conectando al stream EEG...")
    streams = resolve_byprop('type', 'EEG', timeout=10)

    if not streams:
        print("No se encontr� ning�n stream EEG. Aseg�rate de que Muse est� transmitiendo.")
        return

    inlet = StreamInlet(streams[0])
    print("Conexi�n al stream EEG exitosa.")

    timestamps = []
    values = []
    in_event = False
    start_time = None
    peak_value = None
    stable_count = 0
    sustained_count = 0
    min_duration_threshold = 0.1

    while True:
        sample, timestamp = inlet.pull_sample()
        tp10 = sample[3]  # Suponiendo que TP10 es el cuarto canal
        print(f"Timestamp: {timestamp}, TP10: {tp10}")

        if len(values) > 1:
            # C�lculo de la desviaci�n est�ndar en ventana deslizante
            if len(values) > WINDOW_SIZE:
                threshold = THRESHOLD_FACTOR * np.std(values[-WINDOW_SIZE:])
            else:
                threshold = THRESHOLD_FACTOR * np.std(values)

            variability = abs(tp10 - values[-1])

            if variability > VARIABILITY_THRESHOLD and abs(tp10 - values[0]) > MIN_AMPLITUDE_CHANGE:
                sustained_count += 1
                if sustained_count >= SUSTAINED_THRESHOLD:
                    stable_count = 0
                    if not in_event:
                        start_time = timestamp
                        peak_value = tp10
                        in_event = True
                        print("Inicio de excitaci�n detectado")
                    elif abs(tp10 - peak_value) > MIN_AMPLITUDE_CHANGE:
                        peak_value = tp10
            else:
                sustained_count = 0
                if in_event:
                    stable_count += 1
                    if stable_count >= STABILITY_WINDOW and abs(tp10 - peak_value) < (MIN_AMPLITUDE_CHANGE / 2):
                        end_time = timestamp
                        duration = end_time - start_time

                        if duration >= min_duration_threshold:
                            print(f"Excitaci�n completada - Duraci�n: {duration:.2f} segundos")
                            if DURATION_LEFT_RANGE[0] <= duration <= DURATION_LEFT_RANGE[1]:
                                client.publish(MQTT_TOPIC, "izquierda")
                                print(f"Publicado en MQTT: 'izquierda' en {MQTT_TOPIC}")
                            elif duration > DURATION_RIGHT_THRESHOLD:
                                client.publish(MQTT_TOPIC, "derecha")
                                print(f"Publicado en MQTT: 'derecha' en {MQTT_TOPIC}")

                        in_event = False
                        stable_count = 0

        values.append(tp10)
        timestamps.append(timestamp)

        if len(values) > 1000:
            values.pop(0)
            timestamps.pop(0)

        time.sleep(0.01)

if __name__ == "__main__":
    detect_large_excitations()
