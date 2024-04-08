import matplotlib.pyplot as plt
import pm4py
import pandas as pd
import numpy as np
import duckdb
from pm4py.objects.conversion.log import converter as log_converter

def import_data_and_convert_to_event_log(data_path):
    con = duckdb.connect(data_path)
    con.sql('''CREATE OR REPLACE VIEW patient_view AS 
    SELECT *, CASE 
        WHEN inhospital_thrombectomy_bl = TRUE THEN hospital_intervention_date_dt
    END as inhospital_thrombectomy_bl_date_dt,
    CASE 
        WHEN inhospital_fibrinolysis_bl = TRUE THEN hospital_intervention_date_dt
    END as inhospital_fibrinolysis_bl_date_dt,
    CASE 
        WHEN thrombolysis_emergency_dt is NULL THEN 0 ELSE 1
    END as thrombolysis_emergency_bl
    FROM main.patient ''')
    df = con.sql("SELECT * FROM patient_view").df()
    ## TO use this columns in some models and decision mining
    df[['hospital_cd','healthcare_area_cd','socioeconomic_level_cd','modified_rankin_scale_cd']] = df[['hospital_cd','healthcare_area_cd','socioeconomic_level_cd','modified_rankin_scale_cd']].apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
    df.replace({False: 0, True: 1}, inplace = True)

    df_all = df
    df = df.loc[:,df.columns.str.contains('patient_id|_dt') & ~df.columns.str.contains('prescription|exitus|barthel|date_first_readmissions_30days_all_cause_dt')]
    df = pd.melt(df, id_vars='patient_id')
    # Sort df by time
    df.sort_values(['patient_id', 'value'], ascending=[False, True],inplace=True)
    df.dropna(inplace = True)
    df.rename(columns={'value': 'time:timestamp', 'patient_id': 'case:concept:name', 'variable': 'concept:name'},inplace=True)
    # Convert to a event log object
    event_log_:pm4py.objects.log.obj.EventLog = log_converter.apply(df)
    result = []
    for event_ in event_log_:
        patient_id = event_._attributes['concept:name']
        event_list = [ac['concept:name'] for ac in event_._list]
        event_list = ','.join(event_list)
        result.append({
            'patient_id':patient_id,
            'trace': event_list})
    result = pd.DataFrame(result)
    unique_traces = result.groupby(['trace']).size().reset_index(name='freq_trace')
    result = result.merge(unique_traces, on='trace', how='left')
    unique_traces = unique_traces.sort_values('freq_trace', ascending=False)
    unique_traces['index_trace'] = np.arange(len(unique_traces)) + 1
    unique_traces['cumsum'] = np.cumsum(unique_traces['freq_trace'])
    unique_traces['perc'] = unique_traces['cumsum']/sum(unique_traces['freq_trace'])
    
    unique_traces_ = unique_traces[unique_traces['perc'] <= 0.9]
    
    
    fig=unique_traces_.plot(kind='bar',x = 'index_trace', y = 'freq_trace', figsize=(45, 20), fontsize=20).get_figure()
    plt.xlabel('Index trace', fontsize = 24)
    plt.ylabel('Frequency', fontsize = 24)
    plt.title('Barplot unique traces', fontsize = 28)
    #plt.rc('axes', titlesize=8)  # fontsize of the axes title
    plt.xticks(np.arange(0, len(unique_traces_), 4), fontsize=20,rotation=90)
    plt.savefig('../../outputs/barplot_unique_traces.png')
    plt.close()
    df['registration_type'] = 'completed'
    df['resource_id'] = 'employee'
    df['activity_instance'] = range(1, len(df) + 1)
    con.sql(''' CREATE OR REPLACE TABLE event_log(	"case:concept:name" VARCHAR,
    "concept:name" VARCHAR,
    "time:timestamp" TIMESTAMP,
    registration_type VARCHAR,
    resource_id VARCHAR,
    activity_instance BIGINT)''')
    con.sql("INSERT INTO event_log SELECT * from df")
    con.close()
    
    
    return df, result, unique_traces, df_all



