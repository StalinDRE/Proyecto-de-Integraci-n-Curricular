import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
new_file_path = 'doblepapapdecopy.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Extraer la columna TP10
tp10_values = data['TP10']

# Definir el umbral para los valles
umbral_valle = -270

# Detectar todos los valles menores al umbral
valles = data[data['TP10'] < umbral_valle]

# Mostrar los valles detectados en formato tabla
valles = valles.reset_index(drop=True)
valles['Index'] = valles.index + 1
print("Valles detectados (menores a -280):")
print(valles[['Index', 'timestamps', 'TP10']])

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], tp10_values, label='TP10', color='darkseagreen')

# Añadir puntos y etiquetas numeradas
for i, row in valles.iterrows():
    plt.scatter(row['timestamps'], row['TP10'], color='teal', zorder=5)
    plt.text(row['timestamps'], row['TP10'], str(row['Index']), color='blue', fontsize=10)

# Línea de umbral
# plt.axhline(y=umbral_valle, color='red', linestyle='--', label='Umbral -150')

# Configuración de la gráfica
plt.title('Valles Detectados Menores a -280 en TP10')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Mostrar tabla de resultados
import ace_tools as tools; tools.display_dataframe_to_user(name="Tabla de Valles Detectados", dataframe=valles[['Index', 'timestamps', 'TP10']])
