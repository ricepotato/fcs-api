import logging
import uuid
from typing import List, Optional, Protocol

import pymongo
from botocore.exceptions import ClientError
from bson import ObjectId
from mypy_boto3_dynamodb import DynamoDBServiceResource

from fcs import models

logger = logging.getLogger(__name__)


class Repository(Protocol):
    def insert_fc(self, fc: models.FCS):
        ...

    def get_fc_by_name(self, name: str) -> Optional[models.FCS]:
        ...

    def get_fc_by_no(self, no: str) -> Optional[models.FCS]:
        ...

    def get_fc_list(self, limit: int, offset: int) -> List[models.FCS]:
        ...

    def get_fc(self, id: str) -> Optional[models.FCS]:
        ...

    def get_count(self) -> int:
        ...

    def delete_fc(self, id: str) -> bool:
        ...

    def update_fc(self, fc: models.FCS) -> bool:
        ...


class MongodbRepository:
    def __init__(self, url: str):
        self.client = pymongo.MongoClient(url)
        self.collection = self.client.yazzal.fcs

    def insert_fc(self, fc: models.FCS):
        """
        Inserts an FCS item into an Amazon DynamoDB table.
        :param fc: The FCS item to insert.
        """
        result = self.collection.insert_one(fc.dict(exclude_none=True))
        return str(result.inserted_id)

    def get_fc_by_name(self, name: str) -> Optional[models.FCS]:
        """
        Gets an FCS item from an Amazon DynamoDB table.
        :param fc: The FCS item to insert.
        """

        result = self.collection.find_one({"name": name})
        if result is None:
            return None

        return models.FCS.from_mongo_result(result)

    def get_fc_by_no(self, no: str) -> Optional[models.FCS]:
        result = self.collection.find_one({"no": no})
        if result is None:
            return None

        return models.FCS.from_mongo_result(result)

    def get_fc_list(self, limit: int, offset: int) -> List[models.FCS]:
        result = self.collection.find().skip(offset).limit(limit)
        return [models.FCS.from_mongo_result(item) for item in result]

    def get_fc(self, id: str) -> Optional[models.FCS]:
        obj = self.collection.find_one({"_id": ObjectId(id)})
        if obj:
            return models.FCS.from_mongo_result(obj)

        return None

    def delete_all(self):
        result = self.collection.delete_many({})
        return result.deleted_count

    def get_count(self) -> int:
        return self.collection.count_documents({})

    def delete_fc(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1

    def update_fc(self, fc: models.FCS) -> bool:
        update_result = self.collection.update_one(
            {"_id": ObjectId(fc.id)}, {"$set": fc.dict(exclude_none=True, exclude={"id"})}
        )
        return update_result.modified_count == 1


class DynamoRepository:
    def __init__(self, dyn_resource: DynamoDBServiceResource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None
        self.table_name = "fcs2"

    def list_tables(self):
        """
        Lists the Amazon DynamoDB tables for the current account.
        :return: The list of tables.
        """

        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            logger.error(
                "Couldn't list tables. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return tables

    def insert_fc(self, fc: models.FCS):
        """
        Inserts an FCS item into an Amazon DynamoDB table.
        :param fc: The FCS item to insert.
        """

        fc.id = str(uuid.uuid4())
        table = self.dyn_resource.Table(self.table_name)
        put_item_result = table.put_item(Item=fc.dict())
        return put_item_result

    def get_fc_list(self, limit: int, offset: int):
        """
        Gets a list of FCS items from an Amazon DynamoDB table.
        :param limit: The maximum number of items to return.
        :param offset: The number of items to skip before returning items.
        :return: The list of FCS items.
        """

        table = self.dyn_resource.Table(self.table_name)
        items = table.scan(Limit=limit)
        return items

    def get_fc(self, fc_id: str):
        """
        Gets an FCS item from an Amazon DynamoDB table.
        :param fc_id: The ID of the FCS item.
        :return: The FCS item.
        """

        table = self.dyn_resource.Table(self.table_name)
        item = table.get_item(Key={"id": fc_id})

    def delete_all_items(self):
        """
        Deletes all items from an Amazon DynamoDB table.
        """

        table = self.dyn_resource.Table(self.table_name)
        table.delete_item(key={})
