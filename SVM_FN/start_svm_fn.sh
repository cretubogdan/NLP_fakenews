rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/SVM_FN/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/fake-news/train.csv
export DEBUG=TRUE
python3 SVM_FN.py
rm -rf ../modules/__pycache__
