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