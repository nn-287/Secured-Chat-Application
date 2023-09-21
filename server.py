# Import required modules
import socket
import threading
import secrets
from tkinter import E
import DeffieHellman
import RSA
import hashlib


HOST = '192.168.1.3'

PORT = 1234 # to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

    
#Function to choose which security method to use
def chooseMethod():
    lst = ["DES","","RSA"]
    print("---------Welcome to our secure chat")
    print("1- DES (Data encryption standard)")

    print("3- RSA (Rivest–Shamir–Adleman)")
    num = input("Choose the encryption system: ")
    print(lst[int(num)-1] + " mode has been started")
    return num



def getMethod():
    return flagmethod




# Function to listen for upcoming messages from a client
def listen_for_messages(client, username,key,rsa_string):

    while 1:

        message = client.recv(2048).decode('utf-8')
        print("RECV : ",message)
        if message != '':
            ####### send
            final_msg = username + '~' + message + '~' + key + "~" +flagmethod+"~"+rsa_string
            send_messages_to_all(final_msg)
            print("rsaaaaaaa:   ",final_msg)

        else:
            print(f"The message send from client {username} is empty")



# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())
    print("SEND : ", message.encode() )




# Function to send any new message to all the clients that
# are currently connected to this server
    #####here
def send_messages_to_all(message):
    
    for user in active_clients:
        
        # Start the security phase using message then pass the message to client
        send_message_to_client(user[1], message)




# Function to handle client
def client_handler(client,key):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        print("KEY BOTHERING!!!!",key)
        print("RECV : ",username)
        if username != '':
            active_clients.append((username, client, key))

            #Random Secret Key !!!!# = Symmetric encryption DES
            # key = secrets.token_hex(8).upper()



            # hash_value = hashlib.sha256(key.encode()).digest()
            #
            # key = hash_value[:8]
            # key = key.hex().upper()
            print("key",key)




            ### RSA parameters ###
            #key of RSA Parameters 
            n,E,D=RSA.calc() 
            print("public and private key paramters: ")
            print("n: ",n)
            print("E: ",E)
            print("D: ",D)
            print("")
            print("")
            
            rsa_string=""

            rsa_string+=str(n)
            rsa_string+=","            
            rsa_string+=str(E)
            rsa_string+=","
            rsa_string+=str(D)
            rsa_string+=","


            



            #########send
            prompt_message = "SERVER~" + f"{username} added to the chat~" + key + "~" +flagmethod +"~"+rsa_string
            send_messages_to_all(prompt_message)
            
            print("Sessison key successfully generated for " + f"{username } ==>",key)

            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, key,rsa_string, )).start()





# Main function
def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Choose security method
    global flagmethod
    flagmethod = chooseMethod()
    

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
    
    
    #No. clients limited
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        key = ""
        # Perform Diffie-Hellman key exchange
        key = DeffieHellman.perform_key_exchange()
        key = int(key)
        key = format(key, '016x').upper()  # '016x' formats the number as 16 characters in hexadecimal
        threading.Thread(target=client_handler, args=(client,key, )).start()


if __name__ == '__main__':
    main()