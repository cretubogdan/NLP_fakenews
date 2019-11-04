rm logs
export LOGGER_PATH=/Users/me/Desktop/Lucru/licenta/NLP_fakenews/naive_bayse/logs
export DATASET=/Users/me/Desktop/Lucru/licenta/trainingandtestdata/dataset.csv
export DEBUG=TRUE
python3 /Users/me/Desktop/Lucru/licenta/NLP_fakenews/naive_bayse/NaiveBayse.py
rm -rf ../modules/__pycache__
