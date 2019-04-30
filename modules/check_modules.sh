rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/modules/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/trainingandtestdata/dataset.csv
export DEBUG=TRUE
python3 TestModules.py modules/Logger.py modules/DbManager.py modules/WorkPool.py modules/Reader.py
rm -rf __pycache__
