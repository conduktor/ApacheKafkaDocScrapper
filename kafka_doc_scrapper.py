from argparse import ArgumentParser
from os.path import isfile
from urllib.parse import urljoin
from re import match
from pickle import dump as pdump, load
from json import dump as jdump
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.transformers import Broker, Consumer, Producer, Topic, Connect, Stream
from src.functions import Functions
from src.utils import Utils

class Scrapper:

    def run(kafka_url, doc_path, transformers, outfile=None, debug_file=None, filter_versions=None):
        if debug_file is None or not isfile(debug_file):
            Utils.log(f"Scraping '{kafka_url}' to get '{doc_path}'...")
            driver = Scrapper._init_web_driver()
            current_html = Scrapper.get_html(driver, urljoin(kafka_url, doc_path))
            current_bs = Functions.get_bs_parsed(current_html)
            versions = [
                {
                    "version": Scrapper.get_current_version(current_bs),
                    "html": current_html
                }
            ]
            previous_versions = Scrapper.get_all_previous_versions(current_bs)
            versions += list(map(lambda x: {"version": x["version"], "html": Scrapper.get_html(driver, urljoin(kafka_url, x["url"]))}, previous_versions))
            versions.sort(key=lambda x: list(map(int, x["version"].split('.'))))
            driver.quit()
        if debug_file is not None and isfile(debug_file):
            Utils.log(f"Reading versions from '{debug_file}'...")
            with open(debug_file, "rb") as f:
                versions = load(f)
        if debug_file is not None and not isfile(debug_file):
            Utils.log(f"Writing the scraping result '{debug_file}'...")
            with open(debug_file, "wb") as f:
                pdump(versions, f)
        if filter_versions is not None:
            versions = list(filter(lambda x: x["version"] in filter_versions.split(','), versions))
        transformed = {}
        for transformer in transformers:
            transformed[transformer.__name__.lower()] = transformer.transform(versions)
        if outfile is None:
            return transformed
        with open(outfile, "w") as f:
            jdump(transformed, f, indent=4)
        
    def _init_web_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_html(driver, url):
        driver.get(url)
        return driver.page_source

    def get_current_version(bs):
        h3 = bs.find_all("h3")
        h3_text = map(lambda x: x.text, h3)
        h3_doc_filtered = filter(lambda x: match("Kafka .* Documentation", x), h3_text)
        return list(h3_doc_filtered)[0].split(' ')[1]

    def get_all_previous_versions(bs):
        a = bs.find_all("a", href=True)
        a_text_href = map(lambda x: (x.text, x['href']), filter(lambda x: x['href'] is not None, a))
        a_doc_filtered = filter(lambda x: match("/\d*/documentation.html", x[1]), a_text_href)
        a_doc_cleaned = map(lambda x: (x[0].lower().replace(".x", ""), x[1]), a_doc_filtered)
        return list(map(lambda x: {"version": x[0], "url": x[1]}, a_doc_cleaned))

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--kafka_url', dest='kafka_url', type=str, help='Main url of Apache Kafka documentation (ex: https://kafka.apache.org).', default="https://kafka.apache.org")
    arg_parser.add_argument('--doc_path', dest='doc_path', type=str, help='Documentation endpoint name (ex: documentation).', default="documentation")
    arg_parser.add_argument('--transformers', dest='transformers', type=str, help='Configuration transformer(s) to run (ex: Broker,Producer).', default="Broker,Consumer,Producer,Topic,Connect,Stream")
    arg_parser.add_argument('--outfile', dest='outfile', type=str, help='File where to write the JSON (if null then the JSON is returned at execution).')
    arg_parser.add_argument('--debug_file', dest='debug_file', type=str, help='File to store and use website HTML content.')
    arg_parser.add_argument('--versions', dest='versions', type=str, help='Runs only on the given versions (ex: 1.1,2.5).')
    arg_parser.add_argument('--silent', dest='silent', help='If true then the program will run without logs.', action='store_true')
    args = arg_parser.parse_args()
    initialized_transformers = map(lambda x: globals()[x], args.transformers.split(','))
    Utils.silent = args.silent
    Scrapper.run(args.kafka_url, args.doc_path, initialized_transformers, outfile=args.outfile, debug_file=args.debug_file, filter_versions=args.versions)