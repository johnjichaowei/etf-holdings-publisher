from .holding_schema import HoldingSchema
import src.holdings_repository
import src.sns_client
from datetime import datetime

class HoldingsPublishService(object):
    def __init__(self, holdings_url, topic_arn):
        self.holdings_url = holdings_url
        self.topic_arn = topic_arn

    def publish(self):
        print('{} - Retrieveing holdings...'.format(datetime.now()))
        holdings = src.holdings_repository.get(self.holdings_url)
        messages = (HoldingSchema().dumps(holding) for holding in holdings)
        print('{} - Publishing holdings to SNS...'.format(datetime.now()))
        count = 0
        with src.sns_client.SnsClient(self.topic_arn) as client:
            for message in messages:
                client.publish(message)
                count += 1
        print('{} - Total {} holdings published!'.format(datetime.now(), count))
