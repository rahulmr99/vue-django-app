from django.db.models.signals import post_migrate
from django.dispatch import receiver
import time

@receiver(post_migrate, )
def create_dynamo_db_tables(sender, **kwargs):  # noqa
    """it is important to ensure that the DynamoDB tables are created before tests/production usage"""
    from lexbot import utils, models

    if sender.name == 'lexbot':
        for Table in [
            models.CallerInfoQueue,
            models.LexSessionAttrsStore,
        ]:

            if not Table.exists():
                Table.create_table()
                retry = 0
                try:
                    time.sleep(1)
                    db = utils.get_boto_client("dynamodb")
                    response = db.update_time_to_live(
                        TableName=Table.Meta.table_name,
                        TimeToLiveSpecification={
                            'Enabled': True,
                            'AttributeName': Table.expire_at.attr_name,
                        }
                    )
                    print("Enable TTL ", response)
                except Exception as ex:
                    if retry > 12:
                        raise ex
                    retry += 1
                    print("Failed to enable TTL. Retrying", retry)
