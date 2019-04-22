from Logger import *
from DbManager import *
from WorkPool import *
from Reader import *

collection_name = 'FakeNews'
wp = WorkPool()
wp.run()
logger = Logger()

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
    for i in range(10):
        wp.enqueue(test_worker, i)
    for i in wp.get_results():
        print(i)

@wp.do_tasks
def test_wp_2(vec):
    new_vec = []
    for elem in vec:
        new_vec.append(elem + "LOL")
    return new_vec

def test_csv():
    csv = Reader()
    csv.Read()
    print(csv.GetHeaderTrain())
    print(csv.GetBodyTrain()[0])
    print(csv.GetBodyTrain()[-1])

    print(csv.GetHeaderTest())
    print(csv.GetBodyTest()[0])
    print(csv.GetBodyTest()[-1])

def main():
    if True:
        test_logger()
    if False:
        test_dbmanager()
        test_wp()
        test_csv()
    if True:
        vec = ["ana", "are", "mere", "si", "pere", "multe", "dar", "totusi", "mi-e", "somn", "si", "as", "vrea", "sa", "ma", "culc", ",", "e", "cam", "tarzior", "!", "!"]
        vec = test_wp_2(vec)
        print(vec)

if __name__ == '__main__':
    main()
    wp.abort()
