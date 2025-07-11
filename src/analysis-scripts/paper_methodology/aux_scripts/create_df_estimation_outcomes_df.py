##### GENERATE A DF FOR MODEL #####
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import duckdb
from pm4py.algo.conformance.alignments.edit_distance.variants import edit_distance
from pm4py.objects.log.obj import EventLog, Trace, Event   


def df_model_estimation_outcomes(data_path, df, event_log, traces, freq_traces, trace_theory):
    traces = traces.merge(freq_traces, on=['trace', 'freq_trace'], how='left')
    traces.loc[traces['index_trace']> 10, 'index_trace'] = 'others'
    traces['rank_trace'] = traces['index_trace']
    traces['jaccard_similarity'] = traces['trace'].apply(lambda x: jaccard_similarity(x, trace_theory))
    theory_trace = ['admission_emergency_care_dt','triage_emergency_care_dt','first_asisstance_medical_dt',
    'internal_neurology_consultation_dt','ct_mri_dt','admission_to_observation_ward_dt','thrombolysis_emergency_dt','discharge_from_emergency_dt']    
    # Crear un log vacío para la traza teórica
    log_theory = EventLog()
    
    # Convertir la traza teórica en un log
    theory_trace_ = Trace()
    for actividad in theory_trace:
        theory_trace_.append(Event({"concept:name": actividad}))
        
    log_theory.append(theory_trace_)
    
    # Inicializar una lista para almacenar las distancias
    dists = []
    
    # Convertir cada cadena de caracteres en una lista de actividades y luego en un log
    for trace_str in traces['trace']:
        trace_act = trace_str.split(',')
        trace_log = EventLog()
        trace_trace = Trace()
        for act in trace_act:
            trace_trace.append(Event({"concept:name": act}))
        
        trace_log.append(trace_trace)
    
        dists_ = edit_distance.apply(trace_log, log_theory)
        dists_ = dists_[0]['fitness']
        dists.append(dists_)
    
    # Añadir las distancias calculadas al DataFrame
    traces['fitness_levenshtein'] = dists
    fig = traces['fitness_levenshtein'].plot.hist(bins=20).get_figure()
    plt.xlabel('Fitness (Levenshtein)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Histogram fitness (Levenshtein)', fontsize=16)
    #plt.xlim((0,1))
    plt.rc('axes', titlesize=14)  # fontsize of the axes title
    plt.savefig('../../../outputs/histogram_fitness_levenshtein.png')
    plt.savefig('../../../outputs/histogram_fitness_levenshtein.tif',dpi=300)
    plt.close()
    
    fig = traces['fitness_levenshtein'].plot.kde(bw_method=0.1).get_figure()
    plt.xlabel('Fitness Levenshtein', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.title('Density Plot of fitness Levenshtein', fontsize=16)
    plt.xlim(0, 1)
    plt.rc('axes', titlesize=14) 
    plt.savefig('../../../outputs/density_plot_fitness_levenshtein.png')
    plt.close()
    
    
    fig = traces['jaccard_similarity'].plot.hist(bins=20).get_figure()
    plt.xlabel('Jaccard similarity', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Histogram Jaccard similarity', fontsize=16)
    #plt.xlim((0,1))
    plt.rc('axes', titlesize=14)  # fontsize of the axes title
    plt.savefig('../../../outputs/histogram_jaccard_similarity.png')
    plt.close()
    
    
    fig = traces['jaccard_similarity'].plot.kde(bw_method=0.1).get_figure()
    plt.xlabel('Jaccard similarity', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.title('Density Plot of jaccard similarity', fontsize=16)
    plt.xlim(0, 1)
    plt.rc('axes', titlesize=14) 
    plt.savefig('../../../outputs/density_plot_jaccard_similarity.png')
    plt.close()
    
    
    df = df.merge(traces[['patient_id','trace','freq_trace', 'rank_trace', 'jaccard_similarity','fitness_levenshtein','perc']], on=['patient_id'], how='left')
    result = event_log.groupby('case:concept:name')['time:timestamp'].agg(['min','max']).reset_index()
    result['dur_trace'] = (result['max']-result['min'])/ np.timedelta64(1, 'D')
    result.rename(columns={'case:concept:name': 'patient_id'},inplace=True)
    df = df.merge(result[['patient_id','dur_trace']], on=['patient_id'], how='left')
    df_ = df[['patient_id','patient_id_st' ,'trace','freq_trace','rank_trace', 'jaccard_similarity','fitness_levenshtein', 'dur_trace','perc']]
    traces_ = traces[['patient_id', 'trace', 'freq_trace','perc']]
    con = duckdb.connect(data_path)

    con.sql('''CREATE OR REPLACE TABLE prediction_outcomes_db(
    patient_id VARCHAR,
    patient_id_st VARCHAR,
    trace VARCHAR,
    freq_trace VARCHAR,
    rank_trace VARCHAR,
    jaccard_similarity DOUBLE,
    fitness_levenshtein DOUBLE,
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

