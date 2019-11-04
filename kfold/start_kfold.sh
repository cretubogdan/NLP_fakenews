rm logs
export LOGGER_PATH=/Users/me/Desktop/Lucru/licenta/NLP_fakenews/kfold/logs
export DATASET_SA=/Users/me/Desktop/Lucru/licenta/trainingandtestdata/dataset.csv
export DATASET_FN=/Users/me/Desktop/Lucru/licenta/fake-news/train.csv
export DEBUG=TRUE
python3 kfold.py
rm -rf ../modules/__pycache__
