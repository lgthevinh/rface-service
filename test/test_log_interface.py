import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from services.interface_manager import LogInterfaceManager

log_interface = LogInterfaceManager(camera_id=1, name="LogInterfaceManager")
log_interface.open()

if __name__ == "__main__":
  log_interface.push_verified_result({"face": {"id": 1}})
  log_interface.push_unverified_result({"result": 0})
  
  log_interface.close()
  print("LogInterfaceManager test completed.")