""" this code will generate a otp and send this to specified email for email verification """
import random
import smtplib

sending = smtplib.SMTP('smtp.gmail.com',587)
sending.starttls()   #    tls is transport layer security here
sending.login('mail','app code')    #   write  your own


def generate_otp():
    otp = random.randint(100000,999999)
    return otp

def send_otp(email):
    otp = generate_otp()
    sender_gmail = 'mail'   #   write your own
    sending.sendmail(sender_gmail,email,f'the otp for verification is {otp} \n do not share it with anyone except for verification..')
    # send this otp to the specified mail address
    return otp
def main():
    email = '12123ashwani@gmail.com'
    send_otp(email)
    print('this is sending otp')
if __name__== "__main__":
    main()