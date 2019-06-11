![Crypto Scroll pHAT HD](crypto-scroll-phat-hd-logo.png)

Cryptocurrencies price scrolling goodness!

This script require Python 3 and the Cryptonator API.

## Hardware
You'll need a Raspberry Pi and a Scroll pHAT:

https://shop.pimoroni.com/products/scroll-phat-hd


## Installing

### Full install (recommended):

Pimoroni has created an easy installation script that will install all pre-requisites and get your Scroll pHAT HD
up and running with minimal efforts. To run it, fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop, as illustrated below:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the command exactly as it appears below (check for typos) and follow the on-screen instructions:

```bash
curl https://get.pimoroni.com/scrollphathd | bash
```

When the necessary libraries have been successfully installed you can copy crypto_scroll.py in /home/pi/Projects and add it to the crontab by typing:

```bash
crontab -e
```

```
*/2 * * * * /usr/bin/python3 /home/pi/Projects/crypto_scroll.py
```

It will automatically start to scroll when the Pi is restarted.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/qjFf3hSImd0/0.jpg)](https://www.youtube.com/watch?v=qjFf3hSImd0)

## Links

* Cryptonator API - https://www.cryptonator.com/api
* Python library for Scroll pHAT HD - https://github.com/pimoroni/scroll-phat-hd'
* YouTube - https://www.youtube.com/watch?v=qjFf3hSImd0
