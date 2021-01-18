import pandas as pd
from sqlalchemy import create_engine


def setup_conn_engine(conn_string):
    return create_engine(conn_string)


def get_total_jobs_number(conn_engine, country_code=None):
    country_code_filter = f'AND country_code = "{country_code.upper()}"' if country_code else ""

    sql_query = f"""
    SELECT COUNT(normalized_job_code) AS TOTAL_JOBS
    FROM career_info JOIN country_info
    ON career_info.uuid = country_info.uuid 
    WHERE normalized_job_code IS NOT NULL
    {country_code_filter}
    """

    result = float(pd.read_sql(sql_query, conn_engine)["TOTAL_JOBS"][0])

    if result == 0:
        raise Exception(f"No entries for the country code {country_code}!!!")

    return result


def get_career_info_df(conn_engine, country_code=None):
    print("Getting career info data from the sqlite database")

    country_code_filter = f'HAVING country_code = "{country_code.upper()}"' if country_code else ""

    sql_query = f"""
    SELECT normalized_job_code, 
        country_code, 
        CASE rural
            WHEN 'urban'
                THEN 'No'
            WHEN 'city'
                THEN 'No'
            WHEN 'Non-Rural'
                THEN 'No'
            ELSE
                'Yes'
        END Rural_Area, 
        COUNT(career_info.uuid) AS Quantity, 
        ROUND(COUNT(career_info.uuid) / {get_total_jobs_number(conn_engine, country_code)} * 100, 2) AS Percentage
    FROM career_info 
    JOIN country_info
    ON career_info.uuid = country_info.uuid
    WHERE normalized_job_code IS NOT NULL 
    GROUP BY Rural_Area, country_code, normalized_job_code
    {country_code_filter}
    """

    return pd.read_sql(sql_query, conn_engine)