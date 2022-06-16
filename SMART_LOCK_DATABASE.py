import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import stdiomask

#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#==========================================================================================================================

utilizador_atual = 0            #ID Utilizador com login efetuado
nome_utilizador_atual = ""      #NOME Utilizador com login efetuado

#Início/Ecrã inicial
def inicio():
    atualizar_estadia()
    while True:
        try:
            print("""\n\t\t  || Smart Lock ||\n
                          1 - Login\n
                          2 - Logout""")

            #Escolha da ação a tomar
            inicio_escolha = int(input("\n\t\t\t      "))
            if (inicio_escolha == 1):       #Login
                login()
                #Escolher casa
                print("\n\tYour Homes: ")
                cur.execute(f"SELECT address FROM home where admin_id = {utilizador_atual}")
                home = cur.fetchone()
                print(home)
                home_choice = input("\n\t Choose a home: ")

                try:
                    try:
                        cur.execute(f"SELECT address from home where address = '{home_choice}';")
                        detalhes = cur.fetchone()
                        if detalhes is None:
                            print(f"There's no home with the name {home_choice}")
                        else:
                            print("\n\n\t\t  Acepted\n")
                            break
                    except:
                        print("ERROR!")
                except ValueError:
                    print("VALOR INVÁLIDO")                  

                menu_admin()

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
    print("\n================================================================")
    print("\n|                             LOGIN                            |")
    print("\n================================================================")
    while True:
        username = input("\n\t\t\t || Username ||\n\t\t    ")
        cur.execute(f"SELECT COUNT(username) FROM admin WHERE admin_name LIKE '%{username}' AND admin_name LIKE '{username}%'")
        username_verif = cur.fetchone()
        if (username_verif[0]==1):
            while True:
                password = stdiomask.getpass("\n\t\t        || Password ||\n\t\t\t   ")
                cur.execute(f"SELECT password FROM admin WHERE username LIKE '%{username}' AND username LIKE '{username}%'")
                password_verif = cur.fetchone()
                if(sha256_crypt.verify(password ,password_verif[0])):
                    print("\n\t         Welcome\n")
                    cur.execute(f"SELECT admin_id, admin_name FROM admin WHERE admin_name LIKE '%{username}' AND admin_name LIKE '{username}%'")
                    dados = cur.fetchone()
                    global utilizador_atual
                    global nome_utilizador_atual
                    utilizador_atual, nome_utilizador_atual = dados
                    break
                else:
                    print(f"\nWrong Password")
            break
        else:
            print("\nWrong Username!")

    return




#==========================================================================================================================
#Atualizar validade das estadias
def atualizar_estadia():
    cur.execute(f"SELECT stay, tenant_id, FROM tenant WHERE ativo = true")
    for linha in cur.fetchall():
        data = linha[0]
        id = linha[1]
        #periodo = linha[2]
        #validade = data + relativedelta(months =+ periodo)
        if(date.today() > data.date()):
            try:
                cur.execute(f"UPDATE tenant SET ativo = false WHERE id = id")
                conn.commit()
            except:
                conn.rollback()

    return
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                               ADMIN
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Menu ADMIN
def menu_admin():
    atualizar_estadia()
    while True:
        print("\n-------------------------------------ADMIN MENU-----------------------------------------------\n")

        escolha_admin = input("""
                              1 - Unlock door
                              2 - View all clients
                              3 - Add Client
                              4 - Change Client's stay date
                              5 - View log of locks
                              6 - Logout 

        Ver: """)

        if escolha_admin == "1":
            

        elif escolha_admin == "2":
            

        elif escolha_admin == "3":
            

        elif escolha_admin == "4":
            

        elif escolha_admin == "5":
            

        elif escolha_admin == "6":
            print("LOGOUT")
            return

        else:
            print("Invalid\nTry again")


#==========================================================================================================================
#Iniciar programa
inicio()


#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
