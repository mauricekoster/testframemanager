#! /usr/bin/env python3

from SpreadsheetDOM import Workbooks
from TestFrame import Cluster
from TestFrameFactory import ClusterFactory

wb = Workbooks.OpenWorkbook('test/test-en.ods')

factory = ClusterFactory()

cluster = factory.getFromWorkbook(wb)

print("Cluster %s. ID: %s" % (cluster['cluster'], cluster['cluster id']))
print('\n\n', '-' * 80,'\n')
cluster.subcluster['XXXX01'].dump_info()
