import elasticsearchlib
import elastic_mappings

# import time

eslib = elasticsearchlib.Elasticsearchlib()
eslib.start_connection("213.227.143.136", 9200)

eslib.add_to_index("test", {"AA":4}, "id")


print(eslib.get_last_document("test", "id"))