from network import LoRa
import binascii
lora = LoRa(mode=LoRa.LORAWAN, public=1, adr=0, tx_retries=0)
print("Device LoRa MAC")
print(binascii.hexlify(lora.mac()))
