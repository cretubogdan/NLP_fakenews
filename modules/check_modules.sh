rm logs
export LOGGER_PATH=/home/bogcretu/Desktop/workspace/NLP_fakenews/modules/logs
export DATASET_PATH=/home/bogcretu/Desktop/task2/datasets/liar_dataset/test.tsv
python3 TestModules.py Logger.py DbManager.py WorkPool.py Reader.py
rm -rf __pycache__
