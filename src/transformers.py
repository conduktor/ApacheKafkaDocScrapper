from src.functions import Functions

class Broker:

    class Mapper:

        def map(version, bs):
            print(f"Finding configuration for version '{version}'...")
            final_columns = ["name", "value"]
            if version in ("0.7", "0.8.0", "0.8.1", "0.8.2", "0.9.0", "0.10.0", "0.10.1", "0.10.2", "0.11.0", "1.0", "1.1", "2.0", "2.1", "2.2", "2.3"):
                return Functions.load_df_from_table(bs, 0).rename(columns={
                    "property": "name",
                    "default": "value",
                })[final_columns]
            if version in ("2.4"):
                return Functions.load_df_from_ul_li_vertical(bs, 0).rename(columns={
                    "default": "value"
                })[final_columns]
            if version in ("2.5", "2.6", "2.7", "2.8", "3.0", "3.1", "3.2"):
                return Functions.load_df_from_ul_table(bs, 0).rename(columns={
                    "default:": "value"
                })[final_columns]
            raise Exception(f"Version not handled.") 

    def transform(versions):
        print("Running Broker config transformation...")
        transformed = []
        for config in versions:
            df =  Broker.Mapper.map(config["version"], Functions.get_bs_parsed(config["html"])).fillna("null").replace(r'^"*$', "", regex=True)
            transformed.append({
                "version": config["version"],
                "configs": list(sorted(df.to_dict('records'), key=lambda x: x["name"]))
            })
        return transformed