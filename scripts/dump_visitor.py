#! /usr/bin/env python3
from TestFrame import *
from TestframeExecutor import TestFrameExecutor, TestFrameSimpleReporter, Dumper, TestFrameXUnitReporter
from TestFrameFactory import ClusterFactory
import importlib
import yaml

if __name__ == '__main__':
    factory = ClusterFactory()
    factory.register_information_fields('date')
    factory.register_information_fields('number of testcases', 'number of testconditions')
    factory.register_information_fields('subcluster priority', 'version')
    cluster = factory.get_from_ods_spreadsheet('test/test-en.ods')

    dumper = Dumper()
    cluster.accept(dumper)
    print('-' * 79)
    m = importlib.import_module("test.my_keywords")
    executor = TestFrameExecutor(m)
    cluster.accept(executor)
    print('-' * 79)
    report = TestFrameSimpleReporter()
    cluster.accept(report)

    fp = open('junit.xml', 'w')
    report = TestFrameXUnitReporter(fp)
    cluster.accept(report)
    fp.close()


    with open('testresult.yaml', 'w') as fp:
        yaml.dump(cluster, fp)
