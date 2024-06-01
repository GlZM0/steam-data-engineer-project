import boto3
import pandas as pd
from datetime import datetime
from item_processor import ItemProcessor
from botocore.exceptions import ClientError
import logging

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    dict_list = []
    item_list = []

    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode()
    
    df = pd.read_json(data)
    
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        dict_list.append(row_dict)

    for item_data in dict_list:
        for key, item_dict in item_data.items():
            if item_dict is not None:
                name = item_dict.get("name")
                sell_price_text = item_dict.get("sell_price_text")
                if name is not None and sell_price_text is not None:
                    logger.info(f"Processing item: {name} - {sell_price_text}")
                    item = ItemProcessor.process_item_data(item_dict)
                    color = ItemProcessor.categorize_item_type(item.type)
                    color_hex = ItemProcessor.add_skin_hex_color(color)
                    condition = ItemProcessor.set_condition(item)

                    refined_item = {
                        "name": item.name,
                        "condition": condition,
                        "price": item.price,
                        "image": item.imageURL,
                        "type": item.type,
                        "color": color,
                        "colorHex": color_hex
                    }
                    item_list.append(refined_item)

    output_path = f'/tmp/cs2_items_transformed_{current_datetime}.csv'
    df = pd.DataFrame(item_list)
    df.to_csv(output_path, sep=';', index=False)

    try:
        s3.upload_file(output_path, bucket, f'transformed_data/cs2_items_transformed_{current_datetime}.csv')
    except ClientError as e:
        logger.error(e)
        return {'statusCode': 500, 'body': 'Error uploading file'}

    return {'statusCode': 200, 'body': 'File processed and uploaded successfully'}