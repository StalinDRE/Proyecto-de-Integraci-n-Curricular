import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
new_file_path = 'usuarioSensor2.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Extraer la columna TP10
tp10_values = data['TP10']

# Definir el umbral para los picos
umbral_pico = 170

# Detectar todos los picos mayores al umbral
picos = data[data['TP10'] > umbral_pico]

# Mostrar los picos detectados en formato tabla
picos = picos.reset_index(drop=True)
picos['Index'] = picos.index + 1
print("Picos detectados (mayores a 150):")
print(picos[['Index', 'timestamps', 'TP10']])

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], tp10_values, label='TP10', color='gray')

# Añadir puntos y etiquetas numeradas
for i, row in picos.iterrows():
    plt.scatter(row['timestamps'], row['TP10'], color='orange', zorder=5)
    plt.text(row['timestamps'], row['TP10'], str(row['Index']), color='red', fontsize=10)



# Configuración de la gráfica
plt.title('Picos Detectados Mayores a 170 en TP10')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Mostrar tabla de resultados
import ace_tools as tools; tools.display_dataframe_to_user(name="Tabla de Picos Detectados", dataframe=picos[['Index', 'timestamps', 'TP10']])
