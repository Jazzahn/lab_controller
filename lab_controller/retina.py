# retina.py

import serial

if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/tty.usbserial-0130F9A1', 9600, timeout=1)
        ser.reset_input_buffer    
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
    except:
        print(f"Puzzle Unplugged")

