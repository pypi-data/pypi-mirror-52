from datetime import datetime

from testframework.util.sql_handler import SqlHandler
from tests import resource


def test_build_query_returns_properly_formatted_query_as_string():
    partition_time = datetime.utcnow().replace(microsecond=0)
    params = {"gcp_project_id": "testing",
              "dataset_name": "test_dataset",
              "table_name": "test_table_name",
              "filter": "customer_id = test_customer_id AND campaign_id = test_campaign_id AND message_id = test_message_id",
              "partition_time": partition_time}

    expected_query = "SELECT * FROM `testing.test_dataset.test_table_name` WHERE (_PARTITIONTIME IS NULL OR _PARTITIONTIME = TIMESTAMP('" + str(
        partition_time) + "')) AND (customer_id = test_customer_id AND campaign_id = test_campaign_id AND message_id = test_message_id)"

    sql_handler = SqlHandler()

    assert expected_query == sql_handler.build_query(resource("test_sql_handler.sql"), params)
