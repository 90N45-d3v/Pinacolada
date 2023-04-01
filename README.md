![banner](https://user-images.githubusercontent.com/79598596/227720053-2c912d60-4c07-4b22-8205-134cfc63feed.svg)
<p align="center">
 <img src="https://img.shields.io/badge/Made%20with-Python-blue">
 <img src="https://img.shields.io/github/license/90N45-d3v/Pinacolada.svg">
 <img src="https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg">
</p>
<h3 align="center">Wireless Intrusion Detection System for Hak5's WiFi Coconut</h3>
<p>Pinacolada looks for typical IEEE 802.11 attacks and then informs you about them as quickly as possible. All this with the help of <a href="https://hak5.org/products/wifi-coconut">Hak5's WiFi Coconut</a>, which allows it to listen for threats on all 14 channels in the 2.4GHz range simultaneously.</p>

### Supported 802.11 Attacks
| Attack | Type | Status
| ------- | --------- | --------- |
| Deauthentication | DoS | ✅ |
| Disassociation | DoS | ✅ |
| Authentication | DoS | ✅ |
| EvilTwin | MiTM | 🔜 |
| KARMA | MiTM | 🔜 |

### Installation
````
# Download Pinacolada
git clone https://github.com/90N45-d3v/Pinacolada
cd Pinacolada

# Install required packages via pip
pip install flask multiprocessing

# Start Pinacolada
python main.py
````
