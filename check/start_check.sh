rm logs
export LOGGER_PATH=/Users/me/Desktop/Lucru/licenta/NLP_fakenews/check/logs
export DATASET=/Users/me/Desktop/Lucru/licenta/NLP_fakenews/check/news_sa.csv
export DEBUG=FALSE
python3 check.py
rm -rf ../modules/__pycache__