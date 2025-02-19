from muselsl import stream, list_muses
import time

def main():
    print("Buscando dispositivos Muse...")

    muse_target = None
    while muse_target is None:
        muses = list_muses()
        if not muses:
            print("No se encontro ningun dispositivo Muse. Se reintentara la busqueda dentro de 5 segundos...")
            time.sleep(5)
            continue
        
        # Buscar el dispositivo con la MAC espec�fica y el nombre espec�fico
        muse_target = next((muse for muse in muses if muse['address'] == '00:55:DA:B8:18:B6' and muse['name'] == 'Muse-18B6'), None)
        if muse_target:
            print(f"Dispositivo encontrado: {muse_target['name']} ({muse_target['address']})")
        else:
            print("Dispositivo especifico no encontrado. Se reintentara la busqueda dentro de 5 segundos...")
            time.sleep(5)

    print(f"Conectando a Muse: {muse_target['name']}, ({muse_target['address']})")      
    try:
        print("Iniciando transmision de datos EEG...")
        stream(address=muse_target['address'])
    except KeyboardInterrupt:
        print("\nTransmision detenida por el usuario.")

if __name__ == "__main__":
    main()
