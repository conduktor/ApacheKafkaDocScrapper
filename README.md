# Apache Kafka Documentation Scrapper

Fetch Apache Kafka configuration documentation into a JSON file.

The source of the data for: https://learn.conduktor.io/kafka/kafka-options-explorer/
File to update when there is a new version: https://github.com/conduktor/conduktor.io/blob/web/apps/kafkademy/kafka_options.json

## How to use it

### Install

```
pip -r requirements.txt
```

### Fetch a specific new version

```
python kafka_doc_scrapper.py --outfile kafka_doc_config_versions.json --versions 3.8
```

### All parameters

- *kafka_url*: Main url of Apache Kafka documentation (ex: https://kafka.apache.org).
- *doc_path*: Documentation endpoint name (ex: documentation).
- *transformers*: Configuration transformer(s) to run (ex: Broker,Producer).
- *outfile*: File where to write the JSON (if null then the JSON is returned at execution).
- *debug_file*: File to store and use website HTML content.
- *versions*: Runs only on the given versions (ex: 1.1,2.5).

### In code
```
from kafka_doc_scrapper import Scrapper, Broker
version_config = Scrapper.run("https://kafka.apache.org", "documentation", [Broker], outfile="kafka_doc_config_versions.json", debug_file="kafka_doc_html.obj")
```
