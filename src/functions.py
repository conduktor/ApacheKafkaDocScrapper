from bs4 import BeautifulSoup
from pandas import read_html, concat, DataFrame
from re import sub
from boltons.iterutils import remap

class Functions:

    def get_bs_parsed(html):
        return BeautifulSoup(html, "html.parser")

    def to_lowercase_df(df):
        df.columns = df.columns.str.lower()
        return df

    def load_df_from_table(bs, id_class, find_func):
        a = find_func(bs, id_class)
        if a is not None:
            table = str(a.parent.find_next_sibling("table"))
            return Functions.to_lowercase_df(read_html(table)[0])

    def load_df_from_ul_table(bs, id_class, find_func):
        a = find_func(bs, id_class)
        if a is not None:
            full_df = None
            ul = str(a.parent.find_next_sibling("ul", {"class": "config-list"}))
            for li in Functions.get_bs_parsed(ul).find_all("li"):
                h4 = li.find("h4")
                table = li.find("table")
                if h4 is not None and table is not None:
                    data = {}
                    for tr in table.find("tbody").find_all("tr"):
                        data[tr.find("th").text] = [tr.find("td").text]
                    df = DataFrame(data=data)
                    df["name"] = h4.find("a")['id']
                    df["description"] = li.find("p").text.strip()
                    full_df = df if full_df is None else concat([full_df, df], ignore_index=True)
            return Functions.to_lowercase_df(full_df)

    def load_df_from_ul_li_vertical(bs, id_class, find_func):
        a = find_func(bs, id_class)
        if a is not None:
            full_df = None
            ul = str(a.parent.find_next_sibling("ul", {"class": "config-list"}))
            for li in Functions.get_bs_parsed(ul).find_all("li"):
                b = li.find("b")
                ul = li.find("ul", {"class": "horizontal-list"})
                if b is not None and ul is not None:
                    data = {}
                    for li2 in ul.find_all("li"):
                        data[li2.find("b").text] = [li2.text.split(':')[1].strip()]
                    df = DataFrame(data=data)
                    df["name"] = b.text
                    tag = Functions.get_bs_parsed(sub("<b.*</b>", "", sub('<ul.*</ul>|\n', "", sub("<code>|</code>", "'", str(li)))).replace(':', '', 1))
                    df["description"] = ''.join(tag.findAll(text=True)).strip()
                    if full_df is None:
                        full_df = df
                    else:
                        full_df = concat([full_df, df], ignore_index=True)
            return Functions.to_lowercase_df(full_df)

    def delete_attr_from_config(config, filters):
        return remap(config, visit=lambda _, key, __: key not in filters)

