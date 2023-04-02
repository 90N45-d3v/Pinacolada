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

### Usage
Pinacolada will be accessible from your browser at `127.0.0.1:8888`.  
The default password is `CoconutsAreYummy`.  
After you have logged in, you can see a dashboard on the start page and you should change the password in the settings tab.

### E-Mail Notifications
<p>If configured, Pinacolada will alert you to attacks via E-Mail. In order to send you an E-Mail, however, an E-Mail account for Pinacolada must be specified in the settings tab. To find the necessary information such as SMTP server and SMTP port, search the internet for your mail provider and how their SMTP servers are configured + how to use them. Here are some information about known providers:</p>

| Provider | SMTP Server | SMTP Port (TLS)
| ------- | --------- | --------- |
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp.office365.com | 587 |
| GoDaddy | smtpout.secureserver.net | 587 |
