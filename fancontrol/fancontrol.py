import utime as time


PERIOD = 60

TEMP = "/sys/class/hwmon/hwmon0/temp1_input"
FAN_PWM = "/sys/class/hwmon/hwmon1/device/pwm1"
FAN_RPM = "/sys/class/hwmon/hwmon1/device/fan1_input"  # Min value (pwm=1) ~1935

TEMP_LOW = 43
TEMP_HIGH = 50

PWM_MIN = 0
PWM_MAX = 255


def get_val(f):
    val = int(f.read())
    f.seek(0)
    return val


def set_val(f, val):
    #print("Setting PWM:", val)
    f.write("%d\n" % val)


def tstamp():
    return "%04d-%02d-%02d %02d:%02d:%02d" % (time.localtime()[:6])


f_temp = open(TEMP)
f_pwm = open(FAN_PWM, "w")
f_rpm = open(FAN_RPM)

prev_temp = 0

while True:
    temp = get_val(f_temp) / 1000
    rpm = get_val(f_rpm)
    extra = ""

    if temp <= TEMP_LOW:
        pwm_val = PWM_MIN
    elif temp >= TEMP_HIGH:
        pwm_val = PWM_MAX
    else:
        pwm_range = PWM_MAX - PWM_MIN
        temp_range = TEMP_HIGH - TEMP_LOW
        temp_pcnt = (temp - TEMP_LOW) / temp_range
        pwm_val = pwm_range * temp_pcnt + PWM_MIN
        extra = ", temp ratio: %.2f" % temp_pcnt
        pwm_val = int(pwm_val)

    if temp != prev_temp:
        print("%s cur temp: %.1f, cur rpm: %s, new pwm: %s%s" % (
            tstamp(), temp, rpm, pwm_val, extra
        ))

    set_val(f_pwm, pwm_val)
    prev_temp = temp
    time.sleep(PERIOD)
