from TestFrame import *
from SpreadsheetDOM import Workbooks
import yaml

class TestFrameUnexpectedTestCase(Exception):
    pass


class ClusterFactory(object):
    def __init__(self):
        self.current_actionword = None
        self.current_testcase = None
        self.current_testcondition = None
        self.current_scenario = None
        self.subcluster = None

        self.keyword_types = {'information': ['cluster', 'cluster id', 'subcluster id', 'subcluster name'],
                              'scenario': ['scenario'],
                              'testcondition': ['testcondition', 'testconditie', "test condition"],
                              'testcase': ['testcase', 'test case', 'testgeval'],
                              'continue': ['&Cont', '&cont'],
                              'tag': ['#tag']}

    def register_information_fields(self, *fields):
        self.keyword_types['information'].extend(fields)

    def get_from_tsv_file(self, filename):
        cluster = Cluster()

        cluster.add_subcluster(self._parse_file(filename))

        return cluster

    def _parse_file(self, filename):
        self.current_testcondition = None
        self.current_testcase = None
        self.current_actionword = None
        self.current_scenario = None

        previous_line = None
        current_line = None

        self.subcluster = SubCluster()

        self.line_number = 0
        for line in open(filename):
            self.line_number += 1
            line = line.rstrip()
            previous_line = current_line
            current_line = line.split('\t')
            print(current_line)

            if not current_line:
                continue

            if current_line[0] is None or current_line[0] == '':
                continue

            self.process_line(current_line, previous_line)

        return self.subcluster

    def get_from_ods_spreadsheet(self, filename):
        workbook = Workbooks.OpenWorkbook(filename)

        if workbook.has_sheet('Version information'):
            lang = 'en'
            version_sheet = workbook.Sheets['Version information']
        else:
            lang = 'nl'
            version_sheet = workbook.Sheets['Versie informatie']

        cluster = Cluster()

        for r in range(1, version_sheet.RowCount + 1):
            if not version_sheet.Cells(r, 1).Text is None and version_sheet.Cells(r, 1).Style == 'information':
                cluster.add_information(version_sheet.Cells(r, 1).Text, version_sheet.Cells(r, 2).Text)

        for sheet in workbook.Sheets:
            if sheet.Name.startswith(cluster['cluster id']):
                subcluster = self._parse_sheet(sheet)
                cluster.add_subcluster(subcluster)

        return cluster

    @staticmethod
    def get_line_from_sheet(sheet, line_number):
        txt = []
        for c in range(1, sheet.ColumnCount + 1):
            txt.append(sheet.Cells(line_number, c).Text)

        return txt

    def determine_keyword_type(self, keyword):
        for keyword_type, keywords in self.keyword_types.items():
            if keyword in keywords:
                return keyword_type

        # default type is actionword
        return 'actionword'

    def process_line(self, current_line, previous_line):
        keyword_type = self.determine_keyword_type(current_line[0])

        if keyword_type == 'information':
            self.subcluster.add_information(current_line[0], current_line[1])

        elif keyword_type == 'testcondition':
            tc = TestCondition(current_line[1], current_line[2], current_line[5], current_line[6], current_line[7])
            self.subcluster.add_testcondition(tc)
            self.current_scenario = None
            self.current_testcondition = tc
            self.current_testcase = None

        elif keyword_type == 'scenario':
            scenario = Scenario(current_line[1])
            self.subcluster.add_scenario(scenario)
            self.current_scenario = scenario
            self.current_testcondition = None
            self.current_testcase = None

        elif keyword_type == 'testcase':
            if not self.current_testcondition:
                raise TestFrameUnexpectedTestCase('sheet %s, row: %d' % (self.subcluster.name, self.line_number))

            testcase = TestCase(current_line[1], current_line[2], current_line[8])
            self.current_testcondition.add_testcase(testcase)
            self.current_testcase = testcase

        elif keyword_type == 'tag':
            key = current_line[1]
            value = current_line[2]
            if self.current_testcase:
                self.current_testcase.add_tag(key, value)

            elif self.current_testcondition:
                self.current_testcondition.add_tag(key, value)

            else:
                self.subcluster.add_tag(key, value)

        elif keyword_type == 'actionword':
            # action word
            self.current_actionword = ActionWord(current_line[0])
            if self.current_testcase:
                self.current_testcase.add_action(self.current_actionword)
            elif self.current_testcondition:
                self.current_testcondition.add_setup_action(self.current_actionword)
            elif self.current_scenario:
                self.current_scenario.add_action(self.current_actionword)
            else:
                self.subcluster.add_setup_action(self.current_actionword)

            self.process_arguments(current_line, previous_line)

        elif keyword_type == 'continue':
            self.process_arguments(current_line, previous_line)

    def process_arguments(self, current_line, previous_line):
        use_previous = (not previous_line[0])
        argument_name = None
        for c, value in enumerate(current_line):
            if c == 0:
                continue

            if value is None:
                break

            if value.lower() == '&cont':
                break

            if use_previous:
                if c < len(previous_line):
                    argument_name = previous_line[c]
                else:
                    argument_name = None
            self.current_actionword.add_argument(value, argument_name)

    def _parse_sheet(self, sheet):
        self.current_testcondition = None
        self.current_testcase = None
        previous_line = None
        current_line = None

        self.subcluster = SubCluster()

        for r in range(1, sheet.RowCount + 1):
            self.line_number = r
            previous_line = current_line
            current_line = self.get_line_from_sheet(sheet, r)

            if not current_line:
                continue

            if current_line[0] is None or current_line[0] == '':
                continue

            self.process_line(current_line, previous_line)

        return self.subcluster

    def get_from_yaml(self, filename):
        return yaml.load(open(filename,'r'))
