import board
import busio

# Initialize I2C using the default SCL and SDA pins for your board
# On most boards: board.SCL and board.SDA are predefined
try:
    i2c = busio.I2C(board.GP3, board.GP2)
except ValueError as e:
    print("Error initializing I2C:", e)
    raise SystemExit

# Wait until the I2C bus is ready
while not i2c.try_lock():
    pass

try:
    # Scan for devices
    devices = i2c.scan()

    if devices:
        print("I2C devices found:")
        for device in devices:
            print(f"  - Address: 0x{device:02X}")
    else:
        print("No I2C devices found.")
finally:
    # Always unlock the I2C bus
    i2c.unlock()