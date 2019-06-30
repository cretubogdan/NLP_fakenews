rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/kfold/logs
export DATASET_SA=/Users/mihnea-bogdancretu/Desktop/licenta/trainingandtestdata/dataset.csv
export DATASET_FN=/Users/mihnea-bogdancretu/Desktop/licenta/fake-news/train.csv
export DEBUG=TRUE
python3 kfold.py
rm -rf ../modules/__pycache__
