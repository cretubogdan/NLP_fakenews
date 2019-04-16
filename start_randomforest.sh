rm logs
export LOGGER_PATH=/home/bogcretu/Desktop/workspace/NLP_fakenews/logs
export DATASET_PATH=/home/bogcretu/Desktop/task2/datasets/liar_dataset/test.tsv
python3 RandomForest.py modules/Logger.py modules/DbManager.py modules/WorkPool.py modules/Reader.py
rm -rf __pycache__
