import time
import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os
import datetime
from datetime import date
#from dateutil.relativedelta import relativedelta
import stdiomask
import hashlib
from datetime import datetime

#==========================================================================================================================

utilizador_atual = 0            #ID Utilizador com login efetuado0
nome_utilizador_atual = ""      #NOME Utilizador com login efetuado

#Início/Ecrã inicial
def main():
    clear()
    #atualizar_estadia()
    while True:
        conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            print("""\n|| Smart Lock ||\n
                          1 - Login\n
                          2 - Logout""")

            #Escolha da ação a tomar
            inicio_escolha = int(input("\n\t\t\t      "))
            if (inicio_escolha == 1):       #Login
                IDadmin = login()                                      #ID do admin com login efetuado
               
               #Escolher casa
                
                print("\n\tYour Homes: ")

                cur.execute("SELECT home_name, address FROM home where admin_admin_id = " + str(IDadmin))
                homes = cur.fetchall()
                for home in homes:
                    name, address = home
                    #[home] = home
                    print(name + '---' +address)
                home_name_choosen = input("\n\t Choose a home: ")

                cur.execute("SELECT home_id FROM home where home_name = " + "'" + home_name_choosen + "'")

                homeID = cur.fetchone()
                if homeID is None:
                    print("\n\t\t  || Home not found ||")
                    exit()
                else:
                    [homeID] = homeID
                    #print(homeID)
                    cur.close()
                    conn.close()
                    menu_admin(IDadmin, homeID)

                

            elif(inicio_escolha == 2):      #Sair
                return
            else:
                print("")
        #Se não for introduzido um número
        except ValueError:
            print("")

#==========================================================================================================================
#Login
def login():
    clear()
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("\n================================================================")
    print("\n|                             LOGIN                            |")
    print("\n================================================================")
    while True:
        username = input("\n\t\t        || Username ||\n\t\t\t   ")
        password = stdiomask.getpass("\n\t\t        || Password ||\n\t\t\t   ")
        password = enc_password(password)
        
        cur.execute("SELECT admin_id FROM admin WHERE username = " + "'" + username + "'" + "AND password = " + "'" + password + "'")
        username_verif = cur.fetchone()
        if username_verif is None:
            print("\n\t\t  || Username or Password incorrect ||")
        else:
            [username_verif] = username_verif
            #print(username_verif)
            print("\n\t         Welcome\n")
            break

    cur.close()
    conn.close()
    return username_verif




#==========================================================================================================================
#crerate a function that checks the current date and time and compares it to the stay date and time and sets ativo to false if the stay date and time is passed and ativo is true
def atualizar_estadia():
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM tenant")
    for linha in cur.fetchall():
        id, name, stay, number, active, home_id = linha
        #if stay has passed set active to false and update the database else set active to true and update the database 
        if stay < datetime.now():
            active = False
            cur.execute(f"UPDATE tenant SET ativo = '{active}' WHERE tenant_id = {id}")
            conn.commit()
        else:
            active = True
            cur.execute(f"UPDATE tenant SET ativo = '{active}' WHERE tenant_id = {id}")
            conn.commit()


    cur.close()
    conn.close()
    return


def view_clients(homeID):
    clear()
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #active clients
    cur.execute(f"SELECT tenant_id, tenant_nome, phone_number, stay, ativo FROM tenant WHERE home_home_id = {homeID} AND ativo = 'TRUE'")
    print("\n\t\t  || Active clients ||")
    for linha in cur.fetchall():
        id, nome, phone, stay, ativo = linha
        print(f"\n\t\t\t{nome} --- {phone} --- {stay} --- {ativo}")
    #inactive clients
    cur.execute(f"SELECT tenant_id, tenant_nome, phone_number, stay, ativo FROM tenant WHERE home_home_id = {homeID} AND ativo = 'FALSE'")
    print("\n\t\t  || Inactive clients ||")
    for linha in cur.fetchall():
        id, nome, phone, stay, ativo = linha
        print(f"\n\t\t\t{nome} --- {phone} --- {stay} --- {ativo}")
    cur.close()
    conn.close()
    return




    # cur.execute(f"SELECT * FROM tenant WHERE home_home_id = {homeID}")
    # for linha in cur.fetchall():
    #     id, name, stay, number, active, home_id = linha
    #     print(name + ' with phone number: ' + str(number) + ' is staying until ' + str(stay))
    # cur.close()
    # conn.close()
    # return

