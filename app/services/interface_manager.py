import serial
import time
import json
import serial.tools
import serial.tools.list_ports
from services.database_manager import DatabaseManager

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
    raise NotImplementedError("to_dict method must be implemented in child class")
  
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
      "port": self.port,
      "baudrate": self.baudrate,
      "timeout": self.timeout
    }

class CustomUartInterface(UartInterfaceManager):
  serPort = serial.Serial()
  serPort.timeout = 1  # Set timeout (optional)
  serPort.bytesize = serial.EIGHTBITS
  serPort.parity = serial.PARITY_NONE
  serPort.stopbits = serial.STOPBITS_ONE
  serPort.dsrdtr = False  # Prevent automatic opening
  serPort.rtscts = False
  TYPE_VERIFIED_HUMAN = 0x01
  TYPE_NONVERIFIED_HUMAN = 0x02
  
  def __init__(self, name):
    self.name = name
  
  def connectToPort(self, name, baudrate):
    try:
      self.serPort.port = name
      self.serPort.baudrate = baudrate
      self.serPort.open()
      print("connected to port")
      return True
    except KeyError as e:
      print(e)
      return False

  def getPorts(self):
    # Step 1: Scan available serial ports
    ports = serial.tools.list_ports.comports()
    port_info = []  # Changed to store information about all ports

    for port in ports:
      # Collecting information about each port
      port_info.append(
        {"device": port.device, "description": port.description, "hwid": port.hwid}
      )

    return port_info  # Return the collected port information

  def sendData(self, data):
    self.serPort.write(data)

  def getTargetPort(self, target_vid="1A86", target_pid="7523"):
    ports = self.getPorts()  # Updated variable name
    VID = ["1A86", "10C4", "0403", "067B"]
    for port in ports:
      hwid = port["hwid"]  # Example: "USB VID:PID=1A86:7523 LOCATION=7-1"
      for vid in VID:
        if f"VID:PID={vid}" in hwid:
            return True, port["device"]
      if f"VID:PID={target_vid}" in hwid:
        return True, port["device"]
    return False, None

  def sendNotifyEnable(self, type, id):
    if type == self.TYPE_VERIFIED_HUMAN:
      
      # Convert id to a list of hex bytes
      id_bytes = []
      while id > 0:
        id, bytes = divmod(id, 256)
        id_bytes.append(bytes)
      
      size = len(id_bytes) + 4
      frames = [0x72, 0x67, 0x00, 0x00, 0x00, 0x00, 0x01]
      frames[2] = size >> 8
      frames[3] = size & 0xFF
      frames.extend(id_bytes)
      frames.append(0xFF)
      self.sendData(frames)
    elif type == self.TYPE_NONVERIFIED_HUMAN:
      frames = [0x72, 0x67, 0x00, 0x04, 0x01, 0x02, 0x02, 0xFF]
      self.sendData(frames)
  
  def open(self):
    state, name = self.getTargetPort()
    if state:
      print(f"port Founded: {name}")
      self.connectToPort(name, 115200)
    else:
      print("port not found")
  
  def push_verified_result(self, result_data):
    self.sendNotifyEnable(self.TYPE_VERIFIED_HUMAN, result_data["face"]["id"])
  
  def push_unverified_result(self, result_data):
    self.sendNotifyEnable(self.TYPE_NONVERIFIED_HUMAN, None)
    
  def to_dict(self):
    return {
      "type": "cuart",
      "name": self.name,
      "timeout": self.serPort.timeout,
    }
    
class LogInterfaceManager(InterfaceManager):
  db_manager = DatabaseManager()
  
  def __init__(self, camera_id: int, name="LogInterfaceManager"):
    self.name = name
    self.camera_id = camera_id
  
  def push_verified_result(self, result_data):
    self.db_manager.store_log(camera_id=self.camera_id, detected_face_id=result_data["face"]["id"])
    
  def push_unverified_result(self, result_data):
    self.db_manager.store_log(camera_id=self.camera_id, detected_face_id=None)
  
  def to_dict(self):
    return {
      "type": "log",
      "name": self.name,
      "camera_id": self.camera_id
    }