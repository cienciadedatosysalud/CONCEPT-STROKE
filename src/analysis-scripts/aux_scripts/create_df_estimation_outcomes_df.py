##### GENERATE A DF FOR GAMM MODEL #####
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import duckdb

def df_model_estimation_outcomes(data_path, df, event_log, traces, freq_traces, trace_theory):
    traces = traces.merge(freq_traces, on=['trace', 'freq_trace'], how='left')
    traces.loc[traces['index_trace']> 10, 'index_trace'] = 'otros'
    traces['rank_trace'] = traces['index_trace']
    traces['jaccard_similarity'] = traces['trace'].apply(lambda x: jaccard_similarity(x, trace_theory))
    fig = traces['jaccard_similarity'].plot.hist().get_figure()
    plt.xlabel('Jaccard similarity', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Histogram jaccard similarity', fontsize=16)
    #plt.xlim((0,1))
    plt.rc('axes', titlesize=14)  # fontsize of the axes title
    plt.savefig('../../outputs/histogram_jaccard_similarity.png')
    plt.close()
    df = df.merge(traces[['patient_id','trace','freq_trace', 'rank_trace', 'jaccard_similarity','perc']], on=['patient_id'], how='left')
    result = event_log.groupby('case:concept:name')['time:timestamp'].agg(['min','max']).reset_index()
    result['dur_trace'] = (result['max']-result['min'])/ np.timedelta64(1, 'D')
    result.rename(columns={'case:concept:name': 'patient_id'},inplace=True)
    df = df.merge(result[['patient_id','dur_trace']], on=['patient_id'], how='left')
    df_ = df[['patient_id','patient_id_st' ,'trace','freq_trace','rank_trace', 'jaccard_similarity', 'dur_trace','perc']]
    traces_ = traces[['patient_id', 'trace', 'freq_trace','perc']]
    con = duckdb.connect(data_path)

    con.sql('''CREATE OR REPLACE TABLE prediction_outcomes_db(
    patient_id VARCHAR,
    patient_id_st VARCHAR,
    trace VARCHAR,
    freq_trace VARCHAR,
    rank_trace VARCHAR,
    jaccard_similarity DOUBLE,
    dur_trace DOUBLE,
    perc DOUBLE)''')
    con.sql("INSERT INTO prediction_outcomes_db SELECT * from df_")

    # con.sql('''CREATE OR REPLACE TABLE traces_db(
    # patient_id VARCHAR,
    # trace VARCHAR,
    # freq_trace BIGINT,
    # perc DOUBLE)''')
    # con.sql("INSERT INTO traces_db SELECT * from traces_")
    con.close()


# SIMPLE JACCARD: without regard to the order of activities

def jaccard_similarity(trace_experimental, trace_theory):
    trace_experimental = set(trace_experimental.split(','))
    trace_theory = set(trace_theory.split(','))
    # Find the intersection
    intersection = len(trace_experimental.intersection(trace_theory))
    # Find the union
    union = len(trace_experimental) + len(trace_theory) - intersection

    # Calculate Jaccard similarity score
    # using length of intersection set divided by length of union set
    return float(intersection) / float(union)



