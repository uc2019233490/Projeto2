# import the serial library    
from ctypes import sizeof
from pickle import TRUE
from numpy import true_divide
import serial, time, random  
import psycopg2
import psycopg2.extras
from twilio.rest import Client

def main_prog():
    numero =''
    # Boolean variable that will represent whether or not the arduino is connected    
    connected = False    
    # open the serial port that your arduino is connected to.    
    arduino = serial.Serial("COM8", 9600)   

    print(arduino.name)    
    

    # if serial available save value in var, print value and clear it afterwards for new input    
    while True:  
        conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        var=arduino.readline()    
        var = var.decode('utf-8')
        var = var.replace('\n',"")
        print(repr(var))
        print(var)
        if(len(var) == 10):
            #print("NUMERO DE TELEMOVEL")
            #fazer o select
            tel_nmb_flag = TRUE

            if(tel_nmb_flag):   #Existe o numero na base de dados e esta valido
                #print("AQUI\n")
                if (var == '123456789\r'):
                    print("magic code")
                    code = '0000' + '\n'
                    arduino.write(code.encode()) #in case number is 123456789
                    
                    
                    # cur.execute("SELECT tenant_id, phone_number FROM tenant WHERE phone_number = '123456789' ")
                    # person = cur.fetchone()
                    
                    
                    # tenant_id, phone_number = person



                    entrou_erro = arduino.readline()  
                    entrou_erro = entrou_erro.decode('utf-8')
                    print (repr(entrou_erro))
                    if(entrou_erro == '1\r\n'):
                        print("vandalo")
                        envia_sms_admin(932667859)
                    else:
                        
                        
                        print("log")
                        #insert into logs the now time in format time.strftime in tenant_id = 3
                        cur.execute("INSERT INTO logs (tenant_tenant_id, log_date) VALUES (3, '" + time.strftime("%Y-%m-%d %H:%M:%S") + "')")

                        conn.commit()











                    

                else:
                    
                    
                    var.rstrip()
                    #select tenant_id, phone_number from tenant where phone_number = var and stay > now()
                    cur.execute("SELECT tenant_id, phone_number FROM tenant WHERE phone_number = '" + var + "' AND stay > now()")
                    person = cur.fetchone()
                    
                    
                    if(person is None):
                        arduino.write("$".encode())
                        envia_sms_admin(932667859)
                        

                    else:
                        tenant_id, phone_number = person
                        code = random_password() + '\n'
                        print(phone_number)
                        arduino.write(code.encode())
                        envia_sms(code, phone_number)
                        print(code)

                        entrou_erro = arduino.readline()  
                        entrou_erro = entrou_erro.decode('utf-8')
                        print (repr(entrou_erro))
                        if(entrou_erro == '1\r\n'):
                            print("vandalo")
                            envia_sms_admin(932667859)
                        else:
                            
                            
                            print("log")
                            cur.execute("INSERT INTO logs (tenant_tenant_id, log_date) VALUES (%s, %s)", (tenant_id, time.strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()
                    
        cur.close()
        conn.close()
                    
                


    # close the port and end the program    
    arduino.close()    


#define a function that creates a random password of lenght 4 using the characters "A,B,C,D,*,1,2,3,4,5,6,7,8,9,0"
def random_password():
    #create a list of characters
    characters = "ABCD*1234567890"
    #create a string of length 4
    password = ""
    #loop through 4 times
    for i in range(4):
        #get a random character from the list
        character = random.choice(characters)
        #add the character to the string
        password += character
    #return the string
    return password

#define a main function
def main():
    
    main_prog()


def envia_sms(code, num):
    # Your Account SID from twilio.com/console
    account_sid = "ACff24b35a0affafbf2d063bc460a8f4cf"
    # Your Auth Token from twilio.com/console
    auth_token  = "1d63de83e9ee60d56315b80872138248"

    num = '+351' + str(num)
    message = "Your unique code is: " + str(code) + "You have 3 tries."
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=num,
        from_="+19783893589",
        body=message)

    print(message.sid)

def envia_sms_admin(num):
    # Your Account SID from twilio.com/console
    account_sid = "ACff24b35a0affafbf2d063bc460a8f4cf"
    # Your Auth Token from twilio.com/console
    auth_token  = "1d63de83e9ee60d56315b80872138248"

    num = '+351' + str(num)
    message = "INTRUDER ALERT!! SOMEONE IS TRYING TO FORCE THE DOOR"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=num,
        from_="+19783893589",
        body=message)

    print(message.sid)


#run the main function
if __name__ == "__main__":
    main()



















