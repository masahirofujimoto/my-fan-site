import json
import boto3
import decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Posts')
    
    try:
        response = table.scan()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # CORSヘッダー
                'Access-Control-Allow-Methods': 'GET, OPTIONS',  # 必要に応じて設定
                'Access-Control-Allow-Headers': 'Content-Type'  # 必要に応じて設定
            },
            'body': json.dumps(response['Items'], cls=DecimalEncoder)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # CORSヘッダー
                'Access-Control-Allow-Methods': 'GET, OPTIONS',  # 必要に応じて設定
                'Access-Control-Allow-Headers': 'Content-Type'  # 必要に応じて設定
            },
            'body': json.dumps({'error': str(e)})  # エラーメッセージを適切に設定
        }

