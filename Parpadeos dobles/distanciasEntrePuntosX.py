import pandas as pd

# Cargar el dataset
data = pd.read_csv('doblepapapdeo.csv')

# Convertir la columna 'timestamps' a un formato legible
data['timestamps'] = pd.to_datetime(data['timestamps'], unit='s')

# Para los mínimos
pares_minimos = [(4, 6), (9, 12), (14, 16), (18, 21), (22, 24),
                 (26, 29), (33, 34), (35, 36), (39, 41)]

minimos = []
tp10_values = data['TP10']
for i in range(1, len(tp10_values) - 1):
    if tp10_values[i] < -270 and tp10_values[i] < tp10_values[i - 1] and tp10_values[i] < tp10_values[i + 1]:
        minimos.append((data['timestamps'][i], tp10_values[i]))

# Calcular diferencias para los mínimos
diferencias_minimos = {}
for i1, i2 in pares_minimos:
    if i1 - 1 < len(minimos) and i2 - 1 < len(minimos):
        x1 = minimos[i1 - 1][0]
        x2 = minimos[i2 - 1][0]
        diferencias_minimos[f'Diferencia entre mínimo {i1} y mínimo {i2}'] = (x2 - x1).total_seconds()

# Para los máximos
pares_maximos = [(924, 1022), (1743, 1837), (2370, 2464), (3087, 3168),
                 (3745, 3834), (4462, 4590), (5166, 5239), (5781, 5888)]

diferencias_maximos = {}
for i1, i2 in pares_maximos:
    if i1 < len(data) and i2 < len(data):
        x1 = data['timestamps'][i1]
        x2 = data['timestamps'][i2]
        diferencias_maximos[f'Diferencia entre máximo {i1} y máximo {i2}'] = (x2 - x1).total_seconds()

# Calcular el intervalo para los mínimos y los máximos
if diferencias_minimos:
    intervalo_minimos = (min(diferencias_minimos.values()), max(diferencias_minimos.values()))
else:
    intervalo_minimos = None

if diferencias_maximos:
    intervalo_maximos = (min(diferencias_maximos.values()), max(diferencias_maximos.values()))
else:
    intervalo_maximos = None

# Imprimir los resultados
print("Diferencias entre los mínimos:")
for key, value in diferencias_minimos.items():
    print(f"{key}: {value:.3f} segundos")

print("\nDiferencias entre los máximos:")
for key, value in diferencias_maximos.items():
    print(f"{key}: {value:.3f} segundos")

print("\nIntervalo de diferencias en los mínimos:")
if intervalo_minimos:
    print(f"Desde {intervalo_minimos[0]:.3f} segundos hasta {intervalo_minimos[1]:.3f} segundos")
else:
    print("No se encontraron diferencias para los mínimos")

print("\nIntervalo de diferencias en los máximos:")
if intervalo_maximos:
    print(f"Desde {intervalo_maximos[0]:.3f} segundos hasta {intervalo_maximos[1]:.3f} segundos")
else:
    print("No se encontraron diferencias para los máximos")
