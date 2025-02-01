# reading and writing into file

def insert_into_file(name,email,password):
    with open('credential.txt','+a') as credential:
        credential.write(f'{name},{email},{password}\n')  #   i have written the correct code i just need the correct format to save the file.
        return True

def readfile(user):
    stored_password =''
    with open('credential.txt','r') as credential:
        data = credential.readlines()
        # where the user matches the name return the pass
        for name in data:
            cred = name.strip().split(',')
            if cred[0] == user:
                stored_password = cred[2]
                return stored_password
    return "NO_USER"

def check_unique(username, email):
    names = []
    emails = []
    with open('credential.txt', 'r') as credential:
        data = credential.readlines()
        for line in data:
            line = line.strip()
            if not line:
                continue
            cred = line.split(',')
            if len(cred) == 3:
                names.append(cred[0])
                emails.append(cred[1])
    
    if username not in names and email not in emails:
        return True
    else:
        return False


def main():
    print()
if __name__=="__main__":
    main()