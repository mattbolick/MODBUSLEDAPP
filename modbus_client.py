from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException

class ModbusClient:
    def __init__(self):
        self.client = None
        self.is_connected = False

    def connect(self, ip_address, port):
        try:
            self.client = ModbusTcpClient(ip_address, port=port)
            self.is_connected = self.client.connect()
            return self.is_connected
        except ConnectionException as e:
            print(f"Error connecting to Modbus server: {e}")
            self.is_connected = False
            return False

    def write_color(self, red, green, blue):
        # Assuming Holding Registers are used to store color values:
        # - Address 0: Red
        # - Address 1: Green
        # - Address 2: Blue

        try:
            # Write multiple registers at once
            self.client.write_registers(0, [red, green, blue], slave=255) 
            # If you need to change the default unit/slave ID, change it here ^
        except ConnectionException as e:
            print(f"Error writing to Modbus server: {e}")
            self.is_connected = False
            self.client.close()

    def disconnect(self):
        if self.client:
            self.client.close()
            self.is_connected = False