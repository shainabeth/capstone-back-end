import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

def lambda_handler(event, context):
    print(json.dumps(event))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    phase_table = dynamodb.Table(os.environ['PHASE_TABLE_NAME'])
    if event['rawPath'] == '/api/add_task':
        return add_task(table, event)
    elif event['rawPath'] == '/api/delete_task':
        return delete_task(table, event)
    elif event['rawPath'] == '/api/list_tasks':
        return list_tasks(table, event)
    elif event['rawPath'] == '/api/update_task_completion_date':
        return update_task_completion_date(table, event)
    elif event['rawPath'] == '/api/update_task_name':
        return update_task_name(table, event)
    elif event['rawPath'] == '/api/start_cycle':
        return start_cycle(phase_table, event)
    elif event['rawPath'] == '/api/get_cycle_info':
        return get_cycle_info(phase_table, event)
    elif event['rawPath'] == '/api/update_task_completion_date':
        return update_task_completion_date(table, event)
    return {
        'statusCode': 404,
        'body': json.dumps('not found')
    }

def add_task(table, event):
    response = table.put_item(
        Item={
            'user': event['queryStringParameters']['user'],
            'task_id': event['queryStringParameters']['task_id'],
            'task_name': event['queryStringParameters']['task_name'],
            'phase': event['queryStringParameters']['phase']
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('added task successfully')
    }

def delete_task(table, event):
    response = table.delete_item(
        Key={
            'user': event['queryStringParameters']['user'],
            'task_id': event['queryStringParameters']['task_id'],
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('added deleted successfully')
    }

def list_tasks(table, event):
    response = table.query(
        KeyConditionExpression=Key('user').eq(event['queryStringParameters']['user']),
        FilterExpression=Attr('phase').eq(event['queryStringParameters']['phase'])
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }

def start_cycle(table, event):
    response = table.put_item(
        Item={
            'user': event['queryStringParameters']['user'],
            'date': event['queryStringParameters']['date'],
            'duration': event['queryStringParameters']['duration'],
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('phase started successfully')
    }

def get_cycle_info(table, event):
    response = table.get_item(
        Key={
            'user': event['queryStringParameters']['user'],
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'])
    }

def update_task_completion_date(table, event):
    response = table.update_item(
        Key={
            'user': event['queryStringParameters']['user'],
            'task_id': event['queryStringParameters']['task_id'],
        },
        UpdateExpression="set last_completed_date=:d",
        ExpressionAttributeValues={
            ':d': event['queryStringParameters'].get('last_completed_date'),
        },
    )
    return {
        'statusCode': 200,
        'body': json.dumps('updated successfully')
    }

def update_task_name(table, event):
    response = table.update_item(
        Key={
            'user': event['queryStringParameters']['user'],
            'task_id': event['queryStringParameters']['task_id'],
        },
        UpdateExpression="set task_name=:n",
        ExpressionAttributeValues={
            ':n': event['queryStringParameters']['task_name'],
        },
    )
    return {
        'statusCode': 200,
        'body': json.dumps('updated successfully')
    }   