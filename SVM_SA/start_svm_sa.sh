rm logs
export LOGGER_PATH=/Users/me/Desktop/Lucru/licenta/NLP_fakenews/SVM_SA/logs
export DATASET=/Users/me/Desktop/Lucru/licenta/trainingandtestdata/dataset.csv
export DEBUG=TRUE
python3 /Users/me/Desktop/Lucru/licenta/NLP_fakenews/SVM_SA/SVM_SA.py
rm -rf ../modules/__pycache__
