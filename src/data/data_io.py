import json
import gzip
from pathlib import Path
from typing import Union
import requests

def save_json(data: dict, filepath: Union[str, Path]):
    '''Save data as a JSON file.

    Args:
        data: Data to save.
        filepath: Save path. If it ends with '.gz', the file will be compressed with gzip.
    '''
    filepath = str(filepath)
    if filepath.endswith('.gz'):
        with gzip.open(filepath, 'wt', encoding='utf-8') as file:
            json.dump(data, file)
    else:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file)

def load_json(filepath: Union[str, Path]) -> dict:
    '''Load data from a JSON file.

    Args:
        filepath: Load path. If it ends with '.gz', the file will be decompressed with gzip.

    Returns:
        The loaded data as a dictionary.
    '''
    filepath = str(filepath)
    if filepath.endswith('.gz'):
        with gzip.open(filepath, 'rt', encoding='utf-8') as file:
            return json.load(file)
    else:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

def download_file(url: str, dest: Union[str, Path], timeout: int=30, chunk_size: int=8192):
    '''Download a file from a URL to a destination.'''
    response = requests.get(url, stream=True, timeout=timeout)
    with open(dest, 'wb') as file:
        for file_chunk in response.iter_content(chunk_size=chunk_size):
            file.write(file_chunk)
