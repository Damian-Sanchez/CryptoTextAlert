import os
import requests
import boto3
from twilio.rest import Client
import json

def lambda_handler(event, context):
    
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
    MY_PHONE_NUMBER = os.environ['MY_PHONE_NUMBER']
    COIN_LAYER_API_TOKEN = os.environ['COIN_LAYER_API_TOKEN']
        
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Crypto')
        
    msg = ''
        
    for coin in ['BTC', 'DOGE', 'ETC', 'ETH']:
        response = table.get_item(
            Key={
            'Coin' : coin
            }
        )
        
        open_price = float(response['Item']['Price'])
        
        url = 'http://api.coinlayer.com/api/live?access_key={0}&target=usd&symbols={1}'.format(COIN_LAYER_API_TOKEN, coin)
        r = requests.get(url)
        data = r.json()
        live_price = float(data["rates"][coin])
        
        percent_change = str(round((live_price-open_price)/open_price*100, 2))
        
        msg += coin + ': $' + str("{:,}".format((round(live_price, 2)))) + ' (' + percent_change + '%)\n'
        
    client.messages.create(
        to=MY_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body= '.\n' + msg
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps("Damian's Second Lambda Function Works!")
    }
