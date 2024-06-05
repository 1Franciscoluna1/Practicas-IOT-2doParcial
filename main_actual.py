import machine
import time
import dht
from machine import SoftI2C, Pin
import sh1106

# Definir las notas musicales
c = 261
d = 294
e = 329
f = 349
g = 391
gS = 415
a = 440
aS = 455
b = 466
cH = 523
cSH = 554
dH = 587
dSH = 622
eH = 659
fH = 698
fSH = 740
gH = 784
gSH = 830
aH = 880

# Configura el pin del buzzer
BUZZER_PIN = 18
buzzer = Pin(BUZZER_PIN, Pin.OUT)

# Función beep para las notas
def beep(note, duration):
    pwm = machine.PWM(buzzer)
    pwm.freq(note)
    pwm.duty(512)  # 50% duty cycle
    time.sleep_ms(duration)
    pwm.deinit()
    time.sleep_ms(50)

def first_section():
    beep(a, 500)
    beep(a, 500)
    beep(a, 500)
    beep(f, 350)
    beep(cH, 150)
    beep(a, 500)
    beep(f, 350)
    beep(cH, 150)
    beep(a, 650)
    time.sleep_ms(500)
    beep(eH, 500)
    beep(eH, 500)
    beep(eH, 500)
    beep(fH, 350)
    beep(cH, 150)
    beep(gS, 500)
    beep(f, 350)
    beep(cH, 150)
    beep(a, 650)
    time.sleep_ms(500)

def second_section():
    beep(aH, 500)
    beep(a, 300)
    beep(a, 150)
    beep(aH, 500)
    beep(gSH, 325)
    beep(gH, 175)
    beep(fSH, 125)
    beep(fH, 125)
    beep(fSH, 250)
    time.sleep_ms(325)
    beep(aS, 250)
    beep(dSH, 500)
    beep(dH, 325)
    beep(cSH, 175)
    beep(cH, 125)
    beep(b, 125)
    beep(cH, 250)
    time.sleep_ms(350)

def play_song():
    first_section()
    second_section()
    beep(f, 250)
    beep(gS, 500)
    beep(f, 350)
    beep(a, 125)
    beep(cH, 500)
    beep(a, 375)
    beep(cH, 125)
    beep(eH, 650)
    time.sleep_ms(500)
    second_section()
    beep(f, 250)
    beep(gS, 500)
    beep(f, 375)
    beep(cH, 125)
    beep(a, 500)
    beep(f, 375)
    beep(cH, 125)
    beep(a, 650)
    time.sleep_ms(650)

# Define los pines para el sensor ultrasónico
TRIG_PIN = 22
ECHO_PIN = 23

# Define el pin para el sensor DHT11
DHT_PIN = 5  # Cambia este número según tu configuración para evitar conflictos
BUTTON_PIN = 13
SERVO_PIN = 21

# Configura los pines GPIO
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)
dht11 = dht.DHT11(machine.Pin(DHT_PIN))
button = machine.Pin(BUTTON_PIN, machine.Pin.IN)
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50)

# Configura el I2C para el display OLED usando SoftI2C
i2c = SoftI2C(scl=Pin(15), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c)
# oled.rotate(1)

# Definir los pines de los segmentos
seg_a = machine.Pin(12, machine.Pin.OUT)
seg_b = machine.Pin(14, machine.Pin.OUT)
seg_c = machine.Pin(25, machine.Pin.OUT)
seg_d = machine.Pin(26, machine.Pin.OUT)
seg_e = machine.Pin(27, machine.Pin.OUT)
seg_f = machine.Pin(32, machine.Pin.OUT)
seg_g = machine.Pin(33, machine.Pin.OUT)

# Mapeo de las letras a los segmentos
letters = {
    'P': (1, 1, 0, 0, 1, 1, 1),
    'A': (1, 1, 1, 0, 1, 1, 1),
    'C': (1, 0, 0, 1, 1, 1, 0),
    'O': (1, 1, 1, 1, 1, 1, 0),
}

# # Configura el pin de la fotoresistencia
# pin_fotoresistencia = machine.Pin(35, machine.Pin.IN)

