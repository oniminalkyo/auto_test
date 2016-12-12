import unittest


class LineAnalyser(object):
    FRD_ID = ':frd:'
    FUNCTION_ID = 'def'
    INTERFACE_ID = 'import'

    def __init__(self, code_line):
        self._line_items = [item for item in code_line.split() if item]
        self._function = ''

    def get_interface(self):
        return self._line_items[1]

    def get_function(self):
        self._function = self._line_items[1].split('(')[0]
        return self._function

    def get_frd_dic(self):
        frd_dic = {}
        for item in self._line_items[1:]:
            parse_item = item.split('(')
            key = parse_item[0]
            value = parse_item[1].split(')')[0]
            frd_dic[key] = value

        return frd_dic

    def is_function_line(self):
        if not self._line_items:
            return False

        if self._line_items[0] != self.FUNCTION_ID:
            return False

        return True

    def is_interface_line(self):
        if not self._line_items:
            return False

        if self._line_items[0] != self.INTERFACE_ID:
            return False

        return True

    def is_frd_line(self):
        if not self._line_items:
            return False

        if self._line_items[0] != self.FRD_ID:
            return False

        return True


class TestCaseWriter(object):
    INCIDENT_BLANK_4 = '    '
    INCIDENT_BLANK_8 = INCIDENT_BLANK_4 * 2

    def __init__(self, src_file, interface, test_plan):
        self._module = src_file.split('.')[0]
        self._test_file = 'test_' + src_file
        self._interface = interface
        self._test_plan = test_plan

    def write(self):
        self._map_test_plan_to_cases()

    def _map_test_plan_to_cases(self):
        with open(self._test_file, 'w') as file:
            file.writelines('import unittest\n')
            file.writelines('from unittest import mock\n')
            file.writelines('import %s\n' % self._module)
            for function in self._test_plan:
                file.writelines('from %s import %s\n' % (self._module, function))
            file.writelines('\n\n')

            self._map_frd_to_test_cases(file)

            file.writelines("if __name__ == '__main__':\n")
            file.writelines(self.INCIDENT_BLANK_4 + "unittest.main()\n")

    def _map_frd_to_test_cases(self, file):
        for function in self._test_plan:
            file.writelines('class Test_%s(unittest.TestCase):\n' % function)
            for i, frd in enumerate(self._test_plan[function]):
                file.writelines(self.INCIDENT_BLANK_4 + 'def test_frd%s(self):\n' % i)
                if 'input' in frd:
                    file.writelines(self.INCIDENT_BLANK_8 + 'result = %s(%s)\n' % (function, frd['input']))
                else:
                    file.writelines(self.INCIDENT_BLANK_8 + 'result = %s()\n' % function)

                if 'return' in frd:
                    file.writelines(self.INCIDENT_BLANK_8 + 'self.assertEqual(%s, result)\n' % frd['return'])
                else:
                    file.writelines(self.INCIDENT_BLANK_8 + 'self.assertEqual(%s, None)\n')

                file.writelines('\n')
            file.writelines('\n')


class AutoTester(object):
    def __init__(self, src_file):
        self._src_file = src_file
        self._test_file = 'test_' + self._src_file
        self._load()

    def run(self):
        suite = unittest.TestSuite()
        suite.addTests(unittest.TestLoader().discover("./", 'test*.py'))
        unittest.TextTestRunner().run(suite)

    def _load(self):
        interface = []
        test_plan = {}
        with open(self._src_file) as file:
            for each_line in file:
                line_analyser = LineAnalyser(each_line)
                if line_analyser.is_interface_line():
                    inter = line_analyser.get_interface()
                    interface.append(inter)

                elif line_analyser.is_function_line():
                    function = line_analyser.get_function()
                    test_plan[function] = []

                elif line_analyser.is_frd_line():
                    frd_dic = line_analyser.get_frd_dic()
                    test_plan[function].append(frd_dic)

        valid_plan = self._check_test_plan_validate(test_plan)
        self._test_plan_to_cases(interface, valid_plan)

    def _test_plan_to_cases(self, interface, test_plan):
        """
        {
            'abs_num': [ {'input': -1, 'return': 1}, {'input': 1, 'return': 1} ]
        }
        """
        print('interfaces = %s' % interface)
        print('test_plan:')
        print(test_plan)
        case_writer = TestCaseWriter(self._src_file, interface, test_plan)
        case_writer.write()

    @staticmethod
    def _check_test_plan_validate(test_plan):
        valid_plan = {}
        for function in test_plan:
            if test_plan[function]:
                valid_plan[function] = test_plan[function]
        return valid_plan

if __name__ == '__main__':
    tester = AutoTester('fibnaci.py')
    tester.run()