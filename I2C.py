# Import the required libraries for I2C communication and time management.
import smbus
import time

# Customize the program by setting the time interval (in seconds) between readings and brightness level thresholds.
INTERVAL = 1
TOO_BRIGHT = 400
BRIGHT = 350
MEDIUM = 150
DARK = 100

# Define the I2C address for the light sensor and set it to continuous high-resolution mode.
LIGHT_SENSOR = 0x23
CONTINUOUS_HIGH_RES_MODE = 0x20
bus = smbus.SMBus(1)
bus.write_byte(LIGHT_SENSOR, CONTINUOUS_HIGH_RES_MODE)

# Function to retrieve and return the light reading from the LIGHT_SENSOR.
def getLightReading():
    bus.write_byte(LIGHT_SENSOR, CONTINUOUS_HIGH_RES_MODE)
    
    # Wait for the measurement to complete (timing depends on the selected mode).
    time.sleep(0.2)

    # Read the lux data from the LIGHT_SENSOR (2 bytes).
    lux_data = bus.read_i2c_block_data(LIGHT_SENSOR, 0x00, 2)

    # Convert the lux data to lux using the formula from the BH1750 datasheet.
    lux = int((lux_data[1] + (256 * lux_data[0])) / 1.2)

    return lux

# Function that categorizes the light level based on lux and returns a corresponding ranking as a string.
def getBrightnessRanking(lux):
    if lux >= TOO_BRIGHT:
        print(f"Current Light Level: {lux} lux - Too bright")
        return "Too bright"
    if lux < TOO_BRIGHT and lux >= BRIGHT:
        print(f"Current Light Level: {lux} lux - Bright")
        return "Bright"
    if lux < BRIGHT and lux >= MEDIUM:
        print(f"Current Light Level: {lux} lux - Medium")
        return "Medium"
    if lux < MEDIUM and lux >= DARK:
        print(f"Current Light Level: {lux} lux - Dark")
        return "Dark"
    if lux < DARK and lux > 0:
        print(f"Current Light Level: {lux} lux - Too dark")
        return "Too dark"

# Function to repeatedly print the light level.
def main():
    while True:
        lightLevel = getLightReading()
        print("Light level is " + getBrightnessRanking(lightLevel))
        time.sleep(INTERVAL)

# Entry point to the script; calls the main function.
if __name__ == "__main__":
    main()
