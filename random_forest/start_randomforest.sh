rm logs
export LOGGER_PATH=/Users/me/Desktop/Lucru/licenta/NLP_fakenews/random_forest/logs
export DATASET=/Users/me/Desktop/Lucru/licenta/fake-news/train.csv
export DEBUG=TRUE
python3 /Users/me/Desktop/Lucru/licenta/NLP_fakenews/random_forest/RandomForest.py
rm -rf ../modules/__pycache__
