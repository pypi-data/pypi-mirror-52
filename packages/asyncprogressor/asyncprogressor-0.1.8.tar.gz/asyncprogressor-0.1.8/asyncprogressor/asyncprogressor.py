#!/usr/bin/env python3
from tqdm import tqdm
import multiprocessing, time
import diskcache as dc
from datetime import datetime 

def go_progress(seconds):
    for i in tqdm(range(0, seconds * 2)):
        time.sleep(0.5)

def progressor(key):
        def wrapper(*args, **kwargs):
                cache = dc.Cache('tmp')
                whole_key = func.__name__
                if whole_key in cache:
                        if cache[whole_key] > 2:
                                p = multiprocessing.Process(target=go_progress, args=(int(cache[whole_key]),))
                                p.start()
                start = datetime.now()
                func(*args, **kwargs)
                end = datetime.now()
                cache[whole_key] = (end - start).seconds
        return wrapper


@progressor
def long_function():
        time.sleep(3)

if __name__ == "__main__":
        long_function()
        
