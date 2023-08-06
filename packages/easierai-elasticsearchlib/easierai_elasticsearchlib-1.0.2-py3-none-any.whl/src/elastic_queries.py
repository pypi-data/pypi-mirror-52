# Placeholder for all the Elasticsearch queries

QUERY_ALL = {
    # '_source': ['id'],
    'query': {
        'match_all': {}
    }
}


def query_by_id(device_id):
    body = {
        'query': {
            'match': {
                'id': device_id
            }
        }
    }

    return body


def query_by_type(type):
    body = {
        'query': {
            'match': {
                'type': type
            }
        }
    }

    return body


def query_data_history(device_id, gte, lte):
    body = {
        'query': {
            'bool': {
                'must': [{
                    'match': {
                        'id': device_id
                    }
                },
                    {
                        'range': {
                            'timestamp': {
                                'gte': gte,
                                'lt': lte
                            }
                        }
                    }
                ]
            }
        },
        'sort': [{
            'timestamp': {
                'order': 'asc'
            }
        }]
    }

    return body


def query_data_history_inv(device_id, gte, lte):
    body = {
        'query': {
            'bool': {
                'must': [
                    {'match': {'id': device_id}},
                    {'range': {
                        'timestamp': {
                            'gte': gte,
                            'lt': lte
                        }
                    }
                    }
                ]
            }
        },
        'sort': [{
            'timestamp': {'order': 'desc'}
        }]
    }

    return body
