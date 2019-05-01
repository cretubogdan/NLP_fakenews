rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/fake-news/train.csv
export DEBUG=TRUE
python3 RandomForest.py modules/Logger.py modules/DBManager.py modules/WorkPool.py modules/Reader.py
rm -rf __pycache__
