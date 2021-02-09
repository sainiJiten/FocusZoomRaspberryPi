# To do the manual or auto focus:

### Install the required packages (pip3 install )
- numpy
- opencv-python
- opencv-contrib-python==4.1.0.25
- picamera
- "picamera[array]"
- adafruit-circuitpython-mcp3xxx (For controlling potentiometer)


### Enable i2c in the configuration:
- Run sudo raspi-config
- Choose 5.Interfacing options
- Enable I2C
- Enable SPI

### Add(or uncomment, if present) the following lines in the config.txt under the boot folder of the raspi OS:

 - dtparam=i2c_arm=on
- dtparam=i2c1=on
- dtoverlay=spi1-1cs,cs0_pin=05

### Run the program using: python3 filename
