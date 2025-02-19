import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar el dataset
data = pd.read_csv('parpadeoDoblePrueba.csv')
#data = pd.read_csv('doblepapapdeo.csv')

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Extraer la columna TP10
tp10_values = data['TP10']

# Helper function to calculate time differences in seconds
def calculate_time_differences(min_or_max_list):
    timestamps = [entry[0] for entry in min_or_max_list]
    return np.diff([ts.timestamp() for ts in timestamps])

# Encontrar los mínimos locales por debajo de -150
minimos = []
for i in range(1, len(tp10_values) - 1):
    if tp10_values[i] < -150 and tp10_values[i] < tp10_values[i - 1] and tp10_values[i] < tp10_values[i + 1]:
        minimos.append((data['timestamps'][i], tp10_values[i]))

# Filtrar los mínimos dentro del rango de interés
valleys = [(timestamp, value) for timestamp, value in minimos if -150 <= value <= -350.832]
valley_time_diffs = calculate_time_differences(valleys)
double_valleys = [(valleys[i], valleys[i + 1]) for i in range(len(valley_time_diffs))
                  if 0.01 <= valley_time_diffs[i] <= 0.7]

# Encontrar los máximos locales por encima de 150
maximos = []
for i in range(1, len(tp10_values) - 1):
    if tp10_values[i] > 150 and tp10_values[i] > tp10_values[i - 1] and tp10_values[i] > tp10_values[i + 1]:
        maximos.append((data['timestamps'][i], tp10_values[i]))

# Filtrar los máximos dentro del rango de interés
peaks = [(timestamp, value) for timestamp, value in maximos if 150 <= value <= 305.246]
peak_time_diffs = calculate_time_differences(peaks)
double_peaks = [(peaks[i], peaks[i + 1]) for i in range(len(peak_time_diffs))
                if 0.01 <= peak_time_diffs[i] <= 0.7]

# Combinar valles y picos para identificar parpadeos dobles
double_blinks_combined = []
for valley1, valley2 in double_valleys:
    for peak1, peak2 in double_peaks:
        if (valley1[0] <= peak1[0] <= valley2[0]) or (peak1[0] <= valley1[0] <= peak2[0]):
            double_blinks_combined.append((valley1, valley2, peak1, peak2))

# Mostrar la gráfica
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], tp10_values, label='TP10', color='gray')

# Añadir líneas horizontales para los umbrales
plt.axhline(y=-150, color='blue', linestyle='--', label='Umbral Mínimo (Valles)')
plt.axhline(y=-350.832, color='cyan', linestyle='--', label='Umbral Máximo (Valles)')
plt.axhline(y=150, color='orange', linestyle='--', label='Umbral Mínimo (Picos)')
plt.axhline(y=305.246, color='red', linestyle='--', label='Umbral Máximo (Picos)')

# Resaltar los parpadeos dobles y los rangos de tiempo
for valley1, valley2 in double_valleys:
    plt.axvspan(valley1[0], valley1[0] + pd.Timedelta(seconds=0.6), color='blue', alpha=0.1, label='Rango de Tiempo (Valles)' if 'Rango de Tiempo (Valles)' not in plt.gca().get_legend_handles_labels()[1] else "")
for peak1, peak2 in double_peaks:
    plt.axvspan(peak1[0], peak1[0] + pd.Timedelta(seconds=0.6), color='orange', alpha=0.1, label='Rango de Tiempo (Picos)' if 'Rango de Tiempo (Picos)' not in plt.gca().get_legend_handles_labels()[1] else "")

# Resaltar los parpadeos dobles
for valley1, valley2, peak1, peak2 in double_blinks_combined:
    plt.plot([valley1[0], valley2[0]], [valley1[1], valley2[1]], 'go-', label='Parpadeo Doble (Valle-Pico)' if 'Parpadeo Doble (Valle-Pico)' not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.plot([peak1[0], peak2[0]], [peak1[1], peak2[1]], 'ro-', label='Parpadeo Doble (Valle-Pico)' if 'Parpadeo Doble (Valle-Pico)' not in plt.gca().get_legend_handles_labels()[1] else "")

# Títulos, etiquetas y leyenda
plt.title('Gráfica de TP10 con Parpadeos Dobles Identificados y Rangos de Tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Resultados
print(f"Parpadeos dobles identificados: {len(double_blinks_combined)}")
