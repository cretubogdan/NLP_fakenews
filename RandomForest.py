import sys
sys.path.insert(0, "modules")
from Logger import *
from DbManager import *
from WorkPool import *
from Reader import *

collection_name = 'FakeNews'

def test_dbmanager():
    db = DbManager(collection_name)
    db.Insert({'test':'merge'})
    db.InsertBulk([{'test2':'merge2'}, {'test3':'merge3'}])
    ret = db.Find({"test2":"merge2"})
    print(list(ret))
    ret = db.FindBulk()
    print(list(ret))
    db.DeleteBulk({})


def test_logger():
    logger_1 = Logger()
    logger_2 = Logger()

    logger_1.Log(Severity.INFO, "Test_INFO")
    logger_2.Log(Severity.WARNING, "TEST_WARNING")
    logger_1.Log(Severity.ERROR, "Test_ERROR")
    logger_2.Log(Severity.FATAL, "Test_FATAL")

def test_worker(n):
    return n*2

def test_wp():
    wp = WorkPool()
    wp.run()
    for i in range(1000):
        wp.enqueue(test_worker, i)
    for i in wp.get_results():
        print(i)

def test_csv():
    csv = Reader()
    csv.Read()
    print(csv.GetHeader())
    print(csv.GetBody()[0])
    print(csv.GetBody()[-1])

def main():
    if True:
        test_logger()
        test_dbmanager()
        test_wp()
        test_csv()

if __name__ == '__main__':
    main()
