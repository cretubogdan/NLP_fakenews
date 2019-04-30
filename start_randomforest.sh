rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/trainingandtestdata/dataset.csv
export DEBUG=FALSE
python3 RandomForest.py modules/Logger.py modules/DbManager.py modules/WorkPool.py modules/Reader.py
rm -rf __pycache__
