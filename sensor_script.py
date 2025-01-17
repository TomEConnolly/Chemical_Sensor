
import RPi.GPIO as GPIO
import time

# Set the GPIO pins for the TRIG and ECHO
TRIG = 23
ECHO = 24

def setup():
    """Initial setup for GPIO pins."""
    # Use Broadcom Pin Mode
    GPIO.setmode(GPIO.BCM)
    # Set TRIG as OUTPUT
    GPIO.setup(TRIG, GPIO.OUT)
    # Set ECHO as INPUT
    GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    """Measures the distance by sending a pulse and computing time of flight."""
    # Ensure TRIG is low initially
    GPIO.output(TRIG, False)
    # Allow the sensor to settle
    time.sleep(2)

    # Generate a 10 microsecond pulse on TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)

    # Measure the time the pulse is received back
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate pulse duration
    pulse_duration = pulse_end - pulse_start

    # Convert pulse duration to distance
    distance = pulse_duration * 17150  # Sound speed factor in cm/s
    distance = round(distance, 2)  # Round to two decimal places

    return distance

def cleanup():
    """Clean up GPIO settings before exiting."""
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        while True:
            # Call measure_distance function and print the result
            dist = measure_distance()
            print(f"Distance: {dist} cm")
            time.sleep(1)  # Delay of 1 second between readings
    except KeyboardInterrupt:
        # Gracefully handle user interruption with CTRL+C
        cleanup()
