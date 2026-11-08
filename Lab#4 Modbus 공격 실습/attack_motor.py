from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient("192.168.31.177", port=502)
client.connect()

client.write_coil(address=0, value=True)
print("Motor ON sent")
client.close()
