import os, json, uuid, datetime as dt
import boto3

# Initialize the table client once per container
TABLE = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    # Basic validation
    if not body.get("name") or not body.get("dateOfBirth"):
        return {"statusCode": 400, "body": json.dumps({"message":"name & dateOfBirth required"})}

    child_id = str(uuid.uuid4())
    item = {
        "id": child_id,
        "name": body["name"],
        "dateOfBirth": body["dateOfBirth"],
        "createdAt": dt.datetime.utcnow().isoformat()
    }
    # **persist** to DynamoDB
    TABLE.put_item(Item=item)

    return {
        "statusCode": 201,
        "body": json.dumps(item)
    }
