import network
from machine import RTC
import time

def connect():
    wlan = network.WLAN(mode=network.WLAN.STA)
    wlan.connect('VM8707621', auth=(network.WLAN.WPA2, 'sm7zkSspWsmq'))
    while not wlan.isconnected():
        time.sleep_ms(50)
    print(wlan.ifconfig())
    rtc = RTC()
    rtc.ntp_sync("pool.ntp.org")
    while not rtc.synced():
        time.sleep_ms(50)
    print(rtc.now())
