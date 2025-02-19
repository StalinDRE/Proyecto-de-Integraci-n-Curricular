from pylsl import StreamInlet, resolve_byprop

# Definir rangos
low_range = (-264.648, -183.105)
high_range = (173.340, 205.078)

# Inicializar el estado del flujo
waiting_for_low = True

def detect_blink(value):
    """
    Detecta un parpadeo basado en el flujo de la se�al.
    """
    global waiting_for_low

    if waiting_for_low:
        # Detectar si el valor est� en el rango bajo
        if low_range[0] <= value <= low_range[1]:
            print(f"Detectado valor bajo: {value}")
            waiting_for_low = False  # Cambiar a esperar alto
    else:
        # Detectar si el valor est� en el rango alto
        if high_range[0] <= value <= high_range[1]:
            print(f"Detectado valor alto: {value}")
            print("Parpadeo detectado")
            waiting_for_low = True  # Reiniciar flujo

def main():
    print("Conectando al stream EEG...")
    streams = resolve_byprop('type', 'EEG', timeout=10)
    if not streams:
        print("No se encontr� ning�n stream EEG. Aseg�rate de que Muse est� transmitiendo.")
        return

    inlet = StreamInlet(streams[0])
    print("Conexi�n al stream EEG exitosa.")

    # Leer y analizar datos en tiempo real
    while True:
        sample, _ = inlet.pull_sample()
        tp10 = sample[3]  # Suponiendo que TP10 es el cuarto canal
        detect_blink(tp10)

if __name__ == "__main__":
    main()
