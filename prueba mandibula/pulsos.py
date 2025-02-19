import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def detect_large_excitations(file_path="pulsoMordida.csv", channel="TP10", threshold_factor=2):
    # Cargar el dataset
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            print("Error: El archivo está vacío o no se cargó correctamente.")
            return 0
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return 0
    
    # Evaluar excitaciones solo en el canal especificado
    if channel not in df.columns:
        print(f"Error: El canal {channel} no está en el dataset.")
        return 0
    
    variability = df[channel].diff().abs()
    
    # Umbral basado en el doble de la desviación estándar del canal
    threshold = threshold_factor * variability.std()
    
    # Identificar los puntos donde hay excitaciones
    excitation_points = variability > threshold
    
    # Identificar eventos completos de excitación (cuando hay una subida y luego baja)
    excitation_events = []
    in_event = False
    
    for i in range(1, len(excitation_points)):
        if excitation_points.iloc[i] and not in_event:
            in_event = True
            start_index = i
        elif not excitation_points.iloc[i] and in_event:
            in_event = False
            excitation_events.append((start_index, i))
    
    if not excitation_events:
        print("No se detectaron excitaciones en la señal.")
        return 0
    
    # Agrupar las excitaciones en grandes eventos
    excitation_timestamps = [start for start, end in excitation_events]
    if len(excitation_timestamps) < 2:
        print("Menos de 2 excitaciones detectadas, no se pueden agrupar correctamente.")
        return 1
    
    excitation_diffs = np.diff(excitation_timestamps)
    
    # Definir un umbral de separación para identificar grupos de excitaciones
    separation_threshold = excitation_diffs.mean() + 1.5 * excitation_diffs.std()
    
    # Identificar los puntos donde hay suficiente separación para considerar un nuevo grupo de excitaciones
    grouped_excitations = []
    current_group = [excitation_timestamps[0]]
    
    for i in range(1, len(excitation_timestamps)):
        if excitation_diffs[i-1] > separation_threshold:
            grouped_excitations.append(current_group)
            current_group = [excitation_timestamps[i]]
        else:
            current_group.append(excitation_timestamps[i])
    
    grouped_excitations.append(current_group)
    
    # Contar el número de grandes excitaciones
    num_large_excitations = len(grouped_excitations)
    
    # Graficar la señal con las grandes excitaciones marcadas
    plt.figure(figsize=(12, 6))
    plt.plot(df[channel],color="red" ,label=f"Señal {channel}", alpha=0.7)
    
    for group in grouped_excitations:
        if len(group) > 1:
            start, end = group[0], group[-1]
            plt.axvspan(start, end, color="yellow", alpha=0.3)
    
    plt.xlabel("Muestras")
    plt.ylabel(f"Amplitud de {channel}")
    plt.title(f"Detección de presión en la mandíbula {channel}")
    plt.legend()
    plt.show()
    
    print(f"Número de grandes excitaciones detectadas: {num_large_excitations}")
    return num_large_excitations

# Ejecutar detección en el dataset "Mordidad51.csv"
num_excitations = detect_large_excitations()