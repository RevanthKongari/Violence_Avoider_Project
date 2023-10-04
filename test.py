import os
from twilio.rest import Client
import PSReadLine


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['AC01fee5996d1961875ed87ed607e33304']
auth_token = os.environ['b914bcf3ee14e1ee3932599912f976dd']
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         media_url=['C:\Users\Rajesh\Dropbox\My PC (DESKTOP-D8Q1STA)\Desktop\project\recording1.wav'],
         from_='whatsapp:+916300834419',
         to='whatsapp:+918074756457'
     )

print(message.sid)