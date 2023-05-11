# Etherscape

## Raspberry Pi

The puredata Raspberry Pi patch requires a microphone input, such as a USB microphone. The default input can be modified as follows:

```
nano /.pdsettings
```


## Simulated
When not using a Raspberryi Pi, it is possible to simulate the WiFi input with wifi.py.

```
pip3 install oscpy

git clone https://github.com/Maximaaal/Etherscape.git

cd Etherscape

python3 wifi.py
