import network
import urequests

def connect():
    # Turn on Wi-Fi module
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # print("Available networks: ")
    # print(wlan.scan())

    # Connect to Wi-Fi/hot spot
    wlan.connect("Your Faithful FBI Agent", "1through8")

    while not wlan.isconnected():
        pass

    print(wlan.ifconfig())

    req = urequests.get("https://www.google.com")
    print(req.status_code)
    req.close()