def add_client(homeID):
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    tenant_name = input("\n\t\t        || Name ||\n\t\t\t   ")
    tenant_phone = input("\n\t\t        || Phone ||\n\t\t\t   ")
    tenant_stay = input("\n\t\t        || Stay ||\n\t\t\t   ")
    #print(f"INSERT INTO tenant (tenant_nome, phone_number, stay, home_home_id, ativo) VALUES ('{tenant_name}', '{tenant_phone}', '{tenant_stay}', {homeID}," + "'TRUE')")
    cur.execute(f"INSERT INTO tenant (tenant_nome, phone_number, stay, home_home_id, ativo) VALUES ('{tenant_name}', '{tenant_phone}', '{tenant_stay}', {homeID}," + "'TRUE')")
    conn.commit()
    cur.close()
    conn.close()
    return

def edit_client(homeID):
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    view_clients(homeID)
    client_choosen = input("\n\t\t        ||Which client to edit the date of stay ||\n\t\t\t   ")
    tenant_stay = input("\n\t\t        || New date of stay ||\n\t\t\t   ")
    cur.execute(f"UPDATE tenant SET stay = '{tenant_stay}' WHERE tenant_nome = '{client_choosen}'")
    conn.commit()
    cur.close()
    conn.close()
    return
          

def view_logs():
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT tenant_nome, log_date FROM tenant, logs WHERE tenant_id = tenant_tenant_id")
    for linha in cur.fetchall():
        name, log = linha
        print(name + ' - ' + str(log))
    cur.close()
    conn.close()
    return

def unlock_door(homeID):
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT unlock_door FROM home WHERE home_id = {homeID}")
    [unlock_door] = cur.fetchone()
    #print(unlock_door)
    cur.execute(f"UPDATE home SET unlock_door = 'TRUE' WHERE home_id = {homeID}")
    #insert log entry in logs with the name "REMOTE_UNLOCK"
    cur.execute("INSERT INTO logs (tenant_tenant_id, log_date) VALUES (%s, %s)", (6, time.strftime("%Y-%m-%d %H:%M:%S")))    
    conn.commit()
    return







#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                               ADMIN
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Menu ADMIN
def menu_admin(IDadmin, homeID):
    conn = psycopg2.connect(host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com", database = "d4q1906fsmaeht", user="jyclbaeqmpmkww", password="bd28c3d7fc26813a45863e897681ba070ab401cb2f6c69f27f0ba3635fbfb0c5", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("select admin_nome from admin where admin_id = " + str(IDadmin))
    [idname] = cur.fetchone()
    


    while True:
        clear()
        print("\n-------------------------------------ADMIN MENU-----------------------------------------------\n")
        print("YOU ARE LOGGED AS " + str(idname))
        atualizar_estadia()

        escolha_admin = input("""
                              1 - Unlock door
                              2 - View all clients
                              3 - Add Client
                              4 - Change Client's stay date 
                              5 - View log of locks
                              6 - Logout 

        CHOOSE: """)

        if escolha_admin == "1":
            unlock_door(homeID)
            cur.close()
            conn.close()
            input('PRESS ANY KEY TO CONTINUE...')
            continue

        elif escolha_admin == "2":
            view_clients(homeID)
            cur.close()
            conn.close()
            input('PRESS ANY KEY TO CONTINUE...')
            continue

        elif escolha_admin == "3":
            add_client(homeID)
            cur.close()
            conn.close()
            input('PRESS ANY KEY TO CONTINUE...')
            continue

        elif escolha_admin == "4":
            edit_client(homeID)
            cur.close()
            conn.close()
            input('PRESS ANY KEY TO CONTINUE...')
            continue

        elif escolha_admin == "5":
            view_logs()
            cur.close()
            conn.close()
            input('PRESS ANY KEY TO CONTINUE...')
            continue

        elif escolha_admin == "6":
            print("LOGOUT")
            cur.close()
            conn.close()
            input('PRESS ANY KEY TO CONTINUE...')
            return

        else:
            print("Invalid\nTry again")
    


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def enc_password(password):
    result = hashlib.md5(password.encode())
    result = hashlib.sha256(result.hexdigest().encode())
    return (result.hexdigest())

#run the main function
if __name__ == "__main__":
    #print(enc_password("admin123"))
    main()
