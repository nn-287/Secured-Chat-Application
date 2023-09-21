import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import DES_Decrypt
import DES_Encrypt
import RSA
import DeffieHellman

HOST = '192.168.1.3'


PORT = 1234

BLACK = '#000000'
OCEAN_BLUE = '#60a3bc'
WHITE = '#ffffff'
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)



def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        print("SEND : ", username.encode() )
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

        # Perform Diffie-Hellman key exchange
    key = DeffieHellman.perform_key_exchange()  # Use the function from diffie_hellman module

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    username_button.pack_forget()
    username_textbox.pack_forget()
    username_label['text']= "Welcome " + username + " to our secure room"
    username_label.pack(side=tk.LEFT)




def send_message():
    message = message_textbox.get()
    if message != '':
        message_textbox.delete(0, len(message))
        
        if flagMethod == 1:
            message = DES_Encrypt.startDesEncryption(message, key)


        elif flagMethod == 3:
            print("RSA encryption")
            global vo
            pla=[]
            global mes
            mes = []
            pla,mes=RSA.preprocess_message(message,int(rsa_string[0]))
            print("mes:",mes)
            message =RSA.to_cipher(int(rsa_string[1]),int(rsa_string[0]),pla)
            message = [str(x) for x in message]
            message = ",".join(message)
            print("msg type:",type(message))
            print("cipher RSA : ",message)

        client.sendall(message.encode("utf-8"))
        # client.sendall(f"{message.encode('utf-8')}~{str(flagMethod)}~{','.join(rsa_string)}".encode("utf-8"))

        print("SEND : ", message.encode() )
        
        print("This message has been delivered")
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")





def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        print("RECV : ", message)
        
        if message != '':
            message = message.split("~")
            global key,flagMethod,rsa_string

            username = message[0]
            content = message[1]
            key = message[2]
            flagMethod = int(message[3])

            rsa_string=message[4]
            rsa_string = rsa_string.split(",")

            if username != "SERVER":
                if flagMethod == 1:
                    content = DES_Decrypt.startDesDecryption(content, key)
                    try:
                        content = bytes.fromhex(content).decode('utf-8','ignore')
                    except:
                        print("error")



                elif flagMethod == 3:
                    content = content.split(",")
                    content = [int(x) for x in content]
                    content = RSA.to_plain(int(rsa_string[2]),int(rsa_string[0]),content, mes)
                    print("RSA Done:",content)

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message received from the client is empty")




def DES_Encryption(pt, key):
    cipher = DES_Encrypt.startDesEncryption(pt,key)  
    return cipher



root = tk.Tk()
root.geometry("600x600")
root.title("What's app Secured Chat")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=WHITE)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=WHITE)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=WHITE)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Nickname:", font=FONT, bg=WHITE, fg=BLACK)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=WHITE, fg=BLACK, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=WHITE, fg=BLACK, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=WHITE, fg=BLACK, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def main():
    root.mainloop()
    
if __name__ == '__main__':
    main()
