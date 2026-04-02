
import serial
import numpy as np

class Uart_MM():
    def __init__(self, port, baudrate):
      self.port = port
      self.baudrate = baudrate
      self.ser = serial.Serial(port, baudrate, timeout=2)

    def write(self,adr,data):
      # Set LSB to '1' for WRITE command
      print("UART MM : ",hex(adr),data)
      adr = adr << 1 
      adr += 1 
      
      # Create 4 bytes
      adr_l = adr & 0x00FF
      adr_h = adr  >> 8 
      data_l = data & 0x00FF
      data_h = data  >> 8 
      bytes_val0 = adr_l.to_bytes(1, 'little')
      bytes_val1 = adr_h.to_bytes(1, 'little')
      bytes_val2 = data_l.to_bytes(1, 'little')
      bytes_val3 = data_h.to_bytes(1, 'little')
      word = bytes_val0 + bytes_val1 + bytes_val2 + bytes_val3
      #print(word)
      # send it
      self.ser.write(word)
