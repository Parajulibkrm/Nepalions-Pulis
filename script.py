from fbchat import Client,log
from fbchat.models import *
import json,apiai

thread_id = 'group_id'
# thread_type = ThreadType.GROUP
email = 'your email'
password = 'password'

#extending the class Client imported from fbchat
class nepalionsBot(Client):
    #apiai method for setting up connection and getting the reply.
    def apiai(self):
        self.ClientAccessToken = 'XXXXXXXXXXXXXX'
        self.ai = apiai.ApiAI(self.ClientAccessToken)
        self.request = self.ai.text_request()
        self.request.lang = 'en'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    #modifying pre defined method onMessage, where author_id is the sender id, thread_id is the id of the chatbox or the
    #  thread and thread_type is weather its personal chat or group chat.
    def onFriendRequest(self,from_id=None, msg=None):
    	print(type(from_id))
    	reply = 'hello'
    	self.sendMessage(reply, thread_id = from_id, thread_type = ThreadType.USER)
    def onMessage(self, author_id, message_object,message,thread_id, thread_type, **kwargs):
        mero = str(message_object.mentions)
        mero = mero[10:24]
        print(mero)
        if author_id =="XXXXXXXXXX":
            client.reactToMessage(message_object.uid, MessageReaction.LOVE)
        if mero == 'XXXXXXXXXXXXXXX' or thread_type == ThreadType.USER:
            #marking the message as read
            self.markAsRead(author_id)
            #printing to terminal as a message is received.
            log.info("Message {} from {} in {}".format(message,thread_id,thread_type))
            #printing message text
            print("The received message - ",message)
            msg = message
            msg = msg.replace('@Nepalions Pulis','')
            msg = msg.replace('@Nepalions Police','')
            try:
                #setting up connection with apiai
                self.apiai()
                #sending the query (message received)
                self.request.query = msg
                #getting the json response
                api_response = self.request.getresponse()
                json_reply = api_response.read()
                #decoding to utf-8 (converting byte object to json format)
                decoded_data = json_reply.decode("utf-8")
                #loading it into json
                response = json.loads(decoded_data)
                #taking out the reply from json
                reply = response['result']['fulfillment']['speech']
            except Exception as e:
                print(e)
                reply = "Yes, Please?"

            #if we are not the sender of the message
            if author_id!=self.uid:
                #sending the message.
                self.sendMessage(reply, thread_id = thread_id, thread_type = thread_type)

            self.markAsDelivered(author_id,thread_id)

print(email,password)
#logging into facebook.(importing email and password from credentials file.)
client = nepalionsBot(email,password)
#listen for incoming message
client.listen()
