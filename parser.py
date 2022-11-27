import time

import multiprocessing
import requests
from bs4 import BeautifulSoup

import pandas as pd
import math

from loguru import logger

from utils import initialize_data_folder, initialize_error_folder
from utils import chunks

from settings import PROXY_URL, USER_AGENT
from settings import DATA_FOLDER, ERROR_FILEPATH
from settings import TARGET_LINKS_FILEPATH
from settings import headers, proxies


def get_page_data(target_links:list):
    logger.info("STARTING NEW PROCESS")
    error_links=[]
    for i, link in enumerate(target_links):
        # parse data from url-page
        try:
            response = requests.get(url=link, headers=headers, proxies=proxies, timeout=3)
        except Exception as e: 
            logger.error(f"TIMED OUT {e}")
            error_links.append(link)
            continue
        if(response.status_code != 200):
            logger.error(f"BAD RESPONSE {response.status_code}")
            error_links.append(link)
            continue

        # get username, name and html 
        employee_username = link.split('/')[-1]
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.find("div", class_='page-title').h1.text
        html = soup.find("body")

        # write name, link and html to the file
        with open (f"{DATA_FOLDER}/{employee_username}.txt", "w") as r:
            r.write(f"{link}\n{name}\n{html}")

        logger.debug(f"link number: {i}; status: {response.status_code}")

    # write error links to the file
    with open (ERROR_FILEPATH, "a") as r:
        for error_link in error_links:
            r.writelines(f"{error_link}\n")

    logger.info("THREAD FINISHED")


if __name__ == "__main__":

    # initialize folders
    initialize_data_folder()
    initialize_error_folder()

    # here u can set the number of process
    # default equal quantity of device cores 
    CORES = multiprocessing.cpu_count()
    
    # get targer urls and chunk them for equal parts for each process
    links = pd.read_csv(TARGET_LINKS_FILEPATH)['url'].to_list()
    chunked_links = chunks(links, CORES)

    processes = []

    start_time = time.time()

    for i in range(CORES):
        p = multiprocessing.Process(target=get_page_data, args=(chunked_links[i], ))
        processes.append(p)
        p.start()

    for proc in processes: proc.join()


    total_work_time = time.time()-start_time
    total_requests = len(links)
    avg_req_per_sec = (len(links)/total_work_time)

    logger.info(f"total requests: {total_requests}")
    logger.info(f"total work time: {total_work_time}")
    logger.info(f"avg req/sec: {avg_req_per_sec}")
