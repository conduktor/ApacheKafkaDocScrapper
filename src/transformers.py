from src.functions import Functions
from pandas import concat
from src.utils import Utils

class Transformer:

    common_configuration =  [
        {
            "versions": ["0.7"],
            "function": Functions.load_df_from_table,
            "find": lambda bs, id_class: bs.find("code", string=id_class) 
        },
        {
            "versions": ["0.8.0", "0.8.1", "0.8.2", "0.9.0", "0.10.0", "0.10.1", "0.10.2", "0.11.0", "1.0", "1.1", "2.0", "2.1", "2.2", "2.3"],
            "function": Functions.load_df_from_table,
            "find": lambda bs, id_class: bs.find("a", {"id": id_class})
        },
        {
            "versions": ["2.4"],
            "function": Functions.load_df_from_ul_li_vertical,
            "find": lambda bs, id_class: bs.find("a", {"id": id_class})
        },
        {
            "versions": ["2.5", "2.6", "2.7", "2.8", "3.0", "3.1", "3.2"],
            "function": Functions.load_df_from_ul_table,
            "find": lambda bs, id_class: bs.find("a", {"id": id_class})
        }
    ]

    class Mapper:

        def map(version, bs, configuration, ids):
            Utils.log(f"Finding configuration for version '{version}'...")
            final_columns = ["name", "value"]
            func_find = Transformer.Mapper._func_find(version, configuration)
            if func_find is not None:
                full_df = None
                for id_class in ids:
                    df = func_find[0](bs, id_class, func_find[1])
                    if df is not None:
                        df = df.rename(columns={
                            "property": "name",
                            "default": "value",
                            "default:": "value"
                        })[final_columns]
                        full_df = df if full_df is None else concat([full_df, df], ignore_index=True)
                return full_df

        def _func_find(version, configuration):
            filtered = list(filter(lambda x: version in x["versions"], configuration))
            if len(filtered) > 0:
                return filtered[0]["function"], filtered[0]["find"]

    def transform(versions, configuration, ids, filters=None):
        transformed = []
        for version_config in versions:
            df =  Transformer.Mapper.map(version_config["version"], Functions.get_bs_parsed(version_config["html"]), configuration, ids)
            if df is not None:
                df = df.fillna("null").replace(r'^"*$', "", regex=True)
                if filters is not None:
                    version_filter = list(filter(lambda x: x["version"] == version_config["version"], filters))
                    if len(version_filter) > 0:
                        Utils.log("Applying filter...")
                        df = version_filter[0]["function"](df)
                transformed.append({
                    "version": version_config["version"],
                    "configs": list(sorted(df.to_dict('records'), key=lambda x: x["name"]))
                })
            else:
                Utils.log("Config type not present in that version or version not handled.")
        return transformed


class Broker:

    def transform(versions):
        Utils.log("Running Broker config transformation...")
        return Transformer.transform(versions, Transformer.common_configuration, ["brokerconfigs", "kafka.server.KafkaConfig"])

class Consumer:

    def transform(versions):
        Utils.log("Running Consumer config transformation...")
        return Transformer.transform(versions, Transformer.common_configuration, ["consumerconfigs", "oldconsumerconfigs", "newconsumerconfigs", "kafka.consumer.ConsumerConfig"])

class Producer:

    def transform(versions):
        Utils.log("Running Producer config transformation...")
        return Transformer.transform(
            versions, 
            Transformer.common_configuration,
            ["producerconfigs", "oldproducerconfigs", "newproducerconfigs", "kafka.producer.ProducerConfig"],
            filters=[
                {
                    "version": "0.7",
                    "function": lambda df: df[~df["name"].isin(["Options for Asynchronous Producers (producer.type=async)"])]
                }
            ]
        )

class Topic:

    def transform(versions):
        Utils.log("Running Topic config transformation...")
        return Transformer.transform(versions, Transformer.common_configuration, ["topicconfigs"])

class Connect:

    def transform(versions):
        Utils.log("Running Connect config transformation...")
        return Transformer.transform(versions, Transformer.common_configuration, ["connectconfigs", "sourceconnectconfigs", "sinkconnectconfigs"])

class Stream:

    def transform(versions):
        Utils.log("Running Stream config transformation...")
        return Transformer.transform(versions, Transformer.common_configuration, ["streamsconfigs"])