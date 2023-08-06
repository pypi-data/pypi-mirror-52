model_mapping = {
    'mappings': {
        'model_keras': {
            'properties': {
                'id': {
                    'type': 'keyword',
                    'ignore_above': 128,
                    'index': True
                },
                'timestamp': {
                    'type': 'date',
                    'format': 'epoch_millis',
                    'index': True
                },
                'algorithm': {
                    'type': 'keyword',
                    'ignore_above': 64,
                },
                'model_file': {
                    'type': 'keyword',
                    'ignore_above': 64,
                },
                'scaler_file': {
                    'type': 'keyword',
                    'ignore_above': 64,
                },
                'metadata': {
                    'type': 'object',
                },
            }
        }
    }
}

predictions_mapping = {
    "mappings": {
        "predictions_keras": {
            "properties": {
                "model_file": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "algorithm": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "id": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "prediction_times": {
                    "type": "date"
                },
                "timestamp": {
                    "type": "date"
                },
                "values": {
                    "type": "float"
                },
                "latency": {
                    "type": "float"
                }
            }
        }
    }
}
