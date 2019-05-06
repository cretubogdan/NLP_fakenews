rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/naive_bayse/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/trainingandtestdata/dataset.csv
export DEBUG=TRUE
python3 NaiveBayse.py
rm -rf *__pycache__
