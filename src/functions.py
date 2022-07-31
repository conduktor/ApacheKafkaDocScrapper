from bs4 import BeautifulSoup
from pandas import read_html, concat, DataFrame

class Functions:

    def get_bs_parsed(html):
        return BeautifulSoup(html, "html.parser")

    def to_lowercase_df(df):
        df.columns = df.columns.str.lower()
        return df

    def load_df_from_table(bs, index):
        return Functions.to_lowercase_df(read_html(str(bs.find_all("table", {"class": "data-table"})[index]))[0])

    def load_df_from_ul_table(bs, index):
        full_df = None
        for li in bs.find_all("ul", {"class": "config-list"})[index].find_all("li"):
            h4 = li.find("h4")
            table = li.find("table")
            if h4 is not None and table is not None:
                data = {}
                for tr in table.find("tbody").find_all("tr"):
                    data[tr.find("th").text] = [tr.find("td").text]
                df = DataFrame(data=data)
                df["name"] = h4.find("a")['id']
                if full_df is None:
                    full_df = df
                else:
                    full_df = concat([full_df, df], ignore_index=True)
        return Functions.to_lowercase_df(full_df)

    def load_df_from_ul_li_vertical(bs, index):
        full_df = None
        for li in bs.find_all("ul", {"class": "config-list"})[index].find_all("li"):
            b = li.find("b")
            ul = li.find("ul", {"class": "horizontal-list"})
            if b is not None and ul is not None:
                data = {}
                for li2 in ul.find_all("li"):
                    data[li2.find("b").text] = [li2.text.split(':')[1].strip()]
                df = DataFrame(data=data)
                df["name"] = b.text
                if full_df is None:
                    full_df = df
                else:
                    full_df = concat([full_df, df], ignore_index=True)
        return Functions.to_lowercase_df(full_df)