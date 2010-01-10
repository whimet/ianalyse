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
            __import__(module_string.replace('/', '.'))
            s.addTest(unittest.defaultTestLoader.loadTestsFromName(module_string.replace('/', '.')))
    return s