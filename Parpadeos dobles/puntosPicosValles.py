import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
data = pd.read_csv('doblepapapdeo.csv')

low_range = (-317.657, -146.484)  # Intervalo para valles
high_range = (150.340, 220.078)   # Intervalo para picos

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Extraer la columna TP10
tp10_values = data['TP10']

# Encontrar los mínimos locales por debajo de -270
minimos = []
for i in range(1, len(tp10_values) - 1):
    if tp10_values[i] < -270 and tp10_values[i] < tp10_values[i - 1] and tp10_values[i] < tp10_values[i + 1]:
        minimos.append((data['timestamps'][i], tp10_values[i]))

# Filtrar los mínimos para obtener solo los índices específicos
indices_especificos = [2, 4, 6, 9, 12, 14, 16, 18, 21, 22, 24, 26, 29, 33, 34, 35, 36, 39, 41]
minimos_filtrados = [minimos[i-1] for i in indices_especificos if i-1 < len(minimos)]

# Determinar el mínimo y máximo de los valles encontrados
if minimos_filtrados:
    min_valley = min(minimos_filtrados, key=lambda x: x[1])  # Mínimo más bajo
    max_valley = max(minimos_filtrados, key=lambda x: x[1])  # Máximo más alto

# Filtrar los picos que son mayores a 220
picos_altos = data[data['TP10'] > 220]

# Configurar el gráfico
plt.figure(figsize=(12, 6))

# Graficar TP10
plt.plot(data['timestamps'], tp10_values, label='TP10', color='gray')

# Añadir puntos en los mínimos encontrados y enumerarlos
for timestamp, value in minimos_filtrados:
    plt.plot(timestamp, value, 'bo')  # Marca un punto azul para los mínimos filtrados
    plt.text(timestamp, value - 10, f'{value:.2f}', fontsize=9, ha='center', color='blue')
    print(f"Mínimo: ({timestamp}, {value})")

# Índices que deben mostrarse como puntos para picos altos
indices_puntos = [395, 924, 1022, 1743, 1837, 2370,
                  2464, 3087, 3168, 3745, 3834,
                  4462, 4590, 5166, 5239,
                  5781, 5888, 6353]

# Marcar los puntos específicos de picos altos
for index in indices_puntos:
    if index < len(data): # Verificar que el índice esté dentro del rango del DataFrame
        plt.plot(data['timestamps'][index], data['TP10'][index], 'ro') # Marca un punto rojo
        plt.text(data['timestamps'][index], data['TP10'][index] + 10, f'{data["TP10"][index]:.2f}', fontsize=9, ha='center', color='red')
        print(f"Pico: ({data['timestamps'][index]}, {data['TP10'][index]})")

# Añadir líneas horizontales en el mínimo y máximo de los valles
if minimos_filtrados:
    plt.axhline(y=min_valley[1]-10, color='green', linestyle='--', label='Mínimo Valle')
    plt.axhline(y=max_valley[1]+10, color='orange', linestyle='--', label='Máximo Valle')

# Calcular el mínimo y máximo de los picos altos para las líneas horizontales
valores_puntos = [data['TP10'][index] for index in indices_puntos if index < len(data)]
if valores_puntos:
    min_pico = min(valores_puntos)
    max_pico = max(valores_puntos)
    plt.axhline(y=min_pico-10, color='purple', linestyle='--', label='Mínimo Pico')
    plt.axhline(y=max_pico+10, color='blue', linestyle='--', label='Máximo Pico')
    
    plt.axhline(y=low_range[0], color='blue', linestyle='--', label='Umbral Mínimo (Valle)')
    plt.axhline(y=low_range[1], color='cyan', linestyle='--', label='Umbral Máximo (Valle)')
    plt.axhline(y=high_range[0], color='orange', linestyle='--', label='Umbral Mínimo (Pico)')
    plt.axhline(y=high_range[1], color='red', linestyle='--', label='Umbral Máximo (Pico)')

# Añadir título y etiquetas
plt.title('Gráfica de TP10 con Mínimos y Picos Altos')
plt.xlabel('Tiempo')
plt.ylabel('Valor de TP10')
#plt.legend()
plt.grid()

# Mostrar el gráfico
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
