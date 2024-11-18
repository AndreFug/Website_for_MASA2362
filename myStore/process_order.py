# process_order.py

import sys
from pymodbus.client import ModbusSerialClient as ModbusClient
# from pymodbus.constants import Defaults
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

def process_order(Size):
    # Since Size is already the variable to be sent, we proceed to send it via Modbus
    send_with_modbus(Size)
    print(f"Saving order with size: {Size}")
    print(f"Sending MQTT with size: {Size}")
    print(f"Sending Modbus with size: {Size}")

def send_with_modbus(Size):
    try:
        # Convert Size to a byte string
        byte_string = Size.encode() if isinstance(Size, str) else Size

        # Pad the byte string if necessary (odd-length strings)
        if len(byte_string) % 2 != 0:
            byte_string += b'\x00'  # Pad with null byte

        # Create a payload builder
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)

        # Add the string to the builder
        builder.add_string(byte_string)

        # Get the payload as a list of register values
        registers = builder.to_registers()

        # Configure Modbus client
        client = ModbusClient(
            method='rtu',
            port='/dev/ttyUSB0',  # Replace with your serial port
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=10  # Timeout in seconds
        )

        # Connect to Modbus device
        if client.connect():
            try:
                # Write the registers to the device
                address = 0  # Starting register address
                unit_id = 1  # Modbus slave unit ID
                result = client.write_registers(address, registers, unit=unit_id)
                if result.isError():
                    print(f"Error writing to Modbus registers: {result}")
                else:
                    print(f"Successfully wrote '{Size}' as {len(registers)} registers starting at address {address}")
            except Exception as e:
                print(f"Exception during Modbus communication: {e}")
            finally:
                client.close()
        else:
            print("Failed to connect to Modbus device.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python process_order.py <Size>")
    else:
        Size = sys.argv[1]
        process_order(Size)
