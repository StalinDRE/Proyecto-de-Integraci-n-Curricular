import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
new_file_path = 'doblepapapdecopy.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

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
selected_picos['timestamps'] = pd.to_datetime(selected_picos['timestamps'])

# Crear pares consecutivos de picos (1-2, 3-4, etc.) y calcular sus distancias
pares_picos = []

for i in range(0, len(selected_picos), 2):
    if i + 1 < len(selected_picos):
        peak1 = selected_picos.iloc[i]
        peak2 = selected_picos.iloc[i + 1]
        time_diff = (peak2['timestamps'] - peak1['timestamps']).total_seconds()
        pares_picos.append({
            'Peak 1 Index': peak1['Index'],
            'Peak 1 Timestamp': peak1['timestamps'],
            'Peak 1 TP10': peak1['TP10'],
            'Peak 2 Index': peak2['Index'],
            'Peak 2 Timestamp': peak2['timestamps'],
            'Peak 2 TP10': peak2['TP10'],
            'Time Difference (s)': time_diff
        })

# Convertir los pares a un DataFrame
paired_picos_df = pd.DataFrame(pares_picos)

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], data['TP10'], label='TP10', color='darkseagreen')

# Añadir líneas entre pares de picos y etiquetas numeradas
for i, row in paired_picos_df.iterrows():
    plt.plot(
        [row['Peak 1 Timestamp'], row['Peak 2 Timestamp']],
        [row['Peak 1 TP10'], row['Peak 2 TP10']],
        color='orange', linestyle='--', linewidth=1, label='Par de Picos' if i == 0 else ""
    )
    plt.scatter(row['Peak 1 Timestamp'], row['Peak 1 TP10'], color='red', zorder=5)
    plt.scatter(row['Peak 2 Timestamp'], row['Peak 2 TP10'], color='red', zorder=5)
    plt.text(row['Peak 1 Timestamp'], row['Peak 1 TP10'], str(row['Peak 1 Index']), color='red', fontsize=10)
    plt.text(row['Peak 2 Timestamp'], row['Peak 2 TP10'], str(row['Peak 2 Index']), color='red', fontsize=10)

# Configuración de la gráfica
plt.title('Pares de Picos con Distancias Temporales')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()

# Exportar los resultados a un archivo CSV
output_paired_picos_file_path = 'Distancia_temporal_picos_absolutos.csv'
paired_picos_df.to_csv(output_paired_picos_file_path, index=False)

# Mostrar ubicación del archivo exportado
print(f"Archivo exportado: {output_paired_picos_file_path}")
