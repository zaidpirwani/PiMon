# PiMon = Raspberry Pi Monitor
using a Pi 3 with multitude of Sensors to monitor environment.

## Connected Hardware (mentioned pins are BCM Pins)
### OUTPUTS
* Nokia 5110/3310 LCD (RST,CE,D/C,DIN,CLK==24,8,23,10,11)
* LED (21)
* Buzzer (16 - with 2N2222)
* USB Powered Speaker

### INPUTS
* TSOP17xx IR Receiver (20)
* 5x Push-to-Make Buttons (26,19,13,6,5)
* DHT11 Temperature and Humidity Sensor (17)
* DS18B20 Temperature Sensor (4)
* DS1307 RTC (SDA,SCL==2,3)
* USB WebCam

## Libraries/Software Tools (used/planned to be used)
* Adafruit Nokia LCD Library
* Adafruit Python DHT Library
* Python RPI GPIO
* Wiring Pi
* LIRC

### Device Tree (/boot/config.txt)
* IR Input (gpio-ir)
* DHT11
* DS1307 RTC
