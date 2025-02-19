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

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], data['TP10'], label='TP10', color='darkseagreen')

# Añadir puntos y etiquetas numeradas
for i, row in selected_valles.iterrows():
   plt.scatter(row['timestamps'], row['TP10'], color='teal', zorder=5)
   plt.text(row['timestamps'], row['TP10'], str(row['Index']), color='blue', fontsize=10)
    
plt.axhline(y=-146.484, color='blue', linestyle='--', label='Umbral maximo (Valles)')
plt.axhline(y=-390.750, color='cyan', linestyle='--', label='Umbral minimo (Valles)')

# Configuración de la gráfica
plt.title('Valles Absolutos')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Exportar la tabla de los valores seleccionados a un CSV
# output_file_path = 'valles_seleccionados_dobles.csv'
# selected_valles.to_csv(output_file_path, index=False)
