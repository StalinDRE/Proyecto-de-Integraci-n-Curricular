import numpy as np
import paho.mqtt.client as mqtt
import time
from pylsl import StreamInlet, resolve_byprop

# Configuración del broker MQTT
MQTT_BROKER = "localhost"  # Cambia esto a la IP de tu servidor Mosquitto si está en otra máquina
MQTT_PORT = 1883
MQTT_TOPIC = "dron/senales"

# Inicializar cliente MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado exitosamente al broker MQTT")
    else:
        print(f"Error de conexión MQTT con código {rc}")

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Definir umbral para detectar excitaciones
THRESHOLD_FACTOR = 3  # Aumentar el umbral para reducir sensibilidad
MIN_AMPLITUDE_CHANGE = 50.293  # Cambio mínimo de amplitud para considerar excitación
VARIABILITY_THRESHOLD = 35  # Variabilidad mínima para considerar inicio de excitación
DURATION_LEFT_RANGE = (1.40, 2.20)
DURATION_RIGHT_THRESHOLD = 2.20
STABILITY_WINDOW = 12  # Número de muestras consecutivas estables necesarias para cerrar la excitación
SUSTAINED_THRESHOLD = 5  # Número de muestras consecutivas necesarias para confirmar una excitación
SEARCH_WINDOW_START = 10  # Mínimo de muestras después del fin de la excitación para buscar el valle
SEARCH_WINDOW_END = 100   # Máximo de muestras para buscar el valle más pronunciado

def detect_large_excitations():
    print("Conectando al stream EEG...")
    streams = resolve_byprop('type', 'EEG', timeout=10)
    
    if not streams:
        print("No se encontró ningún stream EEG. Asegúrate de que Muse esté transmitiendo.")
        return
    
    inlet = StreamInlet(streams[0])
    print("Conexión al stream EEG exitosa.")
    
    timestamps = []
    values = []
    in_event = False
    start_time = None
    peak_value = None
    stable_count = 0
    sustained_count = 0
    min_duration_threshold = 0.1  # Mínimo tiempo que debe durar una excitación válida
    
    while True:
        sample, timestamp = inlet.pull_sample()
        tp10 = sample[3]  # Suponiendo que TP10 es el cuarto canal
        print(f"Timestamp: {timestamp}, TP10: {tp10}")  # Debugging de valores
        
        if len(values) > 1:
            variability = abs(tp10 - values[-1])
            threshold = THRESHOLD_FACTOR * np.std(values[-50:]) if len(values) > 50 else THRESHOLD_FACTOR * np.std(values)
            
            if variability > VARIABILITY_THRESHOLD and abs(tp10 - values[0]) > MIN_AMPLITUDE_CHANGE:
                sustained_count += 1
                if sustained_count >= SUSTAINED_THRESHOLD:  # Confirmar que la excitación es sostenida
                    stable_count = 0  # Reiniciar estabilidad cuando hay cambios bruscos
                    if not in_event:
                        start_time = timestamp
                        peak_value = tp10
                        in_event = True
                        print("Inicio de excitación detectado")
                    elif abs(tp10 - peak_value) > MIN_AMPLITUDE_CHANGE:
                        peak_value = tp10  # Actualizar el pico máximo dentro de la excitación
            else:
                sustained_count = 0  # Reiniciar contador de excitación sostenida
                if in_event:
                    stable_count += 1  # Contamos muestras estables consecutivas
                    if stable_count >= STABILITY_WINDOW and abs(tp10 - peak_value) < (MIN_AMPLITUDE_CHANGE / 2):  # Verificar caída
                        end_time = timestamp
                        duration = end_time - start_time
                        
                        # Buscar el valle más pronunciado después del final de la excitación
                        search_range = values[-SEARCH_WINDOW_END:]
                        if search_range:
                            valley_value = min(search_range)
                            valley_index = len(values) - SEARCH_WINDOW_END + search_range.index(valley_value)
                            
                            if valley_index > len(values) - SEARCH_WINDOW_START:
                                print(f"Valle detectado después de excitación en índice {valley_index}, valor: {valley_value}")
                                
                                if duration >= min_duration_threshold:  # Validar que la duración sea significativa
                                    if DURATION_LEFT_RANGE[0] <= duration <= DURATION_LEFT_RANGE[1]:
                                        client.publish(MQTT_TOPIC, "izquierda")
                                        print(f"Publicado en MQTT: 'izquierda' en {MQTT_TOPIC}")
                                    elif duration > DURATION_RIGHT_THRESHOLD:
                                        client.publish(MQTT_TOPIC, "derecha")
                                        print(f"Publicado en MQTT: 'derecha' en {MQTT_TOPIC}")
                        
                        in_event = False
                        stable_count = 0  # Reiniciar contador de estabilidad
        
        values.append(tp10)
        timestamps.append(timestamp)
        
        if len(values) > 1000:
            values.pop(0)  # Evitar acumulación de datos innecesaria
            timestamps.pop(0)
        
        time.sleep(0.01)  # Pequeña pausa para procesamiento en tiempo real

if __name__ == "__main__":
    detect_large_excitations()
