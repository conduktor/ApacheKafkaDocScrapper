# Apache Kafka Documentation Scrapper
Fetch Apache Kafka configuration documentation into a JSON file.
## Supported configuration
- Broker
- Consumer
- Producer
- Topic
- Connect
- Stream
## How to use it
### Parameters
- *kafka_url*: Main url of Apache Kafka documentation (ex: https://kafka.apache.org).
- *doc_path*: Documentation endpoint name (ex: documentation).
- *transformers*: Configuration transformer(s) to run (ex: Broker,Producer).
- *outfile*: File where to write the JSON (if null then the JSON is returned at execution).
- *debug_file*: File to store and use website HTML content.
- *versions*: Runs only on the given versions (ex: 1.1,2.5).
### To produce a file
```
python kafka_doc_scrapper.py --transformers Broker --outfile kafka_doc_config_versions.json
```
### In code
```
from kafka_doc_scrapper import Scrapper, Broker
version_config = Scrapper.run("https://kafka.apache.org", "documentation", [Broker], outfile="kafka_doc_config_versions.json", debug_file="kafka_doc_html.obj")
```
## JSON file format
```
{
    "<config_type>": [
        {
            "version": "",
            "configs": [
                {
                    "name": "",
                    "value": ""
                }
            ]
        }
    ]
}
```
#### If you want more supported configuration, you can hire me at [Upwork](https://www.upwork.com/workwith/charlescogoluegnes).