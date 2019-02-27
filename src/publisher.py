from .holdings_publish_service import HoldingsPublishService

def call(event, context):
    holdings_url = os.environ('ETF_HOLDINGS_URL')
    topic_arn = os.environ('HOLDINGS_PUBLISH_TOPIC_ARN')
    HoldingsPublishService(holdings_url, topic_arn).publish()