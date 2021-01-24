from p_acquisition.m_country_data_acquisition import get_country_codes_df
from p_acquisition.m_job_data_acquisition import get_jobs_df, get_top_jobs_by_education_level
from p_acquisition.m_career_info_acquisition import get_career_info_df, setup_conn_engine
from p_reporting.m_report_to_csv import df_to_csv
from p_acquisition.m_arguments_data_acquisition import get_num_arguments_by_vote_tendency

import argparse
import pandas as pd
import os
from sqlalchemy import create_engine


def valid_country_code(country_code):
    if country_code not in list(get_country_codes_df()["country_code"]):
        raise argparse.ArgumentTypeError(f'invalid country code ({country_code})!!!')
    return country_code


def valid_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"invalid directory ({path})!!!")
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
                        help="output directory",
                        default = "data/results",
                        type=valid_path)

    return parser.parse_args()


def get_job_distribution_urban_vs_city():
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

    result = pd.merge(result, job_codes,
                      left_on='normalized_job_code',
                      right_on='job_code',
                      how='left').drop(['normalized_job_code', 'job_code'], axis=1)

    return result


def setup_connection(conn_string = 'sqlite:///data/raw/raw_data_project_m1.db'):
    return create_engine(conn_string)


def main(arguments):
    print("Starting pipeline...")

    motor_conexion = setup_connection()

    df_to_csv(get_job_distribution_urban_vs_city(), arguments.output, "job_distribution_urban_vs_city.csv")
    df_to_csv(get_num_arguments_by_vote_tendency(motor_conexion), arguments.output, "num_arguments_by_vote_tendency.csv")
    df_to_csv(get_top_jobs_by_education_level(motor_conexion), arguments.output, "top_jobs_by_education_level.csv")

    print("Pipeline is complete!")


if __name__ == "__main__":
    arguments = argument_parser()
    main(arguments)