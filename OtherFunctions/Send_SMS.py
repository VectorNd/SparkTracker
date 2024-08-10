#importing twilio client

from twilio.rest import Client
#Taking Account SID and authentication token from twilio.com

def send_sms(name, product, price, number):
    account_sid = 'AC11a3758bf35c56fd87f2be8f5a6f8d8a'
    auth_token = ''

    client = Client(account_sid, auth_token)
    #Writing a message
    message = client.messages.create(
        from_= '+14124538097',
        to = '+919084485193',
        body = '\nHi ' + name + ' your product ' + ' '.join(product.split()[0:5]) + ' ...has come down to price of ' + str(price) + '. ' + 'Please check email for url.' + '\nDO NOT REPLY'
    )   

    print('SMS sent to: ', number)
