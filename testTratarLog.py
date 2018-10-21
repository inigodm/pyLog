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
        #elf.pylog.addRegexFor("stuck_info")

    def testMain(self):
        assert 1 == 1        

    def testReadFile(self):
        self.pylog.tratar("./20181017intrashort.txt")
        print "json " + json.dumps(self.pylog.result)
        assert self.pylog.numLines == 4
        assert len(self.pylog.result) == 4
        assert self.pylog.result[0]["date"] == "Oct 17, 2018 9:11:01"

    def testReadLongFile(self):
        self.pylog.tratar("./20181017intra.txt")
        print self.pylog.numLines


suite = TestSuite()
suite.addAll(Test)
result = TestResult()
suite.run(result)
for line in result.errorMsgs():
    print line
print result.summary()