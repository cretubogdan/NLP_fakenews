from Logger import *
from DbManager import *
from WorkPool import *

collection_name = 'FakeNews'

def main():
    logger = Logger()
    db = DbManager(collection_name)
    wp = WorkPool()

if __name__ == '__main__':
    main()
