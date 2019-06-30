rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/random_forest/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/fake-news/train.csv
export DEBUG=TRUE
python3 /Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/random_forest/RandomForest.py
rm -rf ../modules/__pycache__
