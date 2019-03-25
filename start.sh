rm logs
rm -rf __pycache__
export LOGGER_PATH=/home/bogcretu/Desktop/workspace/NLP_fakenews/logs
python3 Main.py Logger.py DbManager.py WorkPool.py
