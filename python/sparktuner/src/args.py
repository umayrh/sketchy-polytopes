import argparse
import opentuner

parser = argparse.ArgumentParser(parents=opentuner.argparsers())

# Program information
parser.add_argument('--name', type=str, required=True,
                    help='Program name')
parser.add_argument('--main-class', type=str, required=True,
                    help='Fully qualified class name')
parser.add_argument('--jar-path', type=str, required=True,
                    help='Absolute path of program JAR')
parser.add_argument('--master', type=str, required=True,
                    help='Master type')
parser.add_argument('--deploy-mode', type=str, required=True,
                    help='Deployment mode')

# Configuration parameters
# TODO: how should memory be accepted as input: str or int?
# TODO: inputs are ranges

parser.add_argument('--driver-memory', type=int, default=10,
                    help='Driver memory. Default: 1g.')
parser.add_argument('--executor-memory', type=int, default=10,
                    help='Executor memory. Default: 1g.')
parser.add_argument('--executor-cores', type=int, default=4,
                    help='Executor cores. Default: 4.')
parser.add_argument('--parallelism', type=int, default=10,
                    help='Parallelism and partitions. Default: 10.')
parser.add_argument('--max-executors', type=int, default=1,
                    help='Maximum number of executors. Default: 1.')
