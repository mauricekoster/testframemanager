#! /usr/bin/env python3
from TestFrame import *
from TestframeExecutor import TestFrameExecutor, TestFrameSimpleReporter
from TestFrameFactory import ClusterFactory
import importlib
import yaml

if __name__ == '__main__':
    factory = ClusterFactory()
    factory.register_information_fields('date')
    factory.register_information_fields('number of testcases', 'number of testconditions')
    factory.register_information_fields('subcluster priority', 'version')
    cluster = factory.get_from_yaml('testresult.yaml')

    report = TestFrameSimpleReporter()
    cluster.accept(report)

