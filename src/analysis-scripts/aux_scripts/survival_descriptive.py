from lifelines import KaplanMeierFitter, CoxPHFitter
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np


def survival_analysis(df_filtered):
    end_study = datetime.date(year=2022, month=12, day=31)
    df_filtered['status'] = True
    df_filtered.loc[df_filtered['exitus_dt'].isna(), 'status'] = False

    df_filtered['survival_in_days'] = (pd.to_datetime(end_study) - df_filtered[
        'admission_emergency_care_dt']) / np.timedelta64(1, 'D')
    df_filtered.loc[df_filtered['exitus_dt'].notna(), 'survival_in_days'] = (df_filtered['exitus_dt'] - df_filtered[
        'admission_emergency_care_dt']) / np.timedelta64(1, 'D')

    fig, ax = plt.subplots()
    kmf = KaplanMeierFitter()
    for value in df_filtered['rank_trace'].unique():
        trace = df_filtered['rank_trace'] == value
        kmf.fit(durations=df_filtered['survival_in_days'][trace], event_observed=df_filtered['status'][trace],
                label='Rank_trace' + str(value))
        kmf.plot_survival_function(
            label=value,
            ax=ax
        )
        ax.set(
            title='Kaplan-Meier survival curves',
            xlabel='Days',
            ylabel='Estimated Probability of Survival'
        )

    fig.savefig('../../outputs/surv_analysis.png')
    plt.close()
    df_filtered1 = df_filtered[['rank_trace', 'survival_in_days', 'status']]
    dummies_rank_trace = pd.get_dummies(df_filtered1["rank_trace"], prefix='trace')
    df_filtered1 = pd.concat([df_filtered1, dummies_rank_trace], axis=1)
    df_filtered1 = df_filtered1.drop("rank_trace", axis=1)

    cph = CoxPHFitter(penalizer=0.1)
    cph.fit(df_filtered1, duration_col='survival_in_days', event_col='status')
    cph.print_summary()



