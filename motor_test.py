from machine import Pin, PWM
import time

ANGLE_CALIBRATION_FACTOR = 0.5
class Motor():
    """JGA25-370 DC gear motor via L298N H-bridge with encoder feedback.

    L298N wiring:
        CW pin  → PWM drive clockwise
        CCW pin → PWM drive counter-clockwise
    JGA25-370 encoder:
        Channel A, Channel B → relative position tracking
        ~11 PPR x 21.3 gear ratio ≈ 234 counts/output revolution
        Adjust COUNTS_PER_REV for your gear ratio variant.
    """
    COUNTS_PER_REV = 234  # 11 PPR * 21.3:1 gear ratio
    MIN_WAIT_TIME_MS = 20

    def __init__(self, cw_pin=25, ccw_pin=26,
                 enc_a_pin=32, enc_b_pin=33, pwm_freq=1000):
        # L298A PWM direction pins
        self.cw = PWM(Pin(cw_pin), freq=pwm_freq, duty=0)
        self.ccw = PWM(Pin(ccw_pin), freq=pwm_freq, duty=0)
        
        # Current needle angle in degrees (from boot position = 0°).
        self.angle = 0
        self._last_drive_time = time.ticks_ms()
        self._last_speed = 0

    # Approximate degrees per second at full duty (1023). Tune for your motor/gear ratio.
    DEG_PER_SEC_AT_FULL = 720.0

    def _drive(self, speed):
        """Set motor speed: positive = CW, negative = CCW, 0 = stop.
        Speed range: -1023 to 1023.
        Duty is inverted: 0 = full power, 1023 = no power.
        Updates self.angle based on elapsed time and previous speed.
        """
        now = time.ticks_ms()
        dt = time.ticks_diff(now, self._last_drive_time) / 1000.0  # seconds
        self.angle += (self._last_speed / 1023.0) * self.DEG_PER_SEC_AT_FULL * dt
        self.angle = self.angle % 360
        #sleep if drive time is too close to now 
        if dt * 1000 <= MIN_WAIT_TIME_MS:
            time.sleep_ms(MIN_WAIT_TIME_MS - dt)
        self._last_drive_time = now

        speed = max(-1023, min(1023, int(speed)))
        print(f"{self.angle=}")
        print(f"{speed=}")
        self._last_speed = speed
        
        if speed > 0:
            self.cw.duty(abs(speed))
            self.ccw.duty(0)
        elif speed < 0:
            self.cw.duty(0)
            self.ccw.duty(abs(speed))
        else:
            self.cw.duty(0)
            self.ccw.duty(0)

    def stop(self):
        self._drive(0)

    def go_to_angle(self, target, deadzone=10):
        """Drive toward target angle. Call repeatedly in a loop.
        Returns the current angular error.
        """
        error = target - self.angle
        # Normalize to shortest path (-180 to 180)
        error = ((error + 180) % 360) - 180

        if abs(error) < deadzone:
            self.stop()
            return error

        # Proportional speed: min 300 (enough to move), max 1023
        speed = max(512, min(512, int(abs(error) * 0.01)))
        if error < 0:
            speed = -speed
        self._drive(speed)
        return error


def test_hold_one_angle(): 
    m = Motor()
    while True:
        m.go_to_angle(180)

def test_max_ocilate():
    m = Motor()
    prev = 0
    while True:
        prev = 180 if prev == 0 else 0
        m.go_to_angle(prev)

if __name__ == '__main__':
    m = Motor()
    # Sweep test: 0° → 90° → 180° → 90° → 0°
    for target in (90, 180, 90, 0):
        print("Target:", target)
        while True:
            err = m.go_to_angle(target)
            if abs(err) < 5:
                break
            time.sleep_ms(20)
        time.sleep(1)
    m.stop()
