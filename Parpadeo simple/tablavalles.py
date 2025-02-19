import pandas as pd

# Crear un ejemplo del DataFrame de valles para exportación
# Este debe ser reemplazado con los datos del script original si estuvieran cargados
new_file_path = 'usuarioSensor.csv'
data = pd.read_csv(new_file_path)

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Definir el umbral para los valles
umbral_valle = -180

# Detectar todos los valles menores al umbral
valles = data[data['TP10'] < umbral_valle]

# Resetear índice para mejor legibilidad
valles = valles.reset_index(drop=True)
valles['Index'] = valles.index + 1

# Exportar la tabla a CSV
output_path = "Valles_Detectados.csv"
valles[['Index', 'timestamps', 'TP10']].to_csv(output_path, index=False)

output_path
