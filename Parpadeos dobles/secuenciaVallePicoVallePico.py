import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
new_file_path = 'doblepapapdecopy.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Crear un DataFrame con los valles seleccionados
selected_valles = pd.DataFrame({
    'Index': [2, 4, 10, 15, 17, 19, 23, 28, 29, 31, 36, 39, 45, 46, 47, 48],
    'timestamps': [
        '2024-12-30 01:49:32.634000063',
        '2024-12-30 01:49:33.062999964',
        '2024-12-30 01:49:35.898999929',
        '2024-12-30 01:49:36.266000032',
        '2024-12-30 01:49:38.348000050',
        '2024-12-30 01:49:38.730999947',
        '2024-12-30 01:49:41.112999916',
        '2024-12-30 01:49:41.464999914',
        '2024-12-30 01:49:43.648000002',
        '2024-12-30 01:49:44.030999899',
        '2024-12-30 01:49:46.467999935',
        '2024-12-30 01:49:46.933000088',
        '2024-12-30 01:49:49.167000055',
        '2024-12-30 01:49:49.569000006',
        '2024-12-30 01:49:51.569000006',
        '2024-12-30 01:49:52.052999973'
    ],
    'TP10': [
        -289.551, -331.055, -315.430, -324.707, -338.379, -313.965, -343.750, -277.832, -293.457, 
        -296.875, -296.387, -322.266, -291.016, -285.645, -291.504, -330.078
    ]
})

# Crear un DataFrame con los picos seleccionados
selected_picos = pd.DataFrame({
    'Index': [8, 18, 27, 40, 43, 48, 55, 63, 74, 80, 91, 101, 111, 119, 124, 134],
    'timestamps': [
        '2024-12-30 01:49:32.841000080',
        '2024-12-30 01:49:33.223999977',
        '2024-12-30 01:49:36.039999962',
        '2024-12-30 01:49:36.407000065',
        '2024-12-30 01:49:38.489000082',
        '2024-12-30 01:49:38.855999947',
        '2024-12-30 01:49:41.289000034',
        '2024-12-30 01:49:41.605000019',
        '2024-12-30 01:49:43.858999968',
        '2024-12-30 01:49:44.207000017',
        '2024-12-30 01:49:46.660000086',
        '2024-12-30 01:49:47.158999920',
        '2024-12-30 01:49:49.408999920',
        '2024-12-30 01:49:49.694000006',
        '2024-12-30 01:49:51.811000109',
        '2024-12-30 01:49:52.229000092'
    ],
    'TP10': [
        300.293, 291.016, 270.508, 245.605, 243.652, 231.445, 282.227, 251.465, 260.254, 
        249.023, 272.461, 298.34, 302.246, 224.609, 294.434, 262.207
    ]
})

# Convertir timestamps a formato datetime
selected_valles['timestamps'] = pd.to_datetime(selected_valles['timestamps'])
selected_picos['timestamps'] = pd.to_datetime(selected_picos['timestamps'])

# Buscar secuencias de valle -> pico -> valle -> pico
double_blinks_combined = []
for i in range(len(selected_valles) - 1):
    valley1 = selected_valles.iloc[i]
    valley2_candidates = selected_valles[selected_valles['timestamps'] > valley1['timestamps']]
    
    if valley2_candidates.empty:
        continue
    
    valley2 = valley2_candidates.iloc[0]

    # Buscar el pico entre valley1 y valley2
    peak1_candidates = selected_picos[(selected_picos['timestamps'] > valley1['timestamps']) & (selected_picos['timestamps'] < valley2['timestamps'])]
    if peak1_candidates.empty:
        continue
    peak1 = peak1_candidates.iloc[0]

    # Buscar el siguiente pico después de valley2
    peak2_candidates = selected_picos[selected_picos['timestamps'] > valley2['timestamps']]
    if peak2_candidates.empty:
        continue
    peak2 = peak2_candidates.iloc[0]

    # Verificar distancias temporales
    time_diff_valleys = (valley2['timestamps'] - valley1['timestamps']).total_seconds()
    time_diff_peaks = (peak2['timestamps'] - peak1['timestamps']).total_seconds()
    
    if 0.01 <= time_diff_valleys <= 0.7 and 0.01 <= time_diff_peaks <= 0.7:
        double_blinks_combined.append({
            'Valley 1 Index': valley1['Index'],
            'Valley 1 Timestamp': valley1['timestamps'],
            'Peak 1 Index': peak1['Index'],
            'Peak 1 Timestamp': peak1['timestamps'],
            'Valley 2 Index': valley2['Index'],
            'Valley 2 Timestamp': valley2['timestamps'],
            'Peak 2 Index': peak2['Index'],
            'Peak 2 Timestamp': peak2['timestamps'],
            'Time Difference Valleys (s)': time_diff_valleys,
            'Time Difference Peaks (s)': time_diff_peaks
        })

# Convertir las secuencias a un DataFrame
double_blinks_df = pd.DataFrame(double_blinks_combined)

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], data['TP10'], label='TP10', color='darkseagreen')

# Añadir líneas y puntos para las secuencias detectadas
for blink in double_blinks_combined:
    plt.plot(
        [blink['Valley 1 Timestamp'], blink['Peak 1 Timestamp'], blink['Valley 2 Timestamp'], blink['Peak 2 Timestamp']],
        [selected_valles[selected_valles['Index'] == blink['Valley 1 Index']]['TP10'].values[0],
         selected_picos[selected_picos['Index'] == blink['Peak 1 Index']]['TP10'].values[0],
         selected_valles[selected_valles['Index'] == blink['Valley 2 Index']]['TP10'].values[0],
         selected_picos[selected_picos['Index'] == blink['Peak 2 Index']]['TP10'].values[0]],
        marker='o', linestyle='-', color='blue', label='Double Blink' if 'Double Blink' not in plt.gca().get_legend_handles_labels()[1] else ""
    )

# Configuración de la gráfica
plt.title('Secuencias Valle -> Pico -> Valle -> Pico Detectadas')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()

# Exportar los resultados a un archivo CSV
output_double_blinks_file_path = 'double_blinks_sequences.csv'
double_blinks_df.to_csv(output_double_blinks_file_path, index=False)

# Mostrar ubicación del archivo exportado
print(f"Archivo exportado: {output_double_blinks_file_path}")
