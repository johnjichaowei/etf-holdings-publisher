import boto3

class SnsClient(object):
    def __init__(self, topic_arn):
        self.topic_arn = topic_arn

    def publish(self, msg):
        return self.topic.publish(Message=msg)

    def __enter__(self):
        sns = boto3.resource('sns')
        self.topic = sns.Topic(self.topic_arn)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
