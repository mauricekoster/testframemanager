#! /usr/bin/env python3
from TestFrameFactory import ClusterFactory


factory = ClusterFactory()
factory.register_information_fields('date')
factory.register_information_fields('number of testcases', 'number of testconditions')
factory.register_information_fields('subcluster priority', 'version')
cluster = factory.get_from_ods_spreadsheet('test/test-en.ods')
cluster.dump_info()
