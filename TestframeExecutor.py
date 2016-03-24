from TestFrame import *
import html
import datetime
import timeit

class TestFrameTestFailure(Exception):
    pass


class TestFrameExecutor(object):
    def __init__(self, keyword_module):
        self.keyword_module = keyword_module
        self.has_error = False
        self.error_text = None
        self.testcase_ok = True
        self.testcondition_ok = True
        self.executing = True

    def visit(self, element, phase=None):
        if type(element) is TestCondition:
            if phase == 'pre':
                self.testcondition_ok = True
                element.execution_timestamp = datetime.datetime.now().isoformat()
                self.tc_start_time = timeit.default_timer()

            elif phase == 'post':
                if self.testcondition_ok:
                    element.test_status = 'G'
                else:
                    element.test_status = 'F'
                element.elapsed = timeit.default_timer() - self.tc_start_time

        elif type(element) is TestCase:
            if phase == 'pre':
                self.testcase_ok = True
                self.has_error = False
                self.error_text = None
                self.executing = (element.test_status != 'N')
                if self.executing:
                    print("Executing test case", element.id)
                self.start_time = timeit.default_timer()

            elif phase == 'post':
                element.elapsed = timeit.default_timer() - self.start_time
                if element.test_status != 'N':
                    if self.testcase_ok:
                        element.test_status = 'G'
                    else:
                        self.testcondition_ok = False
                        if self.has_error:
                            element.test_status = 'T'
                        else:
                            element.test_status = 'F'
                        element.error = self.error_text

        elif type(element) is ActionWord:
            try:
                if self.executing:
                    print("executing: ", element.actionword)
                    func = element.actionword.replace(' ', '_')
                    method = getattr(self.keyword_module, func)
                    args = element.arguments.values()
                    method(*args)
                    element.test_status = 'G'

            except TestFrameTestFailure as e:
                self.testcase_ok = False
                element.test_status = 'F'
                element.error = str(e)
                self.executing = False
                self.has_error = True
                self.error_text = element.error

            except Exception as e:
                print(e)
                self.testcase_ok = False
                element.test_status = 'T'
                element.error = str(e)
                self.executing = False
                self.has_error = True
                self.error_text = element.error


class TestFrameSimpleReporter(object):
    def visit(self, element, phase=None):
        if type(element) is TestCondition:
            if phase is None:
                print("Testcondition %s result %s" % (element.id, element.test_status))
        elif type(element) is TestCase:
            if phase is None:
                print("\tTestcase %s result %s" % (element.id, element.test_status))


class TestFrameXUnitReporter(object):
    def __init__(self, file):
        self.file = file
        self.current_testcondition_id = None

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
                self.current_testcondition_id = element.id

            elif phase is 'post':
                self.file.write("\t</testsuite>\n")

        elif type(element) is TestCase:
            if phase is None:
                self.file.write('\t\t<testcase classname="%s" name="[%s] %s" time="%0.5f">\n' %
                                (self.current_testcondition_id, element.id, html.escape(element.description), element.elapsed))

                if element.test_status == 'F':
                    self.file.write('\t\t\t<failure message="Test failed">%s</failure>\n'
                                    % html.escape(element.error))
                elif element.test_status == 'T':
                    self.file.write('\t\t\t<error message="Exception occurred">%s</error>\n'
                                    % html.escape(element.error))
                elif element.test_status == 'N':
                    self.file.write('\t\t\t<skipped />\n')

                self.file.write("\t\t</testcase>\n")


class Dumper(object):
    def visit(self, element, phase=None):

        if type(element) is Cluster:
            print("\nCluster '%s' information:" % element.name)
            for k, v in element.information.items():
                print("%s => %s" % (k, v))

        elif type(element) is SubCluster:
            print("\n\tSub cluster '%s' information:" % element.name)

        elif type(element) is TestCondition:
            if phase is None:
                print("\n\tTest condition %s: %s" % (element.id, element.description))

        elif type(element) is TestCase:
            if phase is None:
                print("\n\tTest case %s: %s" % (element.id, element.description))

        elif type(element) is ActionWord:
            print('\t\t', "action: ", element.actionword)
            for argname, argvalue in element.arguments.items():
                print('\t\t\t', '%s: %s' % (argname, argvalue))

            element.ok = True
