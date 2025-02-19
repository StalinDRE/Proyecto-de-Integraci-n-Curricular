import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar el dataset

#data = pd.read_csv('parpadeoDoblePrueba.csv')
#data = pd.read_csv('Juani.csv')
data = pd.read_csv('doblepapapdeo.csv')

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

# Encontrar los máximos locales por encima de 150
maximos = []
for i in range(1, len(tp10_values) - 1):
    if tp10_values[i] > 150 and tp10_values[i] > tp10_values[i - 1] and tp10_values[i] > tp10_values[i + 1]:
        maximos.append((data['timestamps'][i], tp10_values[i]))

# Verificar secuencia valle -> pico -> valle -> pico
double_blinks_combined = []
for i in range(len(minimos) - 1):
    valley1 = minimos[i]
    valley2_candidates = [val for val in minimos if val[0] > valley1[0]]
    if not valley2_candidates:
        continue
    valley2 = valley2_candidates[0]

    # Buscar el pico entre valley1 y valley2
    peak1_candidates = [peak for peak in maximos if valley1[0] < peak[0] < valley2[0]]
    if not peak1_candidates:
        continue
    peak1 = peak1_candidates[0]

    # Buscar el siguiente pico después de valley2
    peak2_candidates = [peak for peak in maximos if peak[0] > valley2[0]]
    if not peak2_candidates:
        continue
    peak2 = peak2_candidates[0]

    # Verificar las distancias temporales
    time_diff_valleys = (valley2[0] - valley1[0]).total_seconds()
    time_diff_peaks = (peak2[0] - peak1[0]).total_seconds()
    if 0.01 <= time_diff_valleys <= 0.7 and 0.01 <= time_diff_peaks <= 0.7:
        double_blinks_combined.append((valley1, peak1, valley2, peak2))

# Mostrar la gráfica
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], tp10_values, label='TP10', color='gray')

# Añadir líneas horizontales para los umbrales
plt.axhline(y=-150, color='blue', linestyle='--', label='Umbral Mínimo (Valles)')
plt.axhline(y=-350.832, color='cyan', linestyle='--', label='Umbral Máximo (Valles)')
plt.axhline(y=150, color='orange', linestyle='--', label='Umbral Mínimo (Picos)')
plt.axhline(y=305.246, color='red', linestyle='--', label='Umbral Máximo (Picos)')

# Resaltar los parpadeos dobles
for valley1, peak1, valley2, peak2 in double_blinks_combined:
    plt.plot([valley1[0], peak1[0]], [valley1[1], peak1[1]], 'go-', label='Parpadeo Doble (Valle-Pico)' if 'Parpadeo Doble (Valle-Pico)' not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.plot([valley2[0], peak2[0]], [valley2[1], peak2[1]], 'ro-', label='Parpadeo Doble (Valle-Pico)' if 'Parpadeo Doble (Valle-Pico)' not in plt.gca().get_legend_handles_labels()[1] else "")

# Títulos, etiquetas y leyenda
plt.title('Gráfica de TP10 con Parpadeos Dobles Identificados en Secuencia')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Resultados
print(f"Parpadeos dobles identificados: {len(double_blinks_combined)}")
