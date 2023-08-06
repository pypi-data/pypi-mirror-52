import datetime as dt
from elasticsearch import Elasticsearch
import logging
import pydash as _

import elastic_queries as queries
import elastic_mappings

# This comment is necessary because pylint throws errors when using the elasticsearch API because it uses decorators.
# pylint: disable=E1123
# By default, queries will target to up to 10000 documents (maximum permitted by Elastic, without tweaking the legacy setup)
QUERY_SIZE = 2000


class Elasticsearchlib:
    __instance = None
    _logger = logging.getLogger(__name__)

    def __new__(cls):
        if Elasticsearchlib.__instance is None:
            Elasticsearchlib.__instance = object.__new__(cls)
        return Elasticsearchlib.__instance

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.WARNING)

    def start_connection(self, host, port):
        _es = Elasticsearch(hosts=[{'host': host,
                                    'port': port}])
        self.es = _es
        try:
            _es.ping()
        except Exception as e:
            self._logger.error('Could not connect to Elasticsearch')

        self._logger.info('Connected successfully to Elasticsearch')

        return _es
        
    def find_prediction(self, entity, time=None):
        if time is None:
            time = dt.datetime.now().isoformat()

        q = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "@timestamp": time,
                            "id": entity
                        }
                    }
                ]
            }
        }
        self.es.search(index="predictions", body=q)

    def iso_timestamp_to_elk_format(self, timestamp):
        try:
            return dt.datetime.strptime(str(timestamp), "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            return dt.datetime.strptime(str(timestamp), "%Y-%m-%dT%H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S")

    def add_new_entity(self, entity):
        if (not self.entity_exists("entities", entity)):
            body = {
                'id': entity
            }
            self.es.index('entities', 'typelist', body)

    def list_entities(self, apiID):
        qu = {
            "_source": ["id"],
            'query': {
                'match_all': {}
            }
        }
        res = self.es.search(index="entities", body=qu, scroll='2m')

        # Scroll with 1000 entries
        entries = self.get_source_as_list(res['hits']['hits'])

        # Get the scroll ID
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits'])

        while scroll_size > 0:
            res = self.es.scroll(scroll_id=sid, scroll='2m')

            entries = self.get_source_as_list(res['hits']['hits'], entries)

            # Update the scroll ID
            sid = res['_scroll_id']

            # Get the number of results that returned in the last scroll
            scroll_size = len(res['hits']['hits'])

        entities = []
        for ent in entries:
            if ent["id"] not in entities:
                entities.append(ent["id"])
        return entities

    def list_all_entities(self, apiID):
        qu = {
            "_source": ["id"],
            'query': {
                'match_all': {}
            }
        }
        res = self.es.search(index=apiID, body=qu, scroll='2m')

        # Scroll with 1000 entries
        entries = self.get_source_as_list(res['hits']['hits'])

        # Get the scroll ID
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits'])

        while scroll_size > 0:
            res = self.es.scroll(scroll_id=sid, scroll='2m')

            entries = self.get_source_as_list(res['hits']['hits'], entries)

            # Update the scroll ID
            sid = res['_scroll_id']

            # Get the number of results that returned in the last scroll
            scroll_size = len(res['hits']['hits'])

        entities = []
        for ent in entries:
            if ent["id"] not in entities:
                entities.append(ent["_source"]["id"])
        return entities

    def last_timestamp_entity(self, apiID, id_dataset):
        filter_by_timestamp = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "id": id_dataset
                        }
                    }
                }
            },
            "sort": {
                "timestamp": {
                    "order": "desc",
                    "mode": "max"
                }
            }
        }
        res = self.es.search(index=apiID, body=filter_by_timestamp)
        timestamp = res['hits']['hits'][0]['_source']['timestamp']
        return timestamp

    def entity_exists(self, apiID, entity):
        q = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "id": entity
                        }
                    }
                }
            }
        }
        res = self.es.search(index=apiID, body=q)
        if (res['hits']['total'] == 0):
            return False
        else:
            return True

    def get_last_value_entity(self, apiID, entity):
        q = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "id": entity
                        }
                    }
                }
            },
            "sort": {
                "timestamp": {
                    "order": "desc",
                    "mode": "max"
                }
            }
        }
        res = self.es.search(index=apiID, body=q)
        source_list = []
        for el in res['hits']['hits']:
            source_list.append(el['_source'])
            break

        return source_list

    def number_of_samples_entity(self, apiID, id_dataset):
        filter_by_timestamp = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "id": id_dataset
                        }
                    }
                }
            }
        }
        res = self.es.search(index=apiID, body=filter_by_timestamp)
        return len(res['hits']['hits'])

    def first_timestamp_entity(self, apiID, id_dataset):
        filter_by_timestamp = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "id": id_dataset
                        }
                    }
                }
            },
            "sort": {
                "timestamp": {
                    "order": "asc"
                    # "mode": "max"
                }
            }
        }
        res = self.es.search(index=apiID, body=filter_by_timestamp)
        timestamp = res['hits']['hits'][0]['_source']['timestamp']
        return timestamp

    def get_last_timestamp_trained(self, id_dataset):
        q = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "id": id_dataset
                        }
                    }
                }
            }
        }
        res = self.es.search(index="information", body=q)
        if (res['hits']['total'] == 0):
            return None
        else:
            timestamp = res['hits']['hits'][0]['_source']['timestamp']
            return timestamp

    def set_last_timestamp_trained(self, id_dataset, time):
        q = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "id": id_dataset
                        }
                    }
                }
            }
        }
        res = self.es.search(index='information', body=q)
        if (len(res['hits']['hits']) == 0):
            body = {
                'timestamp': time,
                'id': id_dataset
            }
            self.es.index('information', 'timeseriestype', body)
        else:
            entity = res['hits']['hits'][0]
            internal_id = entity['_id']
            body = entity['_source']
            body['timestamp'] = time
            self.es.index('information', 'timeseriestype', body, id=internal_id)

    def get_source_as_list(self, results, s_list=None):
        if (s_list is None):
            source_list = []
        else:
            source_list = s_list
        for el in results:
            source_list.append(el['_source'])
        return source_list

    def search_from_time(self, apiID, id_dataset, time):
        filter_by_timestamp = {
            "query": {
                'bool': {
                    "must": [
                        {
                            "match": {
                                "id": id_dataset
                            }
                        },
                        {
                            "range": {
                                "timestamp": {
                                    "gt": time,
                                }
                            }
                        }
                    ]
                }
            },
            "sort": {
                "timestamp": {
                    "order": "desc",
                    "mode": "max"
                }
            }
        }

        # Scroll with 1000 entries
        res = self.es.search(index=apiID, body=filter_by_timestamp, scroll='2m')

        if (len(res['hits']['hits']) == 0):
            return None

        entries = self.get_source_as_list(res['hits']['hits'])

        # Get the scroll ID
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits'])

        while scroll_size > 0:
            res = self.es.scroll(scroll_id=sid, scroll='2m')

            entries = self.get_source_as_list(res['hits']['hits'], entries)

            # Update the scroll ID
            sid = res['_scroll_id']

            # Get the number of results that returned in the last scroll
            scroll_size = len(res['hits']['hits'])

        return entries

    def search_until_time(self, apiID, id_dataset, time):
        filter_by_timestamp = {
            "query": {
                'bool': {
                    "must": [
                        {
                            "match": {
                                "id": id_dataset
                            }
                        },
                        {
                            "range": {
                                "timestamp": {
                                    "lte": time,
                                }
                            }
                        }
                    ]
                }
            },
            "sort": {
                "timestamp": {
                    "order": "asc",
                    "mode": "max"
                }
            }
        }

        # Scroll with 1000 entries
        res = self.es.search(index=apiID, body=filter_by_timestamp, scroll='2m')
        entries = self.get_source_as_list(res['hits']['hits'])

        # Get the scroll ID
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits'])

        while scroll_size > 0:
            res = self.es.scroll(scroll_id=sid, scroll='2m')

            entries = self.get_source_as_list(res['hits']['hits'], entries)

            # Update the scroll ID
            sid = res['_scroll_id']

            # Get the number of results that returned in the last scroll
            scroll_size = len(res['hits']['hits'])

        return entries

    def search_between_times(self, apiID, id_dataset, time1, time2):
        filter_by_timestamp = {
            "query": {
                'bool': {
                    "must": [
                        {
                            "match": {
                                "id": id_dataset
                            }
                        },
                        {
                            "range": {
                                "timestamp": {
                                    "gte": time1,
                                    "lte": time2
                                }
                            }
                        }
                    ]
                }
            },
            "sort": {
                "timestamp": {
                    "order": "desc",
                    "mode": "max"
                }
            }
        }

        # Scroll with 1000 entries
        res = self.es.search(index=apiID, body=filter_by_timestamp, scroll='2m')
        entries = self.get_source_as_list(res['hits']['hits'])

        # Get the scroll ID
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits'])

        while scroll_size > 0:
            res = self.es.scroll(scroll_id=sid, scroll='2m')

            entries = self.get_source_as_list(res['hits']['hits'], entries)

            # Update the scroll ID
            sid = res['_scroll_id']

            # Get the number of results that returned in the last scroll
            scroll_size = len(res['hits']['hits'])

        return entries

    def search_last_n_measures(self, apiID, id_dataset, n):
        filter_by_timestamp = {
            "query": {
                'bool': {
                    "must": [
                        {
                            "match": {
                                "id": id_dataset
                            }
                        }
                    ]
                }
            },
            "sort": {
                "timestamp": {
                    "order": "desc",
                    "mode": "max"
                }
            }
        }

        # Scroll with 1000 entries
        res = self.es.search(index=apiID, body=filter_by_timestamp, scroll='2m')
        entries = self.get_source_as_list(res['hits']['hits'])

        # Get the scroll ID
        sid = res['_scroll_id']
        scroll_size = len(res['hits']['hits'])

        if (scroll_size > n):
            entries = self.get_source_as_list(res['hits']['hits'], entries)
            return entries[:n]
        else:
            num_entries = scroll_size
            while scroll_size > 0 and num_entries < n:
                res = self.es.scroll(scroll_id=sid, scroll='2m')

                entries = self.get_source_as_list(res['hits']['hits'], entries)

                # Update the scroll ID
                sid = res['_scroll_id']

                # Get the number of results that returned in the last scroll and add it to our total number of entries
                scroll_size = len(res['hits']['hits'])
                num_entries += scroll_size

            if (num_entries < n):
                return None
            else:
                return entries[:n]

    ##############################
    # FIWARE Summit area

    def create_index(self, index, mapping=None):
        if not self.es.indices.exists(index):
            self._logger.info('New index detected, creating corresponding entity in DB...')

            res = self.es.indices.create(index=index, body=mapping)
            if res['acknowledged']:
                self._logger.info("Created new index correctly for " + index)
            else:
                self._logger.error("Could not create new index for " + index)

        else:
            self._logger.debug("Index already exists for " + index)

    def add_to_index(self, index, body, doc_type, id=''):
        try:
            self.es.index(index=index, body=body, doc_type=doc_type, id=id)
        except Exception as e:
            self._logger.error('Cannot save document on Elastic - ' + str(e))

    def standard_query(self, query, index, filter_path=None):

        res = self.es.search(index=index, body=query,
                             filter_path=filter_path, size=QUERY_SIZE)

        # ToDo - performance and logging

        ###        
        if (res['hits']['total'] > 0):
            output = res['hits']['hits']
        else:
            output = []
        return output

    def scrolled_query(self, query, index, filter_path=None):

        output = []
        res = self.es.search(index=index, body=query, scroll='2m',
                             filter_path=filter_path, size=QUERY_SIZE)

        scroll_id = res['_scroll_id']

        if (res['hits']['total']):
            output = _.concat(output, res['hits']['hits'])

        if (res['hits']['total'] > QUERY_SIZE):
            more = True
            while (more):
                res = self.es.scroll(scroll_id=scroll_id, scroll='2m', filter_path=filter_path)
                more = _.has(res, 'hits.hits')
                if (more):
                    output = _.concat(output, res['hits']['hits'])

            # ToDo - performance and logging

            ###
            self.es.clear_scroll(scroll_id=scroll_id)
        else:
            self.es.clear_scroll(scroll_id=scroll_id)
        return output

    def get_entities_ids(self, index):

        filter_path = ['_scroll_id', 'took', 'hits.total', 'hits.hits._id']
        aux = self.scrolled_query(queries.QUERY_ALL, index, filter_path)
        return _.map_(aux, lambda x: x['_id'])

    def get_first_document(self, index, device_id):
        output = []
        query = queries.query_by_id(device_id)
        filter_path = ['hits.hits._source', 'hits.total']
        # aux = self.standard_query (query, index)

        res = self.es.search(index=index, body=query,
                             filter_path=filter_path, size=1, sort='timestamp:asc')

        # ToDo - performance and logging

        ###        

        if (res['hits']['total'] > 0):
            output = _.head(res['hits']['hits'])['_source']
        else:
            output = []
        return output

    def get_last_document(self, index, device_id):
        output = []
        query = queries.query_by_id(device_id)
        filter_path = ['hits.hits._source', 'hits.total', 'hits.hits._id']
        # aux = self.standard_query (query, index)

        res = self.es.search(index=index, body=query,
                             filter_path=filter_path, size=1, sort='timestamp:desc')

        # ToDo - performance and logging

        ###

        if (res['hits']['total'] > 0):
            output = _.head(res['hits']['hits'])
        else:
            output = []
        return output

    def get_data_history(self, index, device_id, gte, lte='now'):

        filter_path = ['_scroll_id', 'took', 'hits.total', 'hits.hits._source']

        # Get all data
        query = queries.query_data_history(device_id, gte, lte)
        aux = self.scrolled_query(query, index, filter_path)

        # (TEMP)
        # Get last 10000 observations
        # Temporal: This time we will take up to 10000 (QUERY_SIZE) documents 
        # query = queries.query_data_history_inv(device_id, gte, lte)               
        # aux = self.standard_query(query, index, filter_path)  

        return _.collections.map_(aux, lambda x: x['_source'])
