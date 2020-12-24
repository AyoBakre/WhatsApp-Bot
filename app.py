from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chat import fetch_reply


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/sms", methods=['POST'])
def sms_reply():

    # Fetch the incoming message
    msg = request.form.get('Body')
    phone_no = request.form.get('From')

    # Creates a reply
    resp = MessagingResponse()
    reply = fetch_reply(msg, phone_no)

    # Sends a reply
    resp.message(reply)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
