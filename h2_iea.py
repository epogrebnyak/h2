"""

Hydrogen Projects Database
https://www.iea.org/reports/hydrogen-projects-database

"""

import os
import requests
import pandas as pd


def extract_filename(url):
    return url.split("/")[-1]


def download(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


url = (
    "https://iea.blob.core.windows.net/assets/"
    "3e715e9a-65db-4c2a-b636-5e24592fa92a/"
    "IEAHydrogenProjectDatabase.xlsx"
)
filename = extract_filename(url)
if not os.path.exists(filename):
    download(url, filename)


def show_sheets(filename):
    import xlrd

    xls = xlrd.open_workbook(filename, on_demand=True)
    print(xls.sheet_names)


mapper = {
    "Currently operational\n(Y/N)": "oper",
    "MWel": "mw",
    "nm³ H₂/hour": "nm3h",
    "Project name": "name",
}

raw = (
    pd.read_excel(filename, sheet_name=2, skiprows=2).iloc[:, 1:].rename(columns=mapper)
)

raw["_name"] = raw.name.str.lower().map(lambda x: x.strip())

df = raw[mapper.values()]

# number of projects online
# total capacity
# capacity vs output

# https://www.reuters.com/article/us-bp-orsted-hydrogen/bp-orsted-launch-green-hydrogen-project-at-german-oil-refinery-idINKBN27Q0SI?fbclid=IwAR3Rx3hF3iDrVQmZN4HVrFOukuMBqehu03YjjCrNTyMGbujVbSz3GHFgE9E
# 'lingen'
# [x for x in raw.name.str.lower() if 'lingen' in x]


df.nm3h / df.mw  # 217.391304

raw[raw["_name"].str.contains("lingen")].T
