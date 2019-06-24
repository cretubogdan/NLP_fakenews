rm logs
export LOGGER_PATH=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/check/logs
export DATASET=/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/check/news_sa.csv
export DEBUG=FALSE
python3 check.py
rm -rf ../modules/__pycache__