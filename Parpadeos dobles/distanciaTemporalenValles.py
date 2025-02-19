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

# Convertir timestamps a formato datetime
selected_valles['timestamps'] = pd.to_datetime(selected_valles['timestamps'])

# Crear pares consecutivos de valles (1-2, 3-4, etc.) y calcular sus distancias
pares_valles = []

for i in range(0, len(selected_valles), 2):
    if i + 1 < len(selected_valles):
        valley1 = selected_valles.iloc[i]
        valley2 = selected_valles.iloc[i + 1]
        dif_tiempo = (valley2['timestamps'] - valley1['timestamps']).total_seconds()
        pares_valles.append({
            'Valley 1 Index': valley1['Index'],
            'Valley 1 Timestamp': valley1['timestamps'],
            'Valley 1 TP10': valley1['TP10'],
            'Valley 2 Index': valley2['Index'],
            'Valley 2 Timestamp': valley2['timestamps'],
            'Valley 2 TP10': valley2['TP10'],
            'Time Difference (s)': dif_tiempo
        })

# Convertir los pares a un DataFrame
paired_valles_df = pd.DataFrame(pares_valles)

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], data['TP10'], label='TP10', color='darkseagreen')

# Añadir líneas entre pares de valles y etiquetas numeradas
for i, row in paired_valles_df.iterrows():
    plt.plot(
        [row['Valley 1 Timestamp'], row['Valley 2 Timestamp']],
        [row['Valley 1 TP10'], row['Valley 2 TP10']],
        color='blue', linestyle='--', linewidth=1, label='Par de Valles' if i == 0 else ""
    )
    plt.scatter(row['Valley 1 Timestamp'], row['Valley 1 TP10'], color='teal', zorder=5)
    plt.scatter(row['Valley 2 Timestamp'], row['Valley 2 TP10'], color='teal', zorder=5)
    plt.text(row['Valley 1 Timestamp'], row['Valley 1 TP10'], str(row['Valley 1 Index']), color='blue', fontsize=10)
    plt.text(row['Valley 2 Timestamp'], row['Valley 2 TP10'], str(row['Valley 2 Index']), color='blue', fontsize=10)

# Configuración de la gráfica
plt.title('Pares de Valles con Distancias Temporales')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()

# Exportar los resultados a un archivo CSV
output_paired_file_path = 'Distancia_temporal_valles_absolutos.csv'
paired_valles_df.to_csv(output_paired_file_path, index=False)

# Mostrar ubicación del archivo exportado
print(f"Archivo exportado: {output_paired_file_path}")
