from p_acquisition.m_country_data_acquisition import get_country_codes_df
from p_acquisition.m_job_data_acquisition import get_jobs_df
from p_acquisition.m_career_info_acquisition import get_career_info_df, setup_conn_engine
from p_reporting.m_report_to_csv import df_to_csv

import argparse
import pandas as pd


def valid_country_code(country_code):
    if country_code not in list(get_country_codes_df()["country_code"]):
        raise argparse.ArgumentTypeError('invalid country code!!!')
    return country_code


def valid_path(path):
    return path


def argument_parser():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description='Pipeline main script')

    parser.add_argument("-c",
                        "--country",
                        dest='country',
                        help='valid country code',
                        type=valid_country_code)

    parser.add_argument("-o",
                        "--output",
                        dest="output",
                        help="output csv path",
                        default = "data/results/output.csv",
                        type=valid_path)

    return parser.parse_args()


def main(arguments):
    print("Starting pipeline...")

    # Descarga info de carreras desde base de datos sqlite
    db_path = 'sqlite:///./data/raw/raw_data_project_m1.db'
    career_info = get_career_info_df(setup_conn_engine(db_path), arguments.country)

    # Descarga los codigos y nombres de paises usando web scraping
    country_codes = get_country_codes_df()

    # Descarga los trabajos normalizados basándose en su id usando una API
    job_codes = get_jobs_df(list(career_info["normalized_job_code"].unique()))

    # Join dataframes
    result = pd.merge(career_info, country_codes,
                      left_on='country_code',
                      right_on='country_code',
                      how='left').drop('country_code', axis=1)

    print(result.head())

    result = pd.merge(result, job_codes,
                      left_on='normalized_job_code',
                      right_on='job_code',
                      how='left').drop(['normalized_job_code', 'job_code'], axis=1)

    # Save to CSV
    df_to_csv(result, arguments.output)

    print("Pipeline is complete!")


if __name__ == "__main__":
    arguments = argument_parser()
    main(arguments)