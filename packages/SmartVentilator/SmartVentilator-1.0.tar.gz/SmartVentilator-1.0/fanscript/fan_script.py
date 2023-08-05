import os
import sense_hat
from time import sleep
import math
import smtplib

sh = sense_hat.SenseHat()

# Color definitions for LED - Matrix
wh = (255,255,255)
bl = (0,0,0)
    
# LED - Matrix when fan is in use
#pixel tekening frame 1
fan1 = [bl,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,bl,
		wh,wh,wh,wh,wh,wh,wh,wh,
		wh,wh,wh,wh,wh,wh,wh,wh,
		bl,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,bl]
#pixel tekening frame 2	
fan2 = [bl,bl,bl,bl,wh,wh,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,bl,
		wh,bl,bl,wh,wh,bl,bl,bl,
		wh,wh,wh,wh,wh,wh,wh,bl,
		bl,wh,wh,wh,wh,wh,wh,wh,
		bl,bl,bl,wh,wh,bl,bl,wh,
		bl,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,wh,wh,bl,bl,bl,bl]
#pixel tekening frame 3
fan3 = [bl,bl,bl,bl,bl,wh,wh,bl,
		wh,bl,bl,bl,wh,wh,bl,bl,
		wh,wh,bl,wh,wh,bl,bl,bl,
		bl,wh,wh,wh,wh,wh,bl,bl,
		bl,bl,wh,wh,wh,wh,wh,bl,
		bl,bl,bl,wh,wh,bl,wh,wh,
		bl,bl,wh,wh,bl,bl,bl,wh,
		bl,wh,wh,bl,bl,bl,bl,bl]
#pixel tekening frame 4		
fan4 = [wh,bl,bl,bl,bl,bl,wh,wh,
		wh,wh,bl,bl,bl,wh,wh,bl,
		bl,wh,wh,bl,wh,wh,bl,bl,
		bl,bl,wh,wh,wh,bl,bl,bl,
		bl,bl,bl,wh,wh,wh,bl,bl,
		bl,bl,wh,wh,bl,wh,wh,bl,
		bl,wh,wh,bl,bl,bl,wh,wh,
		wh,wh,bl,bl,bl,bl,bl,wh]
#pixel tekening frame 5
fan5 = [wh,wh,bl,bl,bl,bl,bl,wh,
		bl,wh,wh,bl,bl,bl,wh,wh,
		bl,bl,wh,wh,bl,wh,wh,bl,
		bl,bl,bl,wh,wh,wh,bl,bl,
		bl,bl,wh,wh,wh,wh,bl,bl,
		bl,wh,wh,bl,wh,wh,bl,bl,
		wh,wh,bl,bl,bl,wh,wh,bl,
		wh,bl,bl,bl,bl,bl,wh,wh]
#pixel tekening frame 6	
fan6 = [bl,wh,wh,bl,bl,bl,bl,bl,
		bl,bl,wh,wh,bl,bl,bl,wh,
		bl,bl,bl,wh,wh,bl,wh,wh,
		bl,bl,wh,wh,wh,wh,wh,bl,
		bl,wh,wh,wh,wh,wh,bl,bl,
		wh,wh,bl,wh,wh,bl,bl,bl,
		wh,bl,bl,bl,wh,wh,bl,bl,
		bl,bl,bl,bl,bl,wh,wh,bl]
#pixel tekening frame 7		
fan7 = [bl,bl,wh,wh,bl,bl,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,wh,
		bl,wh,wh,wh,wh,wh,wh,wh,
		wh,wh,wh,wh,wh,wh,wh,bl,
		wh,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,bl,wh,wh,bl,bl,bl,
		bl,bl,bl,bl,wh,wh,bl,bl]


# Calculate dew point
def get_dew_point_c(t_air_c, rel_humidity):
    """Compute the dew point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param rel_humidity: relative humidity in %
    :type rel_humidity: float
    :return: the dew point in degrees Celsius
    :rtype: float
    """
    # standard variables
    A = 17.27
    B = 237.7
    
    # the calculation of the dew point
    alpha = ((A * t_air_c) / (B + t_air_c)) + math.log(rel_humidity/100.0)
    return (B * alpha) / (A - alpha)

# Calculate run time
def run_time(ruti):
    run_time = ((ruti * 3.24) / 60)
    return run_time

# Main program
def run_fan_script():
    os.chdir('/home/pi/hub-ctrl.c')
    # Create global variable
    ruti = 0
    
    #Variable speech spam prevention
    spam = 0
    
    try:
	# Infinite loop
        while True:
	    
             # Get sensor data
            humi = round(sh.get_humidity())
            temp = round(sh.get_temperature())

	    
            # Fan power will be cut until the humidity is higher than 50% and LED and the dew point is lower than 15 - Matrix will be turned to green
            if humi < 50 and get_dew_point_c(temp, humi) < 15:
                if spam != 0:
                    os.system("echo \"tuurnniinng off.\" | festival --tts")
                    spam = 0
                os.system('sudo ./hub-ctrl -h 1 -P 2 -p 0')
                sh.set_pixels(fan3)
                print(" uit")
                spam = 0
                sleep(3)

            # Fan kicks in when humidity is higher than 50%
            else:
                if spam != 1:
                    os.system("echo \"tuurrnniinng onn.\" | festival --tts")
                    spam = 1
                os.system('sudo ./hub-ctrl -h 1 -P 2 -p 1')
                print("aan")
                for a in range(0,6):
                    sh.set_pixels(fan1)
                    sleep(0.08)
                    sh.set_pixels(fan2)
                    sleep(0.08)
                    sh.set_pixels(fan3)
                    sleep(0.08)
                    sh.set_pixels(fan4)
                    sleep(0.08)
                    sh.set_pixels(fan5)
                    sleep(0.08)
                    sh.set_pixels(fan6)
                    sleep(0.08)
                    sh.set_pixels(fan7)
                    sleep(0.08)
                    print(a)
		ruti += 1
    except KeyboardInterrupt:
        sh.clear()
        os.system("echo \"shutting down.\" | festival --tts")
        os.system('sudo ./hub-ctrl -h 1 -P 2 -p 0')
        try:
            # Define email settings
            s = smtplib.SMTP('smtp.gmail.com', 587)
            sender = 'UwVentilator@gmail.com'
            senderww = 'wateenvent'
            recipient = 'RinPierneef@gmail.com' 
            message = """Subject: SmartVentilator run data

 Uw ventilator heeft {runtime} minuten gedraaid. """.format(runtime=run_time(ruti))
            s.ehlo()
            s.starttls()
            s.login(sender, senderww)
            s.sendmail(sender, recipient, message)
            os.system("echo \"E-mail has been sent.\" | festival --tts")
            
        except:
            os.system("echo \"E-mail failed to send.\" | festival --tts")
        sleep(1)
        os.system("echo \"Program has been terminated.\" | festival --tts")
run_fan_script()