# # Configura el ADC para leer valores analógicos
# adc = machine.ADC(pin_fotoresistencia)

def display_letter(letter):
    segments = letters.get(letter, (0, 0, 0, 0, 0, 0, 0))
    seg_a.value(segments[0])
    seg_b.value(segments[1])
    seg_c.value(segments[2])
    seg_d.value(segments[3])
    seg_e.value(segments[4])
    seg_f.value(segments[5])
    seg_g.value(segments[6])

# Lista de letras a mostrar
letters_to_display = ['P', 'A', 'C', 'O']

# Función para medir distancia con el sensor ultrasónico
def medir_distancia():
    # Envía un pulso corto al pin Trig
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    # Espera un breve período para que el sensor se estabilice
    time.sleep_ms(2)
    
    # Espera a que el pin Echo se vuelva alto y mide el tiempo
    pulse_start = time.ticks_us()
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    
    # Espera a que el pin Echo se vuelva bajo y mide el tiempo
    pulse_end = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()
    
    # Calcula la duración del pulso y conviértela a distancia
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (pulse_duration * 0.0343) / 2  # En centímetros
    
    return distance

def mover_servo():
    # Mueve el servo a 0 grados
    servo.duty(40)
    time.sleep(1)
    
    # Mueve el servo a 180 grados
    servo.duty(115)
    time.sleep(1)
    
    # Mueve el servo a 90 grados
    servo.duty(77)
    time.sleep(1)

# Limpia la línea 2 (índice 1, ya que se cuenta desde 0)
def clear_line(line_index):
    # Calcula las coordenadas y la altura de la línea
    line_y = line_index * 10  # Suponiendo que cada línea tiene 10 píxeles de altura
    line_height = 10
    
    # Dibuja un rectángulo del color de fondo para cubrir la línea
    oled.fill_rect(0, line_y, oled_width, line_height, 0)
    
    # Actualiza la pantalla para reflejar los cambios
    oled.show()

try:
    while True:
        for letter in letters_to_display:
            # Medir distancia
            distancia = medir_distancia()
            # Medir temperatura y humedad
            try:
                dht11.measure()
                temperatura = dht11.temperature()
                humedad = dht11.humidity()
            except OSError as e:
                # print("Error al leer el DHT11:", e)
                temperatura = None
                humedad = None
            # Limpiar el display
            oled.fill(0)
            # Mostrar los valores en el display
            oled.text("Dist: {:.1f} cm".format(distancia), 0, 0)
            if temperatura is not None and humedad is not None:
                oled.text("Temp: {:.1f}C".format(temperatura), 0, 10)
                oled.text("Hum:  {:.1f}%".format(humedad), 0, 20)
            else:
                oled.text("Error DHT11", 0, 10)
            # Verificar si se presionó el botón para mover el servo
            oled.text("Servo:  Quieto", 0, 40)
            # if button.value() == 1:  # Presiona el botón para mover el servo
            #     clear_line(4)
            #     oled.text("Servo:  Moviendo", 0, 40)
            #     oled.show()
            #     mover_servo()
            #     clear_line(4)
            #     oled.text("Servo:  Quieto", 0, 40)
            #     oled.show()

            # Verificar si se presionó el botón para tocar la canción
            if button.value() == 1:  # Presiona el botón para iniciar la canción
                play_song()
            display_letter(letter)
            # Lee el valor analógico de la fotoresistencia
            # valor_analogico = adc.read()
            # # Mapea el valor analógico a un rango deseado (por ejemplo, 0-100)
            # # Si el rango máximo de lectura es 4095 (12 bits), el valor mapeado será entre 0 y 100
            # intensidad_luz = (valor_analogico / 4095) * 100
            # oled.text("Luz:  {:.1f}%".format(intensidad_luz), 0, 30)
            oled.show()
            time.sleep(1)  # Actualiza cada segundo
except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
    # Apagar todos los segmentos al interrumpir el programa
    seg_a.value(0)
    seg_b.value(0)
    seg_c.value(0)
    seg_d.value(0)
    seg_e.value(0)
    seg_f.value(0)
    seg_g.value(0)