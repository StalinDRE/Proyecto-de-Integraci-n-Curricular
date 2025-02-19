import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
new_file_path = 'doblepapapdecopy.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Extraer la columna TP10
tp10_values = data['TP10']

# Definir el umbral para los picos
umbral_pico = 210

# Detectar todos los picos mayores al umbral
picos = data[data['TP10'] > umbral_pico]

# Ajustar el índice y agregar una columna de índice personalizado
picos = picos.reset_index(drop=True)
picos['Index'] = picos.index + 1

# Exportar los picos detectados a un archivo CSV
output_file_path = 'picos_detectados_doble_parpadeo.csv'
picos[['Index', 'timestamps', 'TP10']].to_csv(output_file_path, index=False)

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps'], tp10_values, label='TP10', color='darkseagreen')

# Añadir puntos y etiquetas numeradas
for i, row in picos.iterrows():
    plt.scatter(row['timestamps'], row['TP10'], color='orange', zorder=5)
    plt.text(row['timestamps'], row['TP10'], str(row['Index']), color='red', fontsize=10)

# Configuración de la gráfica
plt.title('Picos Detectados Mayores a 230 en TP10')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
plt.grid()
plt.xticks(rotation=45)
#plt.legend()
plt.tight_layout()
plt.show()
