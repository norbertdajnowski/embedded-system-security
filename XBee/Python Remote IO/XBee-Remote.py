from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time
import threading

PORT = "COM6"
BAUD_RATE = 9600
REMOTE_NODE_ID = "XBEE_B"
IOLINE_IN = IOLine.DIO2_AD2

def air_readings(value):
    sensor_volt = (value/1024) * 5.0
    RS_air = (5.0-sensor_volt)/sensor_volt
    R0 = RS_air/9.9
    ratio = RS_air / R0

    print("sensor_volt = ", sensor_volt)
    print("RS_ratio = ", RS_air)
    print("Rs/R0 = ", ratio) 
    print("\n")

def main():
    print(" +--------------------------------------------+")
    print(" | XBee Python Library Read Remote ADC Sample |")
    print(" +--------------------------------------------+\n")

    stop = False
    th = None

    local_device = XBeeDevice(PORT, BAUD_RATE)

    try:
        local_device.open()
        xbee_network = local_device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        remote_device.set_io_configuration(IOLINE_IN, IOMode.ADC)

        def read_adc_task():
            while not stop:
                
                value = remote_device.get_adc_value(IOLINE_IN)
                print("True Value: ", value)
                air_readings(value)

                time.sleep(5)

        th = threading.Thread(target=read_adc_task)

        time.sleep(0.5)
        th.start()

        input()

    finally:
        stop = True
        if th is not None and th.isAlive():
            th.join()
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == '__main__':
    main()