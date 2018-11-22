import sys
sys.path.insert(0, '/path/to/application/app/folder')
from Xunit.XUnit import TestCase, TestSuite, TestResult
from tratarLog import PyLog
from DBManager import DBManager
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
        assert(len(self.pylog.result.keys()) == 2)
        assert(len(self.pylog.result["wl11_error"]) == 3)
        assert(len(self.pylog.result["wl11_stuck"]) == 1)
        assert self.pylog.result["wl11_error"][0]["date"] == "Oct 17, 2018 9:11:01"

    def testReadLongFile(self):
        self.pylog.tratar("./20181017intra.txt")
        text_file = open("Output.txt", "w")
        text_file.write("var vjson="+json.dumps(self.pylog.result))
        text_file.close()
        assert(len(self.pylog.result.keys()) == 2)
        assert(len(self.pylog.result["wl11_error"]) == 20)
        assert(len(self.pylog.result["wl11_stuck"]) == 37)
        assert(self.pylog.result["wl11_stuck"][36]["stuck_info"]["thread num"]=="53")     
        db = DBManager("test2.db")
        db.addElements(self.pylog.result)


    
    def testDBCreation(self):
        import os.path
        #os.remove("test.db")
        db = DBManager("test.db")
        assert(os.path.isfile("test.db"))
        res = {}
        res['elem1'] = []
        res['elem1'].append({'val1':'valor 1', 'val2':'valor2'}) 
        res['elem1'].append({'val1':'otro 1', 'val2':'otro 2'})
        res['extra'] = []
        #res['extra'].append({'vala1':'valor 1', 'vaal2':'valor2'}) 
        res['extra'].append({'vala1':'otro 1', 'vaal2':'otro 2', 'data':{'inner':'uno', 'dos':'dos'}})
        res['extra'].append({'vala1':'otro 3', 'vaal2':'otro 4', 'data':{'inner':'tres', 'dos':'cuatro'}})
        db.addElements(res)
        

suite = TestSuite()
suite.addAll(Test)
result = TestResult()
suite.run(result)
for line in result.errorMsgs():
    print line
print result.summary()