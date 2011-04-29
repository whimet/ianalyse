import unittest
import doctest
import os
import glob
test_file_strings = glob.glob('analyse/tests/*_tests.py')
module_strings = [str[0:len(str)-3] for str in test_file_strings]

def suite():
    s = unittest.TestSuite()
    test_type = os.environ.get("TEST_TYPE")
    if test_type == 'PERF' :
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.perf_tests.PerfTests))
    else :
        for module_string in module_strings:
            name = module_string.replace('/', '.')
            name = name.replace('\\', '.')
            __import__(name)
            s.addTest(unittest.defaultTestLoader.loadTestsFromName(name))
    return s