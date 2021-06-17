import os
import requests
import boto3
import json

def lambda_handler(event, context):

    COIN_LAYER_API_TOKEN = os.environ['COIN_LAYER_API_TOKEN']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Crypto')
    
    for coin in ['BTC', 'DOGE', 'ETC', 'ETH']:
        url = "http://api.coinlayer.com/api/live?access_key={0}&target=usd&symbols={1}".format(COIN_LAYER_API_TOKEN, coin)
        r = requests.get(url)
        data = r.json()
        open_price = str(data["rates"][coin])
    
        table.update_item(
            Key={
            'Coin' : coin
            },
            UpdateExpression='SET Price = :vall',
            ExpressionAttributeValues={
                ':vall': open_price
            }
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps("Damian's Lambda Function Works!")
    }
