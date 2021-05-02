# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
load_dotenv()

def get_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        print(f"{env_variable} variable not set")

ES_HOST = get_value("ES_HOST")

BLOG_INDEX = "blog-index"

## Define Mapping of a document for ES
ES_PROPERTIES_BY_INDEX = {
    BLOG_INDEX : {
        ## Define Index name
        "index": BLOG_INDEX,
        ## Define Sorting with keys and values
        "sort_fields": {"key": "key"},
        ## Define searchable fields in Document
        "search": {"source.name", "title"},
        "configuration": {
            "settings": {
                "index": {"max_ngram_diff": 20},
                "analysis": {
                    "filter": {
                        "autocomplete_filter": {
                            "type": "ngram",
                            "min_gram": 3,
                            "max_gram": 20,
                            "token_chars": ["letter", "digit"],
                        }
                    },
                    "analyzer": {
                        "autocomplete": {
                            "type": "custom",
                            "tokenizer": "autocomplete",
                            "filter": ["lowercase", "autocomplete_filter"],
                        },
                        "autocomplete_search": {
                            "tokenizer": "standard",
                            "filter": ["lowercase"],
                        },
                    },
                    "tokenizer": {
                        "autocomplete": {
                            "type": "ngram",
                            "min_gram": 3,
                            "max_gram": 20,
                            "token_chars": ["letter", "digit"],
                        }
                    },
                },
            },
            "mappings": {
                "properties": {
                    "created_at": {"type": "date"},
                    "is_active": {"type": "boolean"},
                    "is_deleted": {"type": "boolean"},
                    "modified_at": {"type": "date"},
                    "key": {"type": "long"},
                    "title": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword", "ignore_above": 256
                            }
                        },
                    },
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        },
                    },
                    "source": {
                        "properties": {
                            "name": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword", "ignore_above": 256
                                    }
                                },
                            },
                            "id": {"type": "long"}
                        },
                    },
                    "url": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        },
                    },
                    "rating": {"type": "text"},
                }
            }
        }
    }
}


ES_SAMPLE_DATA = [
    {
        "key": 1,
        "title": "Blog 1",
        "created_at": "2021-04-01",
        "modified_at":  "2021-04-02",
        "is_active": True,
        "is_deleted": False,
        "source": {
            "name": "Google",
            "id": 1
        },
        "url": "http://google.com/1",
        "description": "Google AI solves rare calculus problems in record time",
        "rating": 5
    },
    {
        "key": 2,
        "title": "Blog 2",
        "created_at": "2021-04-04",
        "modified_at":  "2021-04-04",
        "is_active": True,
        "is_deleted": False,
        "source": {
            "name": "Amazon",
            "id": 2
        },
        "url": "http://amazon.com/1",
        "description": "AWS lambda invocation using triggers",
        "rating": 4
    },
    {
        "key": 3,
        "title": "Blog 3",
        "created_at": "2021-04-02",
        "modified_at":  "2021-04-02",
        "is_active": True,
        "is_deleted": False,
        "source": {
            "name": "Google",
            "id": 1
        },
        "url": "http://google.com/2",
        "description": "Firebase SDK introduces new features for mobile testing",
        "rating": 5
    },
    {
        "key": 4,
        "title": "Blog 4",
        "created_at": "2021-04-03",
        "modified_at":  "2021-04-04",
        "is_active": True,
        "is_deleted": False,
        "source": {
            "name": "Amazon",
            "id": 2
        },
        "url": "http://amazon.com/2",
        "description": "Cloud functions now supports PHP for written procedures",
        "rating": 4
    },
    {
        "key": 5,
        "title": "Blog 5",
        "created_at": "2021-04-01",
        "modified_at":  "2021-04-01",
        "is_active": True,
        "is_deleted": False,
        "source": {
            "name": "Google",
            "id": 1
        },
        "url": "http://google.com/3",
        "description": "Mobile API have more stabilization for maps and navigation",
        "rating": 3
    }
]