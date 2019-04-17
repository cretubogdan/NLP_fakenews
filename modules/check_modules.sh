rm logs
export LOGGER_PATH=/home/bogcretu/Desktop/workspace/NLP_fakenews/modules/logs
export DATASET_TRAIN_PATH=/home/bogcretu/Desktop/workspace/datasets/trainingandtestdata/train.csv
export DATASET_TEST_PATH=/home/bogcretu/Desktop/workspace/datasets/trainingandtestdata/test.csv
export DEBUG=TRUE
python3 TestModules.py modules/Logger.py modules/DbManager.py modules/WorkPool.py modules/Reader.py
rm -rf __pycache__
