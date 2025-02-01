import threading
import socket
import otp_generation
import account
import filemanage

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []
verification_flag = False
    
def close_client(client):
            index = clients.index(client)
            clients.pop(index)
            client.close()
            broadcast2(f'{nicknames[index]} has left the chat.'.encode('ascii'))
            nicknames.pop(index)
            
def broadcast2(message):
     for client in clients:
          client.send(message)

def broadcast1(message,index):
    nickname = nicknames[index]
    for client in clients:
        update_message = f'{nickname} : {message}'.encode('ascii')
        client.send(update_message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            
            if message == 'exit':
                close_client(client)
                break
            else:
                index = clients.index(client)
                broadcast1(message,index)
        except Exception as e:
            print(f'Error is {e}')
            close_client(client)
            break

def receive():
    while True:
        client,address = server.accept()
        print(f'{client} connected to {str(address)}')

        # i am changing from here
        user = client.recv(1024).decode('ascii')

        if user.lower()=="new":
            client_info = client.recv(1024).decode('ascii')
            while True:
                data = client_info.split(',')
                name = data[0]
                email = data[1]
                
                temp_flag = filemanage.check_unique(name,email)

                if temp_flag is True:
                    client.send('unique_user'.encode('ascii'))
                    gen_otp = otp_generation.send_otp(email)
                    client.send('OTP'.encode('ascii'))
                    check_otp = client.recv(1024).decode('ascii')
                    if str(gen_otp) == str(check_otp):
                        client.send('SUCCESS'.encode('ascii'))
                        password = client.recv(1024).decode('ascii')
                        hashed_password = account.create_password(password)
                        filemanage.insert_into_file(name,email,hashed_password)
                        client.send('SUCCESS'.encode('ascii'))
                        client.close()
                        break
                    else:
                         client.send('opt_fail'.encode('ascii'))
                         client.close()
                         continue
                else:
                    client.send('already_existed'.encode('ascii'))
                    client.close()
                    continue
                    
            continue

        else:
            credential = client.recv(1024).decode('ascii')
            credential_in_list = credential.split(',')  
            verification_flag = account.login_info(credential_in_list[0],credential_in_list[1])   #   this is verification check
            if  verification_flag is True:
                client.send('success'.encode('ascii'))
                nickname = credential_in_list[0]
                clients.append(client)
                nicknames.append(nickname)

                print(f'nickname of {client} is {nickname}')
                client.send(f'Connected to server as {nickname}\n'.encode('ascii'))
                broadcast2(f'{nickname} has joined the chat'.encode('ascii'))

                thread = threading.Thread(target=handle,args=(client,))
                thread.start()

            elif verification_flag == 'NO_USER':
                 client.send("no_user_found".encode('ascii'))
                 client.close()

            else:
                 client.send('invalid_credential'.encode('ascii'))
                 client.close()
                 

print('server is listening........')
receive()