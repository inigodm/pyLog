import sys
sys.path.insert(0, '/path/to/application/app/folder')
from Xunit.XUnit import TestCase, TestSuite, TestResult
from tratarLog import PyLog
import json

class Test(TestCase):
    pylog = None

    def setUp(self):
        self.pylog = PyLog()
        self.pylog.addRegexFor("wl11_error")
        self.pylog.addRegexFor("wl11_stuck")

    def testMain(self):
        assert 1 == 1        

    def testReadFile(self):
        self.pylog.tratar("./20181017intrashort.txt")
        print self.pylog.numLines
        print "json " + json.dumps(self.pylog.result)
        assert self.pylog.numLines == 4

    '''def testReadLongFile(self):
        self.pylog.tratar("./20181017intra.txt")
        print self.pylog.numLines'''


suite = TestSuite()
suite.addAll(Test)
result = TestResult()
suite.run(result)
for line in result.errorMsgs():
    print line
print result.summary()