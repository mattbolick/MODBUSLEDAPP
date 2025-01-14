from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusException
import time

class ModbusClient:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.ip_address = None
        self.port = None

    def connect(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        try:
            self.client = ModbusTcpClient(ip_address, port=port)
            self.is_connected = self.client.connect()
            return self.is_connected
        except ConnectionException as e:
            print(f"Error connecting to Modbus server: {e}")
            self.is_connected = False
            return False

    def write_color(self, red, green, blue):
        # Write each color individually, handling errors gracefully
        try:
            # Write red to register 0
            if not self.write_register_with_retry(0, red, slave=255):
                print(f"Failed to write red color to register 0")

            # Write green to register 1
            if not self.write_register_with_retry(1, green, slave=255):
                print(f"Failed to write green color to register 1")

            # Write blue to register 2
            if not self.write_register_with_retry(2, blue, slave=255):
                print(f"Failed to write blue color to register 2")

        except ModbusException as e:
            print(f"General Modbus error: {e}")
            self.is_connected = False
            if self.client:
                self.client.close()

    def write_register_with_retry(self, address, value, slave, retries=1, retry_delay=0.1):
        """
        Writes a value to a Modbus register with retries on failure.

        Args:
            address: The register address to write to.
            value: The value to write.
            slave: The slave ID.
            retries: The number of retry attempts.
            retry_delay: The delay in seconds between retries.

        Returns:
            True if the write was successful, False otherwise.
        """
        for attempt in range(retries + 1):
            try:
                result = self.client.write_register(address, value, slave=slave)
                if result.isError():
                    raise ModbusException(f"Modbus error response: {result}")
                return True  # Write successful

            except ModbusException as e:
                print(f"Attempt {attempt + 1} to write to register {address} failed: {e}")
                if attempt < retries:
                    time.sleep(retry_delay)
                    self.reset_connection()
                else:
                    return False  # Write failed after all retries

    def reset_connection(self):
        """
        Closes the current connection and attempts to reconnect.
        """
        if self.client:
            self.client.close()
        try:
            self.client = ModbusTcpClient(self.ip_address, port=self.port)
            self.is_connected = self.client.connect()
            if self.is_connected:
                print("Modbus connection reset successfully.")
            else:
                print("Failed to reset Modbus connection.")
        except ConnectionException as e:
            print(f"Error resetting Modbus connection: {e}")
            self.is_connected = False

    def disconnect(self):
        if self.client:
            self.client.close()
            self.is_connected = False