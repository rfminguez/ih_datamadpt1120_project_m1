import pandas as pd


def get_base_query():
    base_query = """
    WITH aux_t1 AS (
        SELECT uuid,
            CASE 
                WHEN question_bbi_2016wave4_basicincome_vote = 'I would vote for it' THEN 'In Favor'
                WHEN question_bbi_2016wave4_basicincome_vote = 'I would probably vote for it' THEN 'In Favor'
                WHEN question_bbi_2016wave4_basicincome_vote = 'I would vote against it' THEN 'Against'
                WHEN question_bbi_2016wave4_basicincome_vote = 'I would probably vote against it' THEN 'Against'
                WHEN question_bbi_2016wave4_basicincome_vote = 'I would not vote' THEN 'Not Vote'
                ELSE 'N/A'
            END AS vote,
            question_bbi_2016wave4_basicincome_argumentsfor AS arguments_for,
            question_bbi_2016wave4_basicincome_argumentsagainst AS arguments_against
        FROM poll_info
    )
    """
    return base_query


def num_arguments_for(vote_tendency, conn):
    sql_num_votes_for = f"""
    SELECT vote, COUNT(*) AS num_arguments_for
    FROM aux_t1 
    WHERE vote='{vote_tendency}' AND arguments_for!='None of the above' 
    """

    return pd.read_sql(get_base_query() + sql_num_votes_for, conn)["num_arguments_for"][0]


def num_arguments_against(vote_tendency, conn):
    sql_num_votes_for = f"""
    SELECT vote, COUNT(*) AS num_arguments_against
    FROM aux_t1 
    WHERE vote='{vote_tendency}' AND arguments_against!='None of the above' 
    """

    return pd.read_sql(get_base_query() + sql_num_votes_for, conn)["num_arguments_against"][0]


def get_num_arguments_by_vote_tendency(conn):
    result_dict = {
        "Number of Pro Arguments": {
            "In Favor": num_arguments_for('In Favor', conn),
            "Against": num_arguments_for('Against', conn),
            "Not Vote": num_arguments_for('Not Vote', conn)
        },
        "Number of Cons Arguments": {
            "In Favor": num_arguments_against('In Favor', conn),
            "Against": num_arguments_against('Against', conn),
            "Not Vote": num_arguments_against('Not Vote', conn)
        }
    }

    print("Returning Data about Arguments and Vote Tendency")

    result_df = pd.DataFrame.from_dict(result_dict).reset_index()
    result_df.columns = ["Vote Tendency", "Number of Pro Arguments", "Number of Cons Arguments"]

    return result_df
