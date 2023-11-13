# MetaFireProx

***`metafireprox.py` is a small tool for scraping certain extensions of files from Google Search results for a specific domain using FireProx API.***

## Introduction

The tool performs queries on Google search engine to find specific types of files (pdf, doc, docx, xls, xlsx, ppt, pptx, etc.) being publicly hosted on a web site for a specific domain.
This is useful for Open Source Intelligence gathering to determine what files the organization is leaking to Google search indexers.
To avoid being blocked by Google, the tool is designed to be used with [Fireprox](https://github.com/ustayready/fireprox). 
FireProx leverages the AWS API Gateway to create pass-through proxies that rotate the source IP address with every request.

### Benefits of using FireProx
 * Rotates IP address with every request
 * Configure separate regions
 * All HTTP methods supported
 * All parameters and URI's are passed through
 * Create, delete, list, or update proxies
 * Spoof X-Forwarded-For source IP header by requesting with an X-My-X-Forwarded-For header

## Usage
```shell
usage: metafireprox.py [-h] -d DOMAIN -x PROXY -e FILE_TYPES [-o OUTPUT_FOLDER] [-p MAX_PAGES] [-t MAX_THREADS] [-w DELAY]

Scrape certain extensions of files from Google Search results for a specific domain using FireProx API

optional arguments:
  -h, --help        show this help message and exit
  -d DOMAIN         Domain to search
  -x PROXY          FireProx API URL
  -e FILE_TYPES     File types to download (pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx). To search all 17,576 three-letter "ALL"
  -o OUTPUT_FOLDER  The output folder where the results will be stored
  -p MAX_PAGES      Google search pages to enumerate (default:1000)
  -t MAX_THREADS    Number of threads per extension (default:5)
  -w DELAY          Specify the delay (in seconds) to avoid being fingerprinting
```

**Create a new API gateway proxy in a specific AWS region (example: us-west-1) using https://www.google.com URL end-point**

```shell
python3 fire.py --access_key <ACCESS_KEY> --secret_access_key <SECRET_ACCESS_KEY> --region us-west-1 --command create --url https://www.google.com
```

**Fetch all documents with `pdf,xls,doc,docx,xlsx,ppt,pptx` extensions from Google search using 10 threads with a maximum of 1000 pages for `microsoft.com`**

```shell
python3 metafireprox.py -d microsoft.com -e pdf,xls,doc,docx,xlsx,ppt,pptx -t 10 -p 1000 -x https://xxxxxxxxxx.execute-api.us-west-1.amazonaws.com/apps/
```
