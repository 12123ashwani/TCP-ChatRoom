import hashlib
import random
import filemanage

def login_info(nickname,password_given): #   this function is for account verification
    while True:
        user = nickname
        password = password_given
        try:
            hashed_pass = hashlib.sha256()
            hashed_pass.update(password.encode('ascii'))
            break
        except:
            print("you're password should be in ascii limits")
            return False
    extracted_pass = filemanage.readfile(user)   # check the password
    if extracted_pass == 'NO_USER':
        return "NO_USER"
    elif hashed_pass.hexdigest() == extracted_pass:   
        return True
    else:
        return False

def create_password(password):  #   this function is for password hash creation 
    while True:
        create_pass = password
        try:
            hashed_pass = hashlib.sha256()
            hashed_pass.update(create_pass.encode('ascii'))
            break
        except:
            print("you're password should be in ascii limits")   # this type of condition should be handled by the flag
            continue
        

    return hashed_pass.hexdigest()



def main():
    print("you're using the account.py library")
    print(login_info('oggy','password12'))
    
if __name__=="__main__":
    main() 