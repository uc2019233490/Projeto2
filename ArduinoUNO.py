from ctypes import sizeof
from pickle import TRUE
from numpy import true_divide
import serial, time, random  
import psycopg2
import psycopg2.extras
from twilio.rest import Client

def main():

    connected = False    
    # open the serial port that your arduino is connected to.    
    arduino = serial.Serial("COM9", 9600)   

    print(arduino.name) 
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    while TRUE:
        cur.execute("select unlock_door from home where home_name = 'Smart Lock'")
        [unlock_door] = cur.fetchone()
        print(unlock_door)
        if(unlock_door == True):
            cur.execute("update home set unlock_door = 'FALSE' where home_name = 'Smart Lock'")
            conn.commit()
            print("Abrindo porta")
            #arduino.write(b'1')
            arduino.write("1".encode())


    cur.close()
    conn.close()

#run main function
if __name__ == "__main__":
    main()
