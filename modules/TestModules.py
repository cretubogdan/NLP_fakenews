from Logger import *
from WorkPool import *
from Reader import *
from DBManager import *

l = Logger()
wp = WorkPool()
wp.abort()
r = Reader()
db = DBManager()

def check_logger():
    logger1 = Logger()
    logger2 = Logger()

    logger1.log(Severity.INFO, "INFO MERGE")
    logger1.log(Severity.ERROR, "ERROR MERGE")
    logger2.log(Severity.FATAL, "FATAL MERGE")
    logger2.log(Severity.WARNING, "WARNING MERGE")

    logger1.close()

@wp.do_tasks
def helper_check_workpool(arg):
    new_arg = []
    for elem in arg:
        new_arg.append(elem + "LOL")
    return new_arg

def check_workpool():
    arg = ["I", "am", "a", "workpool", "of", "threads", "and", "I", "do", "all", "my", "jobs"]
    print(arg)
    new_arg = helper_check_workpool(arg)
    print(new_arg)
    wp.abort()

def check_reader():
    r.read()
    print(r.path)
    print(r.header)
    print(r.body[0])
    print(r.body[-1])
    print(r.rows)
    print(r.filetype)
    print(r.train[0])
    print(r.test[0])
    print(len(r.train))
    print(len(r.test))

def check_db():
    collection = "models_dump"
    model1 = {"name":"model1", "data":"asfasfasa11"}
    model2 = {"name":"model2", "data":"asfasfasa22"}
    db.insert(model1, collection)
    db.insert(model2, collection)

    query = {"name":"model2"}
    new_model = db.find(query, collection)
    for model in new_model:
        print(model)

    db.delete(query, collection)

    db.drop(collection)

def check_db_gridfs():
    f = open("dump", "rb")
    tmp = f.read()
    f.close()
    db.grid_insert(tmp, "test_dump")
    res = db.grid_find("test_dump")
    f = open("dump2", "wb")
    tmp = f.write(res)
    f.close()


def main():
    #check_logger()
    #check_workpool()
    #check_reader()
    #check_db()
    #check_db_gridfs() //need a binary file named <dump>
    print("Check above")

if __name__ == '__main__':
    main()
