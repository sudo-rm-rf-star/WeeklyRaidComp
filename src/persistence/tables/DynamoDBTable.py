from exceptions.InternalBotException import InternalBotException
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any, Generic, TypeVar, List
import utils.Logger as Log
import os

T = TypeVar('T')
DEV_THROUGHPUT = {
    "ReadCapacityUnits": 1,
    "WriteCapacityUnits": 1
}


class DynamoDBTable(Generic[T]):
    def __init__(self, ddb, table_name: str):
        self.ddb = ddb
        self.table = self._get_table(table_name)

    def get_item(self, **kwargs) -> Optional[T]:
        response = self.table.get_item(Key=self._to_key(**kwargs))
        if 'Item' not in response:
            return None
        return self._to_object(response['Item'])

    def delete_item(self, **kwargs) -> bool:
        try:
            self.table.delete_item(Key=self._to_key(**kwargs))
            return True
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceNotFoundException':
                raise e
            return False

    def scan(self, **kwargs) -> List[T]:
        response = self.table.scan(**kwargs)
        return [self._to_object(item) for item in response['Items']]

    def query(self, **kwargs) -> List[T]:
        response = self.table.query(**kwargs)
        return [self._to_object(item) for item in response['Items']]

    def put_item(self, t: T) -> None:
        self.table.put_item(Item=self._to_item(t))

    def _table_kwargs(self, **kwargs):
        raise NotImplementedError()

    def _to_object(self, item: Dict[str, Any]) -> T:
        raise NotImplementedError()

    def _to_item(self, t: T) -> Dict[str, Any]:
        raise NotImplementedError()

    def _to_key(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError()

    def create_table(self, table_name) -> Any:
        table_kwargs = self._table_kwargs()
        if os.getenv("APP_ENV") == "development":
            table_kwargs['ProvisionedThroughput'] = DEV_THROUGHPUT
            for gsi in table_kwargs.get("GlobalSecondaryIndexes", []):
                gsi['ProvisionedThroughput'] = DEV_THROUGHPUT

        return self.ddb.create_table(TableName=table_name, **table_kwargs)

    def _get_table(self, table_name: str):
        if os.getenv("APP_ENV") == "development":
            table_name += "-dev"

        try:
            table = self.create_table(table_name)
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                raise InternalBotException(f'The resource is not yet available. Please try again later.')
        return self.ddb.Table(table_name)

    def to_unique_object(self, response: Dict[str, Any]) -> T:
        if response['Count'] == 0:
            return None
        if response['Count'] > 1:
            Log.error(f'Received invalid DDB response: {response}')
            raise InternalBotException('Received invalid DDB response')
        return self._to_object(response['Items'][0])
