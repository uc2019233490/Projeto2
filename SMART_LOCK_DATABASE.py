from time import sleep
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

#==========================================================================================================================

utilizador_atual = 0            #ID Utilizador com login efetuado
nome_utilizador_atual = ""      #NOME Utilizador com login efetuado

#Início/Ecrã inicial
def main():
    clear()
    #update_stay()
    while True:
        conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            print("""\n\t\t  || Smart Lock ||\n
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
                    print(homeID)
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

#create a function that compares timestamap to current time and sets ativo to false if date is in the past
def update_active(homeID):
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM tenant WHERE home_home_id = {homeID}")
    for linha in cur.fetchall():
        id, name, stay, number, active, home_id = linha
        if(active == True):
            if(stay < date.today()):
                cur.execute(f"UPDATE tenant SET active = False WHERE id = {id}")
                conn.commit()
    cur.close()
    conn.close()
    return
    
#compare now time to time of stay and set ativo to false if date is in the past
def update_active(homeID):
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM tenant WHERE home_home_id = {homeID}")
    for linha in cur.fetchall():
        id, name, stay, number, active, home_id = linha
        if(active == True):
            if(stay < date.today()):
                cur.execute(f"UPDATE tenant SET active = False WHERE id = {id}")
                conn.commit()
    cur.close()
    conn.close()
    return





#function to upadate time of stay
def update_stay(homeID):
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM tenant WHERE home_home_id = {homeID}")
    for linha in cur.fetchall():
        id, name, stay, number, active, home_id = linha
        if(active == True):
            stay = stay + relativedelta(months =+ 1)
            cur.execute(f"UPDATE tenant SET stay = '{stay}' WHERE id = {id}")
            conn.commit()   #commit the changes 
                                                                    
#==========================================================================================================================
#Login
def login():
    clear()
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
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
# #Atualizar validade das estadias
# def atualizar_estadia():
#     conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
#     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cur.execute(f"SELECT stay, tenant_id, FROM tenant WHERE ativo = true")
#     for linha in cur.fetchall():
#         data = linha[0]
#         id = linha[1]
        
#         #periodo = linha[2]
#         #validade = data + relativedelta(months =+ periodo)
#         if(date.today() > data.date()):
#             try:
#                 cur.execute(f"UPDATE tenant SET ativo = false WHERE id = id")
#                 conn.commit()
#             except:
#                 conn.rollback()
#     cur.close()
#     conn.close()
#     return

def view_clients(homeID):
    clear()
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM tenant WHERE home_home_id = {homeID}")
    for linha in cur.fetchall():
        id, name, stay, number, active, home_id = linha
        print(name + ' with phone number: ' + str(number) + ' is staying until ' + str(stay))
    cur.close()
    conn.close()
    return

def add_client(homeID):
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    tenant_name = input("\n\t\t        || Name ||\n\t\t\t   ")
    tenant_phone = input("\n\t\t        || Phone ||\n\t\t\t   ")
    tenant_stay = input("\n\t\t        || Stay ||\n\t\t\t   ")
    print(f"INSERT INTO tenant (tenant_nome, phone_number, stay, home_home_id, ativo) VALUES ('{tenant_name}', '{tenant_phone}', '{tenant_stay}', {homeID}," + "'TRUE')")
    cur.execute(f"INSERT INTO tenant (tenant_nome, phone_number, stay, home_home_id, ativo) VALUES ('{tenant_name}', '{tenant_phone}', '{tenant_stay}', {homeID}," + "'TRUE')")
    conn.commit()
    cur.close()
    conn.close()
    return

def edit_client(homeID):
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
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
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT tenant_nome, log_date FROM tenant, logs WHERE tenant_id = tenant_tenant_id")
    for linha in cur.fetchall():
        name, log = linha
        print(name + ' - ' + str(log))
    cur.close()
    conn.close()
    return






#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                               ADMIN
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Menu ADMIN
def menu_admin(IDadmin, homeID):
    conn = psycopg2.connect("host=localhost dbname='Smart Lock' user=postgres password=password")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    clear()
    #atualizar_estadia()
    while True:
        print("\n-------------------------------------ADMIN MENU-----------------------------------------------\n")

        escolha_admin = input("""
                              1 - Unlock door
                              2 - View all clients
                              3 - Add Client
                              4 - Change Client's stay date
                              5 - View log of locks
                              6 - Logout 

        Choose: """)

        if escolha_admin == "1":
            cur.close()
            conn.close()
            continue

        elif escolha_admin == "2":
            view_clients(homeID)
            cur.close()
            conn.close()
            continue

        elif escolha_admin == "3":
            add_client(homeID)
            cur.close()
            conn.close()
            continue

        elif escolha_admin == "4":
            edit_client(homeID)
            cur.close()
            conn.close()
            continue

        elif escolha_admin == "5":
            view_logs()
            cur.close()
            conn.close()
            continue

        elif escolha_admin == "6":
            print("LOGOUT")
            cur.close()
            conn.close()
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
