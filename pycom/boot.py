from network import WLAN

wlan = WLAN()
wlan.init(mode=WLAN.AP, ssid='IamDeath,DoW', auth=(WLAN.WPA2,'jesussss'), channel=7, antenna=WLAN.INT_ANT)