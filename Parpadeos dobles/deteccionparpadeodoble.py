import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar el dataset
data = pd.read_csv('doblepapapdeo.csv')


# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Extraer la columna TP10
tp10_values = data['TP10']

# Encontrar los mínimos locales por debajo de -270
minimos = []
for i in range(1, len(tp10_values) - 1):
    if tp10_values[i] < -270 and tp10_values[i] < tp10_values[i - 1] and tp10_values[i] < tp10_values[i + 1]:
        minimos.append((data['timestamps'][i], tp10_values[i]))

# Filtrar los mínimos para obtener solo los índices específicos
indices_especificos = [2, 4, 6, 9, 12, 14, 16, 18, 21, 22, 24, 26, 29, 33, 34, 35, 36, 39, 41]
minimos_filtrados = [minimos[i-1] for i in indices_especificos if i-1 < len(minimos)]

# Helper function to calculate time differences in seconds
def calculate_time_differences(min_or_max_list):
    timestamps = [entry[0] for entry in min_or_max_list]
    return np.diff([ts.timestamp() for ts in timestamps])

# Filter minima within the range of valleys
valleys = [(timestamp, value) for timestamp, value in minimos_filtrados if -343.75 <= value <= -277.832]
valley_time_diffs = calculate_time_differences(valleys)
double_valleys = [(valleys[i], valleys[i + 1]) for i in range(len(valley_time_diffs))
                  if 0.35 <= valley_time_diffs[i] <= 0.484]

# Define specific indices for high peaks
indices_puntos = [395, 924, 1022, 1743, 1837, 2370,
                  2464, 3087, 3168, 3745, 3834,
                  4462, 4590, 5166, 5239,
                  5781, 5888, 6353]

# Filter peaks within the range of maxima
peaks = [(data['timestamps'][index], data['TP10'][index]) for index in indices_puntos
         if 224.609 <= data['TP10'][index] <= 302.246]
peak_time_diffs = calculate_time_differences(peaks)
double_peaks = [(peaks[i], peaks[i + 1]) for i in range(len(peak_time_diffs))
                if 0.285 <= peak_time_diffs[i] <= 0.499]

# Combine valleys and peaks to identify double blinks
double_blinks_combined = []
for valley1, valley2 in double_valleys:
    for peak1, peak2 in double_peaks:
        # Check if the time intervals overlap between valleys and peaks
        if (valley1[0] <= peak1[0] <= valley2[0]) or (peak1[0] <= valley1[0] <= peak2[0]):
            double_blinks_combined.append((valley1, valley2, peak1, peak2))

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], tp10_values, label='TP10', color='gray')

# Highlight double blinks
for valley1, valley2, peak1, peak2 in double_blinks_combined:
    plt.plot([valley1[0], valley2[0]], [valley1[1], valley2[1]], 'go-', label='Parpadeo Doble (Valle-Pico)' if 'Parpadeo Doble (Valle-Pico)' not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.plot([peak1[0], peak2[0]], [peak1[1], peak2[1]], 'ro-', label='Parpadeo Doble (Valle-Pico)' if 'Parpadeo Doble (Valle-Pico)' not in plt.gca().get_legend_handles_labels()[1] else "")

# Add title, labels, and legend
plt.title('Gráfica de TP10 con Parpadeos Dobles Identificados')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()   
plt.show()

# Results
print(f"Parpadeos dobles identificados: {len(double_blinks_combined)}")
