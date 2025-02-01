import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_event = threading.Event()

def receive():
    while not stop_event.is_set():
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send('there will be some code and logic here'.encode('ascii'))
            elif message == '':
                # Server closed connection
                print('Server has closed the connection.')
                stop_event.set()
                break
            else:
                print(message)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            print('Connection closed by the server.')
            stop_event.set()
            break
        except Exception as e:
            print(f'An error occurred: {e}')
            client.close()
            stop_event.set()
            break

def write():
    while not stop_event.is_set():
        try:
            message = input()
            if message.lower() == 'exit':
                client.send('exit'.encode('ascii'))
                stop_event.set()
                client.close()
                break
            client.send(message.encode('ascii'))
        except (EOFError, ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            print('Connection closed by the server.')
            stop_event.set()
            break
        except Exception as e:
            print(f'An error occurred: {e}')
            client.close()
            stop_event.set()
            break


def call():
    receive_thread = threading.Thread(target=receive, daemon=True)
    receive_thread.start()
    send_thread = threading.Thread(target=write, daemon=False)
    send_thread.start()

    try:
        while send_thread.is_alive():
            send_thread.join(timeout=1)  # Join with a timeout to periodically check for KeyboardInterrupt
    except KeyboardInterrupt:
        print('KeyboardInterrupt received, closing client...')
        stop_event.set()  # Signal the threads to stop
        client.close()
        receive_thread.join(timeout=1)
        send_thread.join(timeout=1)
        print('Client closed.')


while True: 
    # client.connect(('127.0.0.1', 55555))
    about_user = int(input('enter new_user(1)\nexisting user(2)\n'))
    if about_user == 1:
        client.send('new'.encode('ascii'))
        username = input('enter your username it should be unique : ')
        email = input('enter your email for verification \n it should be unique :   ')
        # i have to add email verification here.........................................................
        data_upload = f'{username},{email}'.encode('ascii')
        print(10*'.', 'wait patiently while server is working',10*'.')
        client.send(data_upload)
        
        #  here's the problem.
        flag_check = client.recv(1024).decode('ascii')
        if flag_check=='unique_user':
            asking_otp = client.recv(1024).decode('ascii')
            if asking_otp == 'OTP':
                user_otp = input('enter the verification code')
                client.send(user_otp.encode('ascii'))
            result = client.recv(1024).decode('ascii') 
            if result == 'SUCCESS':
                print("your name and password should contain only english alphabets and special charaters")
                while True:
                    create_pass = input("enter the password : ")
                    verify_pass = input("please verify the password :")
                    if create_pass==verify_pass:
                        try:
                            client.send(create_pass.encode('ascii'))
                            break
                        except:
                            print('your password should be in ascii limits')
                    else:
                        print('password doesn\'t matched please try again \n')
                        continue

                client.recv(1024).decode('ascii')
                print('your account has been created now select the option 2 and login')
                continue
            else:   
                print(result)
                client.close()
              
        else:
            print(flag_check)
            print('user is not unique try again')
            client.close() 
            break
    elif about_user == 2:
        client.send('existing'.encode('ascii')) # server line 86 error referring to this
        name = input("enter your username :  ")
        password = input('enter you password :  ')
        cred = f'{name},{password}'
        client.send(cred.encode('ascii'))
        print(10*'.','wait patiently while server is working',10*'.')
        result = client.recv(1024).decode('ascii') 
        if result == 'success':
            print('you have logged-in now you can chat')
            call()
            print('looks like you\'re done for now')
            break
        else:
            print(result)
            message = client.recv(1024).decode('ascii')
            if message == '':
                # Server closed connection
                print('Server has closed the connection.')
            break
    else:
        print('invalid user select the correct option ')
        continue

# ////////////////////////////////rest of the code here////////////////////////////////////
