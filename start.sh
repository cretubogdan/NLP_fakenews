rm logs
rm -rf __pycache__
export LOGGER_PATH=/home/bogcretu/Desktop/workspace/NLP_fakenews/logs
export DATASET_PATH=/home/bogcretu/Desktop/task2/datasets/liar_dataset/test.tsv
python3 Main.py Logger.py DbManager.py WorkPool.py Reader.py
