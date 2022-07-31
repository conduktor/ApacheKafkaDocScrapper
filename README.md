# Apache Kafka Documentation Scrapper
Fetch Apache Kafka configuration documentation into a JSON file.
## Supported configuration
- Broker
## How to use it
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