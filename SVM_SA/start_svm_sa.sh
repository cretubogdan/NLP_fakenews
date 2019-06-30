rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/SVM_SA/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/trainingandtestdata/dataset.csv
export DEBUG=TRUE
python3 /Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/SVM_SA/SVM_SA.py
rm -rf ../modules/__pycache__
