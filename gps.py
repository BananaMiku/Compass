import machine
import utime

uart = machine.UART(2, baudrate=9600, tx=17, rx=16)
def get_gps_location():
    buffer = b""
    while True:
        if uart.any():
            buffer += uart.read(uart.any())
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            try:
                sentence = line.decode('ascii').strip()
            except Exception:
                continue

            if sentence.startswith('$GPGGA') or sentence.startswith('$GNGGA'):
                lat, lng = parse_nmea_gga(sentence)
                if lat is not None and lng is not None:
                    return lat, lng

            elif sentence.startswith('$GPGLL') or sentence.startswith('$GNGLL'):
                lat, lng = parse_nmea_gll(sentence)
                if lat is not None and lng is not None:
                    return lat, lng
        utime.sleep_ms(100)

def parse_nmea_gll(sentence):
    parts = sentence.split(',')
    if len(parts) < 5:
        return None, None
    try:
        lat_raw = parts[1]
        lat_dir = parts[2]
        lng_raw = parts[3]
        lng_dir = parts[4]

        if not lat_raw or not lng_raw:
            return None, None

        lat = convert_to_decimal(lat_raw, lat_dir)
        lng = convert_to_decimal(lng_raw, lng_dir)
        return lat, lng
    except Exception:
        return None, None

def parse_nmea_gga(sentence):
    parts = sentence.split(',')
    if len(parts) < 6:
        return None, None
    try:
        fix_quality = int(parts[6]) if parts[6] else 0
        if fix_quality == 0:
            return None, None  # No fix yet

        lat_raw = parts[2]
        lat_dir = parts[3]
        lng_raw = parts[4]
        lng_dir = parts[5]

        if not lat_raw or not lng_raw:
            return None, None

        lat = convert_to_decimal(lat_raw, lat_dir)
        lng = convert_to_decimal(lng_raw, lng_dir)
        return lat, lng
    except Exception:
        return None, None

def convert_to_decimal(value, direction):
    if len(value) < 4:
        return None
    dot_pos = value.index('.')
    deg_digits = dot_pos - 2  
    degrees = float(value[:deg_digits])
    minutes = float(value[deg_digits:])
    decimal = degrees + minutes / 60.0
    if direction in ('S', 'W'):
        decimal = -decimal
    return decimal


def test():
    print(get_gps_location())

if __name__ == '__main__':
    test()