def check_dates_hospital_emergency(data_path):
    con = duckdb.connect(data_path)
    df = con.sql("SELECT * FROM patient_view").df()
    con.close()
    # emergency
    emergency_care_admission_date = ['admission_emergency_care_dt',
                  'triage_emergency_care_dt',
                  'first_asisstance_medical_dt',
                  'admission_to_observation_ward_dt',
                  'internal_neurology_consultation_dt',
                  'ct_mri_dt',
                  'thrombolysis_emergency_dt',
                  'discharge_from_emergency_dt',
                  'nihss_score_date_dt']
    df_emergency = df[emergency_care_admission_date]
    df_emergency.dropna(inplace = True)
    p = ((df_emergency.iloc[:,0:len(emergency_care_admission_date)].values >= df_emergency[['admission_emergency_care_dt']].values) & (df_emergency.iloc[:,
          0:len(emergency_care_admission_date)].values <= df_emergency[['discharge_from_emergency_dt']].values)).all(axis=1)
    print('There are', np.count_nonzero(p==False), 'errors in emergency dates, if there are errors they may be dates outside the limits or there may be dates without having entered the emergency')
    # hospital
    hospital_admission_date = ['hospital_admission_date_dt',
                            'hospital_intervention_date_dt',
                            'hospital_discharge_date_dt',
                             'modified_rankin_scale_dt','inhospital_thrombectomy_bl_date_dt','inhospital_fibrinolysis_bl_date_dt']
    df_hospital = df[hospital_admission_date]
    df_hospital.dropna(inplace = True)
    p = ((df_hospital.iloc[:,0:len(hospital_admission_date)].values >= df_hospital[['hospital_admission_date_dt']].values) & (df_hospital.iloc[:,
          0:len(hospital_admission_date)].values <= df_hospital[['hospital_discharge_date_dt']].values)).all(axis=1)
    print('There are', np.count_nonzero(p==False), 'errors in hospital dates, if there are errors they may be dates outside the limits or there are dates without having entered the hospital')
    df.dropna(inplace = True)
    p = (df.loc[(df['hospital_admission_date_dt'] >= df['admission_emergency_care_dt']) & (df['hospital_admission_date_dt'] < df['discharge_from_emergency_dt'])])
    print('There are', len(p), 'errors in hospital dates with emergency dates, the hospital admission date is between the emergency admission and discharge date (included).')

def filter_for_k_freq_traces(event_log, traces, freq_traces, df, k):

    filtered_event_log = pm4py.filter_variants_top_k(event_log, k)
    traces_filtered = traces[traces['patient_id'].isin(filtered_event_log['case:concept:name'].unique())]
    freq_traces_filtered = freq_traces[freq_traces['trace'].isin(traces_filtered['trace'].unique())]
    freq_traces_filtered = freq_traces_filtered.sort_values('freq_trace', ascending = False)
    freq_traces_filtered['rank_trace'] = np.arange(len(freq_traces_filtered))+1
    traces_filtered = traces_filtered.merge(freq_traces_filtered, on=['trace','freq_trace'], how='left')
    df_filtered = df[df['patient_id'].isin(traces_filtered['patient_id'])]
    df_filtered = df_filtered.merge(traces_filtered[['freq_trace','rank_trace','patient_id']], on = 'patient_id', how = 'left')
    traces_filtered = traces_filtered.sort_values('rank_trace')
    traces_filtered.reset_index(drop=True, inplace=True)
    col_names = ['rank_trace', 'freq_abs', 'freq_rel']
    data = freq_traces_filtered[['rank_trace','freq_trace']]
    data['freq_rel'] = (data['freq_trace']*100)/len(df)

    return filtered_event_log, df_filtered, traces_filtered




