from collections import OrderedDict


class Cluster(object):
    def __init__(self):
        self.information = OrderedDict()
        self.subcluster = OrderedDict()

    def add_information(self, key, value):
        self.information[key] = value

    def add_subcluster(self, subcluster):
        self.subcluster[subcluster.id] = subcluster

    def __getitem__(self, key):
        if key in self.information:
            return self.information[key]
        else:
            return "?"

    def dump_info(self, level=0):
        print('\t' * level, "Information:")
        for k, v in self.information.items():
            print('\t' * level, "%s => %s" % (k, v))

        for subcluster in self.subcluster.values():
            print('\t' * level, '-' * 60)
            subcluster.dump_info(level + 1)

    @property
    def name(self):
        return self.information['cluster']

    @property
    def id(self):
        return self.information['cluster id']

    def accept(self, visitor):
        visitor.visit(self)
        visitor.visit(self, 'pre')
        for subcluster in self.subcluster.values():
            subcluster.accept(visitor)
        visitor.visit(self, 'post')


class SubCluster(object):
    """docstring for SubCluster"""

    def __init__(self):
        self.information = OrderedDict()
        self.testconditions = OrderedDict()
        self.scenarios = []
        self.tags = {}
        self.setup = []

    def add_information(self, tag, value):
        self.information[tag] = value

    def add_testcondition(self, testcondition):
        self.testconditions[testcondition.id] = testcondition

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

    def add_setup_action(self, action):
        self.setup.append(action)

    def add_tag(self, key, value):
        self.tags[key] = value

    def __getitem__(self, key):
        if key in self.information:
            return self.information[key]

    @property
    def name(self):
        return self.information['subcluster name']

    def accept(self, visitor):
        visitor.visit(self)
        if self.setup:
            for action in self.setup:
                action.accept(visitor)

        if self.scenarios:
            for scenario in self.scenarios:
                scenario.accept(visitor)

        if self.testconditions:
            for tc in self.testconditions.values():
                tc.accept(visitor)

    def dump_info(self, level=0):
        print('\t' * level, "Information:")
        for k, v in self.information.items():
            print('\t' * level, "%s => %s" % (k, v))

        if self.tags:
            print('\t' * level, "Tags:", self.tags)

        if self.setup:
            print('\t' * level, "Sub cluster setup:")
            for action in self.setup:
                action.dump_info(level + 1)

        if self.scenarios:
            print('\t' * level, "Scenarios:")
            for scenario in self.scenarios:
                scenario.dump_info(level + 1)

        if self.testconditions:
            print('\t' * level, "Testconditions:")
            for tc in self.testconditions.values():
                tc.dump_info(level + 1)

    @property
    def id(self):
        if 'subcluster id' in self.information:
            return self.information['subcluster id']
        else:
            return None

    @property
    def name(self):
        if 'subcluster name' in self.information:
            return self.information['subcluster name']
        else:
            return None


class Scenario(object):
    """docstring for Scenario"""

    def __init__(self, description):
        self.description = description
        self.tags = {}
        self.actions = []

    def add_tag(self, key, value):
        self.tags[key] = value

    def add_action(self, action):
        self.actions.append(action)

    def accept(self, visitor):
        visitor.visit(self)
        if self.actions:
            for action in self.actions:
                action.accept(visitor)

    def dump_info(self, level=0):
        print('\t' * level, "Scenario description: ", self.description)
        if self.tags:
            print('\t' * level, "- Tags:", self.tags)
        if self.actions:
            print('\t' * level, "- Actions:")
            for action in self.actions:
                action.dump_info(level + 1)


class TestCondition(object):
    """docstring for TestCondition"""

    def __init__(self, id, description, business_priority, status, test_priority):
        self.id = id
        self.description = description
        self.business_priority = business_priority
        self.status = status
        self.test_priority = test_priority
        self.setup = []  # list of actionwords
        self.tags = {}
        self.test_cases = OrderedDict()

    def add_tag(self, key, value):
        self.tags[key] = value

    def add_setup_action(self, action):
        self.setup.append(action)

    def add_testcase(self, testcase):
        self.test_cases[testcase.id] = testcase

    def accept(self, visitor):
        visitor.visit(self)
        visitor.visit(self, 'pre')
        if self.setup:
            for action in self.setup:
                action.accept(visitor)

        for testcase in self.test_cases.values():
            testcase.accept(visitor)

        visitor.visit(self, 'post')

    def dump_info(self, level=0):
        print('\t' * level, "ID: ", self.id, "Description: ", self.description)
        if self.tags:
            print('\t' * level, "- Tags:", self.tags)
        if self.setup:
            print('\t' * level, "- Setup:")
            for action in self.setup:
                action.dump_info(level + 1)
        print('\t' * level, "- Testcases:")
        for testcase in self.test_cases.values():
            testcase.dump_info(level + 1)


class TestCase(object):
    """docstring for TestCase"""

    def __init__(self, id, description, status=None):
        self.id = id
        self.description = description
        self.test_status = status
        self.actions = []  # list of action words
        self.tags = {}

    def add_tag(self, key, value):
        self.tags[key] = value

    def add_action(self, action):
        self.actions.append(action)

    def accept(self, visitor):
        visitor.visit(self)
        visitor.visit(self, 'pre')
        for action in self.actions:
            action.accept(visitor)
        visitor.visit(self, 'post')

    def dump_info(self, level=0):
        print('\t' * level, "ID: ", self.id, "Description: ", self.description)
        if self.tags:
            print('\t' * level, "- Tags:", self.tags)
        print('\t' * level, "- Actions:")
        for action in self.actions:
            action.dump_info(level + 1)


class ActionWord(object):
    def __init__(self, actionword):
        self.actionword = actionword
        self.arguments = OrderedDict()

    def accept(self, visitor):
        visitor.visit(self)

    def dump_info(self, level=0):
        print('\t' * level, "action: ", self.actionword)
        for argname, argvalue in self.arguments.items():
            print('\t' * level, '\t', '%s: %s' % (argname, argvalue))

    def add_argument(self, value, name=None):
        if name:
            nm = name
        else:
            nm = 'arg' + str(len(self.arguments) + 1)

        self.arguments[nm] = value