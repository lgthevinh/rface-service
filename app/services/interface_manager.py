import serial
import time
import json

import serial.tools
import serial.tools.list_ports

class InterfaceManager:
  def __init__(self, name: str):
    self.name = name if name else "InterfaceManager"
  
  def open(self):
    print(f"Opening {self.name} interface")
  
  def push_verified_result(self, result_data):
    print(f"Pushing face recognized result to {self.name}: {result_data}")
  
  def push_unverified_result(self, result_data):
    print(f"Pushing face unrecognized result to {self.name}: {result_data}")
  
  def close(self):
    print(f"Closing {self.name} interface")
  
  def to_dict(self):
    return {
      "name": self.name
    }
  
class UartInterfaceManager(InterfaceManager):
  @staticmethod
  def get_uart_ports():
    return [port.device for port in serial.tools.list_ports.comports()]
  
  def __init__(self, name="UartInterfaceManager", port=None, baudrate=9600, timeout=1):
    self.name = name
    self.port = port
    self.baudrate = baudrate
    self.timeout = timeout
    self.serial = None
  
  def open(self):
    try:
      self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
      time.sleep(2) # Wait for the serial connection to be established
    except serial.SerialException as e:
      self.serial = None
      raise e
  
  def push_verified_result(self, result_data: dict):
    super().push_verified_result(result_data)
    if self.serial and self.serial.is_open:
      try:
        json_data = json.dumps(result_data)
        self.serial.write((json_data + "\n").encode())
        print(f"Data sent via UART: {json_data}")
      except serial.SerialException as e:
        print(f"Error sending data via UART: {e}")
        
  def close(self):
    if self.serial:
      self.serial.close()
  
  def to_dict(self):
    return {
      "type": "uart",
      "name": self.name,
      "port": self.serial.port,
      "baudrate": self.serial.baudrate,
      "timeout": self.serial.timeout
    }

class CustomUartInterface(UartInterfaceManager):
  def push_verified_result(self, result_data):
    pass
  
  def push_unverified_result(self, result_data):
    pass
  