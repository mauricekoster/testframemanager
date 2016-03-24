#! /usr/bin/env python3
from TestFrame import *
from TestframeExecutor import TestFrameExecutor, TestFrameXUnitReporter
from TestFrameFactory import ClusterFactory
import importlib
import yaml
import argparse
import os

base = os.path.dirname(os.path.realpath(__file__))
d = os.path.join(base, 'target', 'test-results')

parser = argparse.ArgumentParser(description='Execute TestFrame cluster')
parser.add_argument('script', help="Filename of script to process")
parser.add_argument('--output', dest='output', default=d,
                   help='location of output files (xUnit reports)')

args = parser.parse_args()
print(args)

os.makedirs(args.output, exist_ok=True)

if __name__ == '__main__':
    factory = ClusterFactory()
    factory.register_information_fields('date')
    factory.register_information_fields('number of testcases', 'number of testconditions')
    factory.register_information_fields('subcluster priority', 'version')

    if os.path.isabs(args.script):
        fn = args.script
    else:
        fn = os.path.join(base, args.script)
    print(fn)

    cluster = factory.get_from_ods_spreadsheet(fn)

    m = importlib.import_module("test.my_keywords")
    executor = TestFrameExecutor(m)
    cluster.accept(executor)

    fp = open(os.path.join(args.output, 'junit-%s.xml' % cluster.id), 'w')
    report = TestFrameXUnitReporter(fp)
    cluster.accept(report)
    fp.close()

    with open(os.path.join(args.output, 'testresult.yaml'), 'w') as fp:
        yaml.dump(cluster, fp)
