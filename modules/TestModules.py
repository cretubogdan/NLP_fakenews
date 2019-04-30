from Logger import *
from WorkPool import *
from Reader import *

l = Logger()
wp = WorkPool()
wp.abort()
r = Reader()

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
    arg = ["ana", "are", "mere", "si", "pere", "multe", "dar", "totusi", "mi-e", "somn", "si", "as", "vrea", "sa", "ma", "culc", ",", "e", "cam", "tarzior", "!", "!"]
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

def main():
    #check_logger()
    #check_workpool()
    #check_reader()
    print("Uncomment above")

if __name__ == '__main__':
    main()
