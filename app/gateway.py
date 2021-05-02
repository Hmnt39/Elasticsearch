# -*- coding: utf-8 -*-
from uuid import uuid4
from typing import Dict, Optional, List
from contextlib import suppress

from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import NotFoundError, RequestError

from app import config


class ESGateway:
    """
    Elasticsearch Gateway
    """

    def __init__(self, index_name: str, mapping: Optional[Dict] = None):

        mapping = mapping if mapping else {}
        self.client = Elasticsearch(hosts=config.ES_HOST)
        self.index = index_name
        with suppress(RequestError):
            self.client.indices.create(
                index=index_name, body=mapping
            )
            
    def get(self, key: int):
        """
        Get Object by Key
        """
        try:
            return self.client.get(index=self.index, id=key)["_source"]
        except NotFoundError:
            return None

    def add(self, document: Dict):
        """
        Method to add document into the ES

        Args:
            body: document obj of the entity or document
            key: key of the document

        Return:
            response obj: (dict)
        """
        if not key:
            key = document.get("key") or str(uuid4())
        response = self.client.create(
            index=self.index,
            id=key,
            body=document
        )
        return response

    def bulk_create(self, documents: List = []):
        """
        Bulk Create documents into the index

        Args:
            documents: list of document

        Return:
            response obj: dict
        """
        body = [
            {
                "_index": self.index,
                "_id": document.get("key") or str(uuid4()),
                "_source": document,
            }
            for document in documents
        ]
        response = helpers.bulk(self.client, body)
        return response

    def update(self, key: int, document: Dict):
        """
        Method to Update an object using key

        Args:
            key: Key of document
            document: json object of document

        Return:
            response obj: dict
        """
        return self.client.update(
            index=self.index,
            id=key,
            body={"doc": document}
        )

    def delete(self, key: int):
        """
        Delete doc with primary key

        Args:
            key: int primary id of document

        Return:
            response obj: dict
        """
        try:
            status = self.client.delete(index=self.index, id=key)
        except:
            raise Exception(message="Doc not found")
        return status

    def query(
        self,
        body: Optional[Dict] = {},
        paginate: Optional[bool] = True,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        sorting: Optional[str] = None,
        search: Optional[str] = "",
        order_by: Optional[str] = "desc",
    ):
        """
        Elastic Search Query

        Args:
            body (dict): query_dict
            paginate (boolean): Whether response is paginated or not
            page (int): Page
            page_size (int): Page Size

        Return:
            response obj: dict
        """
        properties = config.ES_PROPERTIES_BY_INDEX.get(self.index, {})

        if not body:
            body = {"query": {"match_all": {}}}
        if paginate and page and page_size:
            body["from"] = (page * page_size) - page_size
            body["size"] = page * page_size
        sortables = properties.get("sort_fields") or {}
        sort = sortables.get(sorting)
        if sort:
            order = order_by if order_by else "asc"
            body["sort"] = [{sort: order}]
        if search:
            search = search + "*"
            searchables = properties.get("search", [])
            body["query"]["bool"]["must"] = [
                {"bool": {"should": [
                    {"wildcard": {searchable: search}}
                    for searchable in searchables
                ]}}
            ]
        print(body)
        es_params = {"index": self.index, "body": body}
        result = self.client.search(**es_params)
        count = result.get("hits", {}).get("total", {}).get("value", 0)
        response = {
            "count": count,
            "results": result.get("hits", {}).get("hits", []),
            "previous_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page * page_size < count else None,
        }
        data = [result.get("_source") for result in response.get("results")]
        response["results"] = data
        return response
