import logging
import datetime
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import csv
import shutil
import multiprocessing
from multiprocessing import Pool
import subprocess
from subprocess import PIPE

import requests
import boto3
import argparse
from tqdm import tqdm
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.DEBUG, filename='task_error.log')
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.DEBUG)

WORKING_DIR = 'scene_detection'

def collect_data(file_name):
    url_map = {}
    with open(file_name) as f:
        reader = csv.reader(f)

        for row in reader:
            url_map[row[1]] = row[16]

    return url_map

def download_image(identifier, url):
    response = requests.get(url, stream=True)
    filename = WORKING_DIR + '/raw_photos/' + identifier + '.png'

    if response.status_code == 200:
        response.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

    else:
        raise RuntimeError(f'Error: Could not download image: {identifier}')

def upload_s3(identifier):
    session = boto3.Session(profile_name='magroup')
    s3 = session.client('s3')

    bucket_name = 'sightseeing-data'
    raw_photo_file_name = 'raw_photos/' + identifier + '.png'
    detected_photo_file_name = 'detected_photos/' + identifier + '.png'

    try:
        _ = s3.upload_file(WORKING_DIR + raw_photo_file_name, bucket_name, raw_photo_file_name)
        _ = s3.upload_file(WORKING_DIR + detected_photo_file_name, bucket_name, detected_photo_file_name)
    except ClientError as e:
        logger.error(f'Error: Could not upload {identifier}: {e}')
        raise

def upload_result():
    session = boto3.Session(profile_name='magroup')
    s3 = session.client('s3')

    bucket_name = 'sightseeing-data'
    file_name = 'sightseeing_place.csv'

    try:
        _ = s3.upload_file(WORKING_DIR + file_name, bucket_name, file_name)
    except ClientError as e:
        logger.error(f'Error: Could not upload result csv: {e}')
        raise

def detect(identifier):
    try:
        place_python_path = 'pipenv run python'
        place_exec_path = 'detect_sightseeing_one.py'
        working_directory = 'scene_detection'
        proc = subprocess.run( 
            f'{place_python_path} {place_exec_path} {identifier}',
            cwd=working_directory,
            shell=True, 
            check=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )

        if proc.returncode != 0:
            logger.error(f'{identifier}: {proc.stderr.decode("utf-8")}')
            raise RuntimeError('Error: while detection -> {}'.format(proc.stderr))

    except subprocess.CalledProcessError as e:
        logger.error(f'Error: detection: {identifier}: {e.cmd}: {e.returncode}: {e.output}')
        raise

    except Exception as e:
        logger.error(f'Error: detection: {identifier}: {e}')
        raise

def delete_files(identifier):
    raw_file_path = WORKING_DIR + 'raw_photos/' + identifier + '.png'
    if os.path.exists(raw_file_path):
        os.remove(raw_file_path)
    else:
        logger.error(f'{identifier}: Could not remove: {raw_file_path}')

    detected_file_path = WORKING_DIR + 'detected_photos/' + identifier + '.png'
    if os.path.exists(detected_file_path):
        os.remove(detected_file_path)
    else:
        logger.error(f'{identifier}: Could not remove: {detected_file_path}')


def run(identifier, url):
    try:
        download_image(identifier, url)
        detect(identifier)
        upload_s3(identifier)
        delete_files(identifier)

    except Exception as e:
        logging.error('-----------------------------------')
        logging.error(e)
        logging.error('-----------------------------------')

    return

def wrapper(args):
    return run(*args)

def main(args):
    start = time.time()
    id_url_dic = collect_data(args.file_name)

    params = []
    for identifier, url in id_url_dic.items():
        params.append((identifier, url))

    pool = Pool(multiprocessing.cpu_count() - 2)
    with tqdm(total=len(params)) as t:
        for _ in pool.imap_unordered(wrapper, params):
            t.update(1)

    pool.close()
    pool.join()

    upload_result()

    print(datetime.timedelta(seconds=time.time() - start))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='download images and object detection and upload S3')
    parser.add_argument('-f', '--file-name', type=str, help='csv data file')

    args = parser.parse_args()
    
    main(args)
