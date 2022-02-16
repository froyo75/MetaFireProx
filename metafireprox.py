import argparse
from bs4 import BeautifulSoup
from collections import defaultdict
import os
from queue import Queue
import requests
import threading
import time

add_lock = threading.Lock()
query_queue = Queue()
search_results = defaultdict(list)

def csv_list(string):
    return string.split(",")

def check_query(proxy, query):
	if proxy[-1] == '/':
		proxy = proxy[:-1]
		
	url = f'{proxy}/{query}'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
	}

	parts = query.split('&')[0].split('site:')
	domain = parts[1].strip()
	filetype = parts[0].split(':')[1].strip()
	results = requests.get(url, headers=headers, verify=False, proxies=None)
	soup = BeautifulSoup(results.text, 'lxml')
	with add_lock:
		idx = 1
		for a in soup.find_all('a', href=True):
			link = a['href']
			if domain + '/' in link:
				search_results[filetype].append(link)
			idx+=1

def gen_queries(domain, filetype, max_pages):
	query = f'search?q=filetype:{filetype} site:{domain}&start=0&num=100'
	query_queue.put(query)
	for count in range(1,max_pages+1)[99::100]:
		query = f'search?q=filetype:{filetype} site:{domain}&start={count}&num=100'
		query_queue.put(query)
	
def process_queue(proxy):
	while True:
		current_query = query_queue.get()
		check_query(proxy, current_query)
		query_queue.task_done()

def gen_results(output_folder):
	if len(search_results) == 0:
		print(f'[-] No results found :(')
	else:
		for key in search_results:
			folder_path = f'{output_folder}/{key}'
			isFolderExist = os.path.exists(folder_path)
			if not isFolderExist:
				os.makedirs(folder_path)
			file_path = f'{folder_path}/{key}.list'
			with open(file_path, 'w', encoding = 'utf-8') as f:
				for value in search_results[key]:
					f.write(f'{value}\n')
			print(f'[+] Total .{key} files: {len(search_results[key])}')

def main():
	parser = argparse.ArgumentParser(description='Scrape certain extensions of files from Google Search results for a specific domain using FireProx API by @froyo75')
	parser.add_argument("-d", help="Domain to search", type=str, required=True,  default=None, dest="domain")
	parser.add_argument('-x', help='FireProx API URL', type=str, required=True, default=None, dest="proxy")
	parser.add_argument('-e', help='File types to download (pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx). To search all 17,576 three-letter "ALL"', required=True, type=csv_list, dest="file_types")
	parser.add_argument('-o', help='The output folder where the results will be stored', type=str, default='.', dest="output_folder")
	parser.add_argument('-p', help='Google search pages to enumerate (default:1000)', type=int, default=1000, dest="max_pages")
	parser.add_argument('-t', help='Number of threads per extension (default:5)', type=int, default=5, dest="max_threads")
	args = parser.parse_args()

	proxy = args.proxy
	file_types = args.file_types
	domain = args.domain
	max_threads = args.max_threads
	max_pages = args.max_pages
	output_folder = args.output_folder

	if output_folder == '.':
		output_folder = domain.replace('.','_')

	if "ALL" in file_types:
		from itertools import product
		from string import ascii_lowercase
		# Generate all three letter combinations.
		file_types = ["".join(i) for i in product(ascii_lowercase, repeat=3)]

	for filetype in file_types:
		print(f"[*] Searching for .{filetype} files...")
		gen_queries(domain, filetype, max_pages)
		for i in range(max_threads):
			t = threading.Thread(target=process_queue, args=(proxy,))
			t.daemon = True
			t.start()

	query_queue.join()
	start = time.time()
	gen_results(output_folder)
	print('[*] Execution time: {0:.5f}'.format(time.time() - start))

if __name__ == '__main__':
	main()
