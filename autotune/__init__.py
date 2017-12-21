from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from autotune.tuner import RandomSearch
from autotune.spec import Spec
import os


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('executable', help='executable to tune')
    parser.add_argument('config', help='config file for tuning')
    parser.add_argument('--gpu', help='whether to tune using GPU')
    parser.add_argument('--tuner', default='random', help='how to tune')
    parser.add_argument('--name', help='name field for recording parameter hashes')
    parser.add_argument('-n', '--num_jobs', help='how many jobs to run', type=int, default=10)
    parser.add_argument('-m', '--max_jobs', help='max jobs to run concurrently', type=int, default=8)
    parser.add_argument('-d', '--delay', help='delay in seconds between jobs', type=int, default=20)
    parser.add_argument('-o', '--output', help='output directory for log files', default=os.getcwd())
    args = parser.parse_args()

    config = Spec.load(args.config)

    Tuner = {
        'random': RandomSearch,
    }[args.tuner]

    tuner = Tuner(args.executable, config, name=args.name, gpu=args.gpu)
    tuner.tune(args.num_jobs, out=args.output, wait_seconds=args.delay, max_jobs=args.max_jobs)
