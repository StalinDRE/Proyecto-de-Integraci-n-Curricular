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

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], data['TP10'], label='TP10', color='darkseagreen')

# Añadir puntos y etiquetas numeradas
for i, row in selected_picos.iterrows():
    plt.scatter(row['timestamps'], row['TP10'], color='orange', zorder=5)
    plt.text(row['timestamps'], row['TP10'], str(row['Index']), color='red', fontsize=10)

# Añadir líneas horizontales para los umbrales
plt.axhline(y=150, color='green', linestyle='--', label='Umbral mínimo (Picos)')
plt.axhline(y=320, color='purple', linestyle='--', label='Umbral máximo (Picos)')

# Configuración de la gráfica
plt.title('Picos Absolutos')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Exportar la tabla de los picos seleccionados a un archivo CSV
output_path = "picos_absolutos_detectados_doble_parpadeo.csv"
selected_picos.to_csv(output_path, index=False)

# # Mostrar la tabla de los picos seleccionados
# import ace_tools as tools; tools.display_dataframe_to_user(name="Picos Seleccionados", dataframe=selected_picos)

# output_path
