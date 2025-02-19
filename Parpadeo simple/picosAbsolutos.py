import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
new_file_path = 'usuarioSensor.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Crear un DataFrame con los picos seleccionados
selected_picos = pd.DataFrame({
    'Index': [3, 6, 7, 11, 13, 18, 22, 30, 33],
    'timestamps': [
        '2024-12-15 21:03:19.308000088',
        '2024-12-15 21:03:21.908999920',
        '2024-12-15 21:03:24.622999907',
        '2024-12-15 21:03:27.423000097',
        '2024-12-15 21:03:30.187999964',
        '2024-12-15 21:03:32.539000034',
        '2024-12-15 21:03:34.753999949',
        '2024-12-15 21:03:37.069999933',
        '2024-12-15 21:03:39.035000086'
    ],
    'TP10': [178.711, 180.664, 173.340, 185.059, 187.500, 192.871, 192.871, 205.078, 181.641]
})

# Convertir timestamps a formato datetime
selected_picos['timestamps'] = pd.to_datetime(selected_picos['timestamps'])

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], data['TP10'], label='TP10', color='gray')

# Añadir puntos y etiquetas numeradas
for i, row in selected_picos.iterrows():
    plt.scatter(row['timestamps'], row['TP10'], color='orange', zorder=5)
    plt.text(row['timestamps'], row['TP10'], str(row['Index']), color='red', fontsize=10)

# Añadir líneas horizontales para los umbrales
plt.axhline(y=150, color='green', linestyle='--', label='Umbral mínimo (Picos)')
plt.axhline(y=220, color='purple', linestyle='--', label='Umbral máximo (Picos)')

# Configuración de la gráfica
plt.title('Picos Absolutos')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Exportar la tabla de los picos seleccionados a un archivo CSV
output_path = "Picos_Seleccionados.csv"
selected_picos.to_csv(output_path, index=False)

# Mostrar la tabla de los picos seleccionados
import ace_tools as tools; tools.display_dataframe_to_user(name="Picos Seleccionados", dataframe=selected_picos)

output_path
