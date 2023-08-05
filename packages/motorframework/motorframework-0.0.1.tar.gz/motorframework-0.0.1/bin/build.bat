cd \home\motorframework
python setup.py sdist
cd dist
pip uninstall motorframework -y
pip install motorframework-0.0.1.tar.gz
cd \home\motorframework\test
robot hello.robot
cd \home\motorframework
