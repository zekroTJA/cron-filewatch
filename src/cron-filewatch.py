import os
import json
import argparse
import subprocess
from os import path
from enum import Enum


STAT_FILE_NAME = '.cron_filewatch_laststats'


class DiffMode(Enum):
    CREATE = 1
    REMOVE = 2
    MOD = 3


def main():
    args = parse_args()
    stat_file = path.join(args.dir, STAT_FILE_NAME)
    s_before = load_stats(stat_file)
    s_now = lsdir(args.dir)
    if not (args.ignoreinit and len(s_before) == 0):
        diff_stats(s_before, s_now, handler_wrapper(args.command))
    save_stats(stat_file, s_now)
    pass


def handler_wrapper(command):
    def handler(stat, mode):
        args = command.split(' ')
        args.extend([
            stat.get('dir'),
            str(mode.value),
            json.dumps(stat)])
        subprocess.call(args)
    return handler


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir', '-d', type=str, required=True, 
        help='The directory to be watched for changes.')
    parser.add_argument(
        '--recursive', '-r', default=True, action='store_true',
        help='Whether the directory is watched recursively or not.')
    parser.add_argument(
        '--ignoreinit', default=False, action='store_true',
        help='Whether to ignore initialization or not.\
            If set to true, no action is taken on first run when no files \
            were being tracked before. Otherwise, the handler will be called \
            for each file in the directory.')
    parser.add_argument(
        '--command', '-c', type=str, required=True,
        help='The command to be executed on file change.')
    return parser.parse_args()


def lsdir(dir, recursive=True, files=[]):
    for f in os.listdir(dir):
        if f == STAT_FILE_NAME:
            continue
        fpath = os.path.abspath(path.join(dir, f))
        if path.isfile(fpath):
            stat = os.stat(fpath)
            files.append({
                'name': f,
                'dir': fpath,
                'modns': stat.st_mtime_ns,
            })
        elif recursive:
            lsdir(fpath, True, files)
    return files


def save_stats(filepath, stats):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(stats, f)


def load_stats(filepath):
    if not path.isfile(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def diff_stats(s_before, s_now, handler):
    s_before_map = dict([(s.get('dir'), s) for s in s_before])
    s_now_map = dict([(s.get('dir'), s) for s in s_now])

    for s in s_now:
        d = s.get('dir')
        if d not in s_before_map:
            handler(s, DiffMode.CREATE)
        elif s_before_map.get(d).get('modns') != s.get('modns'):
            handler(s, DiffMode.MOD)

    for s in s_before:
        d = s.get('dir')
        if d not in s_now_map:
            handler(s, DiffMode.REMOVE)


if __name__ == '__main__':
    main()
