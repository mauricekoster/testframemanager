#! /usr/bin/env python3
from TestFrameFactory import ClusterFactory


factory = ClusterFactory()
factory.register_information_fields('date', 'version', 'document', 'author')
cluster = factory.get_from_tsv_file('test/Example.txt')
cluster.dump_info()
