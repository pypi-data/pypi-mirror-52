# Finance scraper

## Description

This repository contains a Extract-Transform-Load (ETL) pipeline which extracts security
data details from pages on [morningstar.fr](http://tools.morningstar.fr/fr/stockreport/default.aspx?Site=fr&id=0P0001A178&LanguageId=fr-FR&SecurityToken=0P0001A178]3]0]E0WWE$$ALL,DREXG$XHEL,DREXG$XLON,DREXG$XNYS). The steps of the pipeline are:
* extract: scrape web pages and save them raw on AWS S3
* transform: parse raw web pages and store the results in a CSV file, then store in S3
* load: copy the CSV file into a PostgresSQL database

## Installation
### Prerequisites
`finance-scraping` was written in Python 3.6. The following packages are required and will be installed along with `finance-scraping`:
* requests >= 2.22
* BeautifulSoup4 >= 4.7.1
* psycopg2 >= 2.8

You need to install PostgresSQL, and create a database to load data into. Take note of the user name and password with write privileges to this database, as you will need these during the configuration of `finance-scraping`.

### Installation and configuration
* Run `pip install finance-scraping`.
* You can launch unit tests by running `bash run_tests.sh` from the `tests` folder.
* Run `finance-scraping -c` to set the configuration of the scraper. You will be prompted to enter configuration values, which are saved in `~/.bashrc`.
* If you plan to run `finance-scraping` on an EC2 instance launched with an instance role, you can set the parameters `profile` as `None`.

## How to run
To run the entire ETL pipeline, run `python main.py -etl`. You can also run `finance-scraping` with any of the optional arguments `-e`, `-t` or `-l` to run an individual step. It is possible to specify the date parameter `-d` with `-t` and/or `-l` to process data scraped on a specific date. For more information run help with `python main.py -h`.

### Schdule runs with Apache Airflow
* Read the [Airflow documentation](https://airflow.apache.org/index.html) to install and configure Airflow for your system.
* Amend the file `finance_scraping_dag.py` from the `finance_scraping` folder with your scheduling preferences and copy it into the `dags` folder of your Airflow installation before starting the scheduler.
