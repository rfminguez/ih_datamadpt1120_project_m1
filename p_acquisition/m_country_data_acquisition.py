import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_country_codes_df():
    print("Getting country codes data using web scraping")

    # Get country and country codes from HTML using web scraping
    dict_messy = get_messy_dict(get_table_cells())

    # Get a list of clean country codes and country names
    country_codes = get_clean_country_codes(dict_messy)
    country_names = get_clean_country_names(dict_messy)

    return pd.DataFrame.from_dict({"country_code": country_codes, "country_name": country_names})

    #print("Returning country codes and names")
    # Zip the clean data in a dictionary {country_code:country_name} and return the result
    #return dict(zip(country_codes, country_names))


def get_clean_country_names(country_dict):
    country_names = list(country_dict.values())

    # remove non-aphabetic characters at the end of the string
    country_names = list(map(lambda s: re.sub(r"[^\w]$", "", s), country_names))

    # remove content surrounded by parenthesis and squared brackets
    country_names = list(map(lambda s: re.sub(r"\s[\[\(].*", "", s), country_names))

    return country_names


def get_clean_country_codes(country_dict):
    return list(map(lambda s: s[1:3], country_dict.keys()))


def get_messy_dict(cells):
    return {country_code: country_name for country_name, country_code in zip(cells[::2], cells[1::2])}


def get_table_cells():
    return remove_empty_cells(get_cells_text(get_raw_data()))


def remove_empty_cells(cells):
    return [cell for cell in cells if cell != ""]


def get_cells_text(cells):
    return list(map(lambda cell: cell.text.strip(), cells))


def get_raw_data():
    url = "https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.select("table tr td")