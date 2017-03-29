from __future__ import print_function
from TestFrame import *
import datetime
import timeit
import cgi


class TestFrameTestFailure(Exception):
    pass


def html_escape(html_entity):
    return cgi.escape(html_entity)


class TestFrameExecutor(object):
    def __init__(self, keyword_module, strict_mode=False):
        self.keyword_module = keyword_module
        self.has_error = False
        self.error_text = None
        self.test_case_ok = True
        self.test_condition_ok = True
        self.executing = True
        self.tc_start_time = 0
        self.start_time = 0
        self.strict_mode = strict_mode

    def visit(self, element, phase=None):

        if type(element) is TestCondition:
            if phase == 'pre':
                self.test_condition_ok = True
                element.execution_timestamp = datetime.datetime.now().isoformat()
                self.tc_start_time = timeit.default_timer()

            elif phase == 'post':
                if self.test_condition_ok:
                    element.test_status = 'G'
                else:
                    element.test_status = 'F'
                element.elapsed = timeit.default_timer() - self.tc_start_time

        elif type(element) is TestCase:
            if phase == 'pre':
                self.test_case_ok = True
                self.has_error = False
                self.error_text = None
                self.executing = (element.test_status != 'N')
                if self.executing:
                    print("Executing test case", element.id)
                self.start_time = timeit.default_timer()

            elif phase == 'post':
                element.elapsed = timeit.default_timer() - self.start_time
                if element.test_status != 'N':
                    if self.test_case_ok:
                        element.test_status = 'G'
                    else:
                        self.test_condition_ok = False
                        if self.has_error:
                            element.test_status = 'T'
                        else:
                            element.test_status = 'F'
                        element.error = self.error_text

        elif type(element) is ActionWord:
            try:
                if self.executing:
                    func = element.actionword.replace(' ', '_')
                    print("executing: ", element.actionword, func)
                    method = getattr(self.keyword_module, func)
                    args = element.arguments.values()
                    method(*args)
                    element.test_status = 'G'

            except TestFrameTestFailure as e:
                self.test_case_ok = False
                element.test_status = 'F'
                element.error = str(e)
                self.executing = False
                self.has_error = True
                self.error_text = element.error

            except Exception as e:
                print(e)
                self.test_case_ok = False
                element.test_status = 'T'
                element.error = str(e)
                self.executing = False
                self.has_error = True
                self.error_text = element.error


class TestFrameSimpleReporter(object):
    def visit(self, element, phase=None):
        if type(element) is TestCondition:
            if phase is None:
                print("Test condition %s result %s" % (element.id, element.test_status))
        elif type(element) is TestCase:
            if phase is None:
                print("\tTest case %s result %s" % (element.id, element.test_status))


class TestFrameXUnitReporter(object):
    def __init__(self, file):
        self.file = file
        self.current_test_condition_id = None

    def visit(self, element, phase=None):
        if type(element) is Cluster:
            if phase == 'pre':
                self.file.write('<?xml version="1.0" encoding="UTF-8"?>\n<testsuites>\n')
            elif phase == 'post':
                self.file.write('</testsuites>\n')

        if type(element) is TestCondition:
            if phase is 'pre':
                nr_tests = len(element.test_cases)
                nr_failed = sum(tc.test_status == 'F' for tc in element.test_cases.values())
                nr_errors = sum(tc.test_status == 'T' for tc in element.test_cases.values())
                nr_skipped = sum(tc.test_status == 'N' for tc in element.test_cases.values())
                self.file.write(
                    '\t<testsuite name="%s" tests="%d" failures="%d" errors="%d" '
                    'skipped="%d" timestamp="%s" time="%0.5f">\n'
                    % (element.id, nr_tests, nr_failed, nr_errors, nr_skipped, element.execution_timestamp, element.elapsed))
                self.current_test_condition_id = element.id

            elif phase is 'post':
                self.file.write("\t</testsuite>\n")

        elif type(element) is TestCase:
            if phase is None:
                self.file.write('\t\t<testcase classname="%s" name="[%s] %s" time="%0.5f">\n' %
                                (self.current_test_condition_id, element.id, html_escape(element.description), element.elapsed))

                if element.test_status == 'F':
                    self.file.write('\t\t\t<failure message="Test failed">%s</failure>\n'
                                    % html_escape(element.error))
                elif element.test_status == 'T':
                    self.file.write('\t\t\t<error message="Exception occurred">%s</error>\n'
                                    % html_escape(element.error))
                elif element.test_status == 'N':
                    self.file.write('\t\t\t<skipped />\n')

                self.file.write("\t\t</testcase>\n")


class Dumper(object):
    """
    Dumper: visitor for dumping the TestFrame Object Model to the console (stdout)
    """
    def visit(self, element, phase=None):

        if type(element) is Cluster:
            if phase == 'pre':
                print("\nCluster '%s' information:" % element.name)
                for k, v in element.information.items():
                    print("%s => %s" % (k, v))

        elif type(element) is SubCluster:
            print("\n\tSub cluster '%s' information:" % element.name)
            for k, v in element.information.items():
                    print("\t\t%s => %s" % (k, v))

        elif type(element) is TestCondition:
            if phase is None:
                print("\n\tTest condition %s: %s" % (element.id, element.description))

        elif type(element) is TestCase:
            if phase is None:
                print("\n\tTest case %s: %s" % (element.id, element.description))

        elif type(element) is ActionWord:
            print('\t\t', "action: ", element.actionword)
            for arg_name, arg_value in element.arguments.items():
                print('\t\t\t', '%s: %s' % (arg_name, arg_value))

            element.ok = True


class TestFrameSelection(object):
    def __init__(self, selection=None):
        self.selection = selection

    def visit(self, element, phase=None):
        if type(element) is TestCase:
            if phase is None:
                if self.selection is None:
                    element.test_status = 'S'
                elif element.id == self.selection:
                    element.test_status = 'S'
                elif self.selection in element.tags:
                    element.test_status = 'S'
                else:
                    element.test_status = 'N'

        elif type(element) is TestCondition:
            if phase == 'post':
                if element.id == self.selection:
                    for test_case in element.test_cases.values():
                        test_case.test_status = 'S'
