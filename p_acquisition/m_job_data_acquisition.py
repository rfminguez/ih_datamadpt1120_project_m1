import requests
import pandas as pd


def get_jobs_df(job_codes_list):
    print("Getting normalized job data using the dataatwork API")

    job_names = [get_job_name(job_code) for job_code in job_codes_list]

    return pd.DataFrame.from_dict({"job_code": job_codes_list, "job_name": job_names})


def get_job_name(job_code):
    print(f"Returning job name corresponding to code: {job_code}")
    return get_job_data(job_code)['title']


def get_job_data(job_code):
    base_url = "http://api.dataatwork.org"
    endpoint = "/v1/jobs/"
    url = f"{base_url}{endpoint}{job_code}"

    return requests.get(url).json()


def get_top_jobs_from_database(education_level, conn):
    sql_query = f"""
        SELECT uuid,
            CASE 
                WHEN dem_education_level IS NULL THEN 'N/A'
                ELSE dem_education_level
            END AS education_level,
            normalized_job_code AS job_code,
            COUNT(normalized_job_code) AS num_jobs 
        FROM career_info
        WHERE education_level = '{education_level}'
        GROUP BY education_level, job_code
        ORDER BY num_jobs DESC
        LIMIT 10
        """

    return list(pd.read_sql(sql_query, conn)["job_code"])


def get_top_jobs_by_education_level(conn):
    education_levels = ["N/A", "high", "medium", "low", "no"]

    result_dict = {level: list(get_jobs_df(get_top_jobs_from_database(level, conn))['job_name']) for
                   level in education_levels}

    result_df = pd.DataFrame.from_dict(result_dict).T.reset_index()
    result_df.columns = ["Education Level", "Top 1 job", "Top 2 job", "Top 3 job", "Top 4 job", "Top 5 job",
                         "Top 6 job", "Top 7 job", "Top 8 job", "Top 9 job", "Top 10 job"]

    return result_df
