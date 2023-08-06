# -*- coding: utf-8 *-*
import sys
import logging
import time
import traceback
import boto3
from datetime import datetime

if sys.version_info[0] >= 3:
    unicode = str

class DynamoFormatter(logging.Formatter):
    def format(self, record):
        data = record.__dict__.copy()
        if record.args:
            msg = record.msg % record.args
        else:
            msg = record.msg
        data.update(
            args=str([unicode(arg) for arg in record.args]),
            message=str(msg),
        )

        # Remove empty keys from the dictionary
        data = dict((k, v) for k, v in data.items() if v)

        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])

        data['bill'] = record.args[0]
        return data


class DynamoHandler(logging.Handler):
    """ Custom log handler
    Logs all messages to a Dynamo table. This handler is designed to be used with the standard python logging mechanism.
    """

    @classmethod
    def to(cls, table_name, aws_region, level=logging.NOTSET):
        """ Create a handler for a given  """
        return cls(table_name, aws_region, level)

    def __init__(self, table_name, aws_region, level=logging.NOTSET):
        """ Init log handler and store the table handle """
        logging.Handler.__init__(self, level)

        dynamodb = boto3.resource('dynamodb', region_name=aws_region)

        try:
            self.table = dynamodb.Table(table_name)
        except:
            traceback.print_exc()

        self.formatter = DynamoFormatter()

    def emit(self, record):
        """ Store the record in the table. Async insert """
        try:

            formatted_record = self.format(record)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.table.put_item(
                Item={
                    'timestamp': now,
                    'module': formatted_record['name'],
                    'level': formatted_record['levelname'],
                    'message': formatted_record['message'],
                    'factura': formatted_record['bill'],
                }
            )
        except:
            traceback.print_exc()