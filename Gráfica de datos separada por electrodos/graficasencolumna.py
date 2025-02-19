import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo CSV
file_path = 'pruebaUsuario.csv'
#file_path = r'G:\Tesis\señales grabadas\prueba1.csv'

# Cargar el archivo CSV
data = pd.read_csv(file_path)

# Crear una figura con 4 subgráficas en una columna
fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

# Graficar TP9
axs[0].plot(data['timestamps'], data['TP9'], label='TP9', color='blue', alpha=0.7)
axs[0].set_title('Señal TP9')
axs[0].set_ylabel('Amplitud')
axs[0].grid(True)

# Graficar TP10
axs[1].plot(data['timestamps'], data['TP10'], label='TP10', color='orange', alpha=0.7)
axs[1].set_title('Señal TP10')
axs[1].set_ylabel('Amplitud')
axs[1].grid(True)

# Graficar AF7
axs[2].plot(data['timestamps'], data['AF7'], label='AF7', color='green', alpha=0.7)
axs[2].set_title('Señal AF7')
axs[2].set_ylabel('Amplitud')
axs[2].grid(True)

# Graficar AF8
axs[3].plot(data['timestamps'], data['AF8'], label='AF8', color='red', alpha=0.7)
axs[3].set_title('Señal AF8')
axs[3].set_ylabel('Amplitud')
axs[3].set_xlabel('Timestamps')
axs[3].grid(True)

# Ajustar el diseño para que no se superpongan
plt.tight_layout()

# Mostrar la gráfica
plt.show()
