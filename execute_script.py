#! /usr/bin/env python2

from TestframeExecutor import TestFrameExecutor, TestFrameXUnitReporter, TestFrameSelection
from TestFrameFactory import ClusterFactory
import importlib
import yaml
import argparse
import os
import sys

base = os.path.realpath(os.getcwd())
print("Base: %s" % base)
sys.path.append(base)

d = os.path.join(base, 'target', 'test-results')

parser = argparse.ArgumentParser(description='Execute TestFrame cluster')
parser.add_argument('script', help="Filename of script to process")
parser.add_argument('--output', dest='output', default=d,
                   help='location of output files (xUnit reports)')
parser.add_argument('--keywords', dest='keywords', default='keywords',
                    help='Name of module containing the keyword implementation')

parser.add_argument('--tag', dest='tags', default=None,
                    help='Tag to execute')
args = parser.parse_args()
print(args)


def _mkdir_recursive(path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        _mkdir_recursive(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)

_mkdir_recursive(args.output)

factory = ClusterFactory()

if os.path.isabs(args.script):
    fn = args.script
else:
    fn = os.path.join(base, args.script)

cluster = factory.get(fn)

selector = TestFrameSelection(args.tags)
cluster.accept(selector)


m = importlib.import_module(args.keywords)
executor = TestFrameExecutor(m)
cluster.accept(executor)

fp = open(os.path.join(args.output, 'junit-%s.xml' % cluster.id), 'w')
report = TestFrameXUnitReporter(fp)
cluster.accept(report)
fp.close()

with open(os.path.join(args.output, 'testresult.yaml'), 'w') as fp:
    yaml.dump(cluster, fp)
