from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chat import fetch_reply
import requests
import bs4


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/sms", methods=['POST'])
def sms_reply():

    # Fetch the message
    msg = request.form.get('Body')
    phone_no = request.form.get('From')

    # Create reply
    resp = MessagingResponse()

    # if msg.lower().startswith()

    # resp.message()

    # resp.message().media(movie_img_url)

    reply = fetch_reply(msg, phone_no)
    resp.message(reply)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)