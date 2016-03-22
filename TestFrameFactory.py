from TestFrame import *


class TestFrameUnexpectedTestCase(Exception):
    pass


class ClusterFactory(object):
    def getFromWorkbook(self, workbook):
        if workbook.has_sheet('Version information'):
            lang = 'en'
            version_sheet = workbook.Sheets['Version information']
        else:
            lang = 'nl'
            version_sheet = workbook.Sheets['Versie informatie']

        cluster = Cluster()

        for r in range(1, version_sheet.RowCount+1):
            if not version_sheet.Cells(r,1).Text is None and version_sheet.Cells(r, 1).Style == 'information':
                cluster.add_information(version_sheet.Cells(r,1).Text, version_sheet.Cells(r,2).Text)

        for sheet in workbook.Sheets:
            if sheet.Name.startswith(cluster['cluster id']):
                print('Processing %s' % sheet.Name)
                subcluster = self._parse_sheet(sheet)
                cluster.add_subcluster(subcluster)

        return cluster

    @staticmethod
    def get_line_from_sheet(sheet, line_number):
        c = 1
        txt = []
        while sheet.Cells(line_number, c).Text:
            txt.append(sheet.Cells(line_number, c).Text)
            c += 1

        return txt

    def _parse_sheet(self, sheet):
        self.current_testcondition = None
        self.current_testcase = None

        subcluster = SubCluster()

        for r in range(1, sheet.RowCount+1):
            keyword_type = sheet.Cells(r, 1).Style
            txt = self.get_line_from_sheet(sheet, r)

            if not txt:
                continue

            elif keyword_type == 'information':
                subcluster.add_information(txt[0], txt[1])

            elif keyword_type == 'testcondition' and txt[0] == 'testcondition':
                tc = TestCondition( txt[1], txt[2], txt[5], txt[6], txt[7] )
                subcluster.add_testcondition(tc)
                self.current_testcondition = tc
                self.current_testcase = None

            elif keyword_type == 'testcase':
                if not current_testcondition:
                    raise TestFrameUnexpectedTestCase('sheet %s, row: %d' % (self.name, r))

                status=sheet.Cells(r, 8).Text

                testcase = TestCase(txt[1], txt[2], status)
                self.current_testcondition.add_testcase(testcase)
                self.current_testcase = testcase

            elif keyword_type == 'actionword':
                if txt[0][0] == '#':
                    # processing code
                    if txt[0] == '#tag':
                        key = txt[1]
                        value = txt[2]
                        if self.current_testcase:
                            pass
                        elif self.current_testcondition:
                            self.current_testcondition.add_tag(key, value)
                        else:
                            subcluster.add_tag(key, value)
                else:
                    # action word
                    ac = ActionWord(txt[0])
                    if self.current_testcase:
                        self.current_testcase.add_action(ac)
                    elif self.current_testcondition:
                        self.current_testcondition.add_setup_action(ac)
                    else:
                        subcluster.add_setup_action(ac)

        return subcluster

    def getFromTsvFile(self, filename):
        pass
