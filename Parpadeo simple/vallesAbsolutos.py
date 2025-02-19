import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
new_file_path = 'usuarioSensor.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Crear un DataFrame con los valles seleccionados
selected_valles = pd.DataFrame({
    'Index': [2, 7, 9, 12, 18, 21, 26, 31, 35],
    'timestamps': [
        '2024-12-15 21:03:19.167000055',
        '2024-12-15 21:03:21.783999920',
        '2024-12-15 21:03:24.532999992',
        '2024-12-15 21:03:27.263000010',
        '2024-12-15 21:03:30.032000065',
        '2024-12-15 21:03:32.378999949',
        '2024-12-15 21:03:34.644999981',
        '2024-12-15 21:03:36.910000086',
        '2024-12-15 21:03:38.910000086'
    ],
    'TP10': [-215.332, -246.582, -183.105, -231.934, -219.238, -249.512, -224.609, -264.648, -198.730]
})

# Convertir timestamps a formato datetime
selected_valles['timestamps'] = pd.to_datetime(selected_valles['timestamps'])

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], data['TP10'], label='TP10', color='gray')

# Añadir puntos y etiquetas numeradas
for i, row in selected_valles.iterrows():
    plt.scatter(row['timestamps'], row['TP10'], color='orange', zorder=5)
    plt.text(row['timestamps'], row['TP10'], str(row['Index']), color='red', fontsize=10)
    
plt.axhline(y=-146.484, color='blue', linestyle='--', label='Umbral maximo (Valles)')
plt.axhline(y=-317.57, color='cyan', linestyle='--', label='Umbral minimo (Valles)')

# Configuración de la gráfica
plt.title('Valles Absolutos')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Mostrar la tabla de los valores seleccionados
import ace_tools as tools; tools.display_dataframe_to_user(name="Valles Seleccionados", dataframe=selected_valles)
