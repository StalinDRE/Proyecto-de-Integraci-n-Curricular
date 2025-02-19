from pylsl import StreamInlet, resolve_byprop
import paho.mqtt.client as mqtt
import time

# Configuraci�n del broker MQTT
MQTT_BROKER = "localhost"  # Cambia esto a la IP de tu servidor Mosquitto si est� en otra m�quina
MQTT_PORT = 1883
MQTT_TOPIC = "dron/senales"

# Inicializar cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Definir rangos para detecci�n
low_range = (-307.648, -95.105)  # Valles
high_range = (95.340, 260.078)   # Picos

# Inicializar variables
waiting_for_low = True
single_blink_detected = []
double_blink_detected = []

# Tiempo m�ximo entre parpadeos para ser considerado doble (ajustable)
DOUBLE_BLINK_TIME_THRESHOLD = 0.7

def detect_blink(value, timestamp):
    """
    Detecta parpadeos simples y dobles y publica en MQTT.
    """
    global waiting_for_low, single_blink_detected, double_blink_detected
    
    if waiting_for_low:
        if low_range[0] <= value <= low_range[1]:  # Detectar valle (m�nimo)
            print(f"Detectado valle: {value} en {timestamp}")
            waiting_for_low = False
            single_blink_detected.append((timestamp, value))
    else:
        if high_range[0] <= value <= high_range[1]:  # Detectar pico (m�ximo)
            print(f"Detectado pico: {value} en {timestamp}")
            waiting_for_low = True
            
            # Verificar si hay un parpadeo simple completo
            if single_blink_detected:
                low_time, low_val = single_blink_detected[-1]
                time_diff = timestamp - low_time
                
                if time_diff <= 0.5:
                    print("Parpadeo simple detectado")
                    publish_mqtt("abajo")  # Publicar "abajo" en MQTT
                    
                    # Si hay otro parpadeo en la lista reciente, revisar si es un doble
                    if len(single_blink_detected) > 1:
                        prev_low_time, _ = single_blink_detected[-2]
                        prev_time_diff = low_time - prev_low_time
                        
                        if prev_time_diff <= DOUBLE_BLINK_TIME_THRESHOLD:
                            print("Parpadeo doble detectado")
                            publish_mqtt("arriba")  # Publicar "arriba" en MQTT
                            double_blink_detected.append((prev_low_time, low_time, timestamp))
                            single_blink_detected = []  # Limpiar lista tras parpadeo doble

                # Si no es doble, dejar en la lista como simple
                else:
                    single_blink_detected.append((timestamp, value))

def publish_mqtt(message):
    """
    Publica en MQTT el mensaje recibido.
    """
    client.publish(MQTT_TOPIC, message)
    print(f"?? Enviado a MQTT: {message}")

def main():
    print("Conectando al stream EEG...")
    streams = resolve_byprop('type', 'EEG', timeout=10)
    
    if not streams:
        print("No se encontr� ning�n stream EEG. Aseg�rate de que Muse est� transmitiendo.")
        return

    inlet = StreamInlet(streams[0])
    print("Conexi�n al stream EEG exitosa.")

    while True:
        sample, timestamp = inlet.pull_sample()
        tp10 = sample[3]  # Suponiendo que TP10 es el cuarto canal
        detect_blink(tp10, timestamp)
        time.sleep(0.01)  # Peque�a pausa para procesar datos en tiempo real

if __name__ == "__main__":
    main()
