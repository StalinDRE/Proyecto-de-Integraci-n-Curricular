import pandas as pd
import matplotlib.pyplot as plt
import itertools

# Definir rangos para detectar un parpadeo
low_range = (-317.657, -146.484)  # Intervalo para valles
high_range = (150.340, 220.078)   # Intervalo para picos

# Cargar el dataset
new_file_path = 'usuarioSensor.csv'  # Cambia el nombre del archivo si es necesario
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Extraer la columna TP10
tp10_values = data['TP10']

# Estado inicial del flujo
waiting_for_low = True
single_blink_detected = []

# Detectar un parpadeo basado en la secuencia valle → pico
low_point = None
for timestamp, value in zip(data['timestamps'], tp10_values):
    if waiting_for_low:
        # Detectar si el valor está en el rango bajo
        if low_range[0] <= value <= low_range[1]:
            low_point = (timestamp, value)
            waiting_for_low = False  # Cambiar a esperar pico
    else:
        # Detectar si el valor está en el rango alto
        if high_range[0] <= value <= high_range[1]:
            # Parpadeo detectado
            single_blink_detected.append((low_point, (timestamp, value)))
            waiting_for_low = True  # Reiniciar flujo

# Mostrar valles y picos detectados
print("Valles y picos detectados:")
for i, ((low_time, low_val), (high_time, high_val)) in enumerate(single_blink_detected, start=1):
    print(f"Detección {i}: Valle en {low_time} ({low_val}), Pico en {high_time} ({high_val})")

# Calcular distancias en X (tiempo) entre puntos detectados
x_distances = [
    (high[0] - low[0]).total_seconds() for low, high in single_blink_detected
]

# Crear un DataFrame con las distancias
distances_data = [{
    "Valle_Timestamp": low[0],
    "Valle_Value": low[1],
    "Pico_Timestamp": high[0],
    "Pico_Value": high[1],
    "Distancia_Tiempo": (high[0] - low[0]).total_seconds()
} for low, high in single_blink_detected]

distances_df = pd.DataFrame(distances_data)

# Exportar las distancias a un archivo CSV
output_csv_path = 'distancias_pico_valle.csv'
distances_df.to_csv(output_csv_path, index=False)
print(f"Archivo CSV generado: {output_csv_path}")

# Mostrar las distancias calculadas
print("\nDistancias en X entre valles y picos:")
for i, x_distance in enumerate(x_distances, start=1):
    print(f"Distancia {i}: {x_distance} segundos")

# Visualizar la gráfica actualizada con todos los valles y picos detectados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], tp10_values, label='TP10', color='gray')

# Añadir líneas horizontales para los umbrales
plt.axhline(y=low_range[0], color='blue', linestyle='--', label='Umbral Mínimo (Valle)')
plt.axhline(y=low_range[1], color='cyan', linestyle='--', label='Umbral Máximo (Valle)')
plt.axhline(y=high_range[0], color='orange', linestyle='--', label='Umbral Mínimo (Pico)')
plt.axhline(y=high_range[1], color='red', linestyle='--', label='Umbral Máximo (Pico)')

# Colores únicos para diferenciar los puntos
colors = itertools.cycle(['green', 'blue', 'purple', 'orange', 'pink', 'yellow'])

for i, ((low_time, low_val), (high_time, high_val)) in enumerate(single_blink_detected):
    color = next(colors)
    plt.scatter(low_time, low_val, color=color, label=f'Valle {i+1}', zorder=5)
    plt.scatter(high_time, high_val, color=color, label=f'Pico {i+1}', zorder=5)
    plt.plot([low_time, high_time], [low_val, high_val], color=color, linestyle='--', zorder=4)

# Añadir títulos y leyenda
plt.title('Gráfica de TP10 con Valles y Picos Detectados')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
#plt.legend()
plt.show()
