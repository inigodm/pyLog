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
        assert self.pylog.numLines == 4
        assert len(self.pylog.result) == 4
        assert self.pylog.result[0]["date"] == "Oct 17, 2018 9:11:01"

    def testReadLongFile(self):
        self.pylog.tratar("./20181017intra.txt")
        print self.pylog.numLines
        assert(len(self.pylog.result) == 57)
        assert(self.pylog.result[56]["stuckinfo"]["thread num"]=="53")
        text_file = open("Output.txt", "w")
        text_file.write(json.dumps(self.pylog.result))
        text_file.close()
        
        


suite = TestSuite()
suite.addAll(Test)
result = TestResult()
suite.run(result)
for line in result.errorMsgs():
    print line
print result.summary()