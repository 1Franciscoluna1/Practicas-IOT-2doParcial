import network
import time

# Configurar el ESP32 como Access Point
ssid = 'ESP32-AP'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

print('Configurando Access Point...')
while not ap.active():
    time.sleep(1)

print('Access Point activo')
print('IP del AP:', ap.ifconfig()[0])

# Función para convertir la dirección MAC a una cadena legible
def mac_a_cadena(mac):
    return ':'.join(['{:02x}'.format(b) for b in mac])

# Función para verificar dispositivos conectados
def verificar_conexiones(ap):
    clientes_conectados = ap.status('stations')
    if len(clientes_conectados) > 0:
        for cliente in clientes_conectados:
            mac = cliente[0]
            print('Dispositivo conectado:', mac_a_cadena(mac))
    else:
        print('Esperando conexiones...')

while True:
    verificar_conexiones(ap)
    time.sleep(5)  # Verificar cada 5 segundos
