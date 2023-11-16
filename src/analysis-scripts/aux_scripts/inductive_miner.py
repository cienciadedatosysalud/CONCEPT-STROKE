from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py import convert_to_petri_net, PetriNet, discover_petri_net_inductive
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
from pm4py.algo.decision_mining import algorithm as decision_mining

def inductive_miner_algorithm(event_carac):
    tree = inductive_miner.apply(event_carac)
    gviz = pt_visualizer.apply(tree)
    pn_visualizer.save(gviz, "../../outputs/inductive_miner_tree.png")
    # Convert tree to petri net
    net, initial_marking, final_marking = convert_to_petri_net(tree)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.save(gviz, "../../outputs/inductive_miner_petri_net.png")


def get_points(net_: PetriNet):
    inhospital_fibrinolysis_p: str = None
    inhospital_thrombectomy_p: str = None
    thrombolysis_emergency_p: str = None
    for transition in net_.transitions:
        if transition.label is not None and transition.label == "thrombolysis_emergency_dt":
            arc = transition.in_arcs.pop()  # return a set
            thrombolysis_emergency_p = arc.source.name
            # si es none es un skip
        if transition.label is not None and transition.label == "inhospital_thrombectomy_bl_date_dt":
            arc = transition.in_arcs.pop()  # return a set
            inhospital_thrombectomy_p = arc.source.name
        if transition.label is not None and transition.label == "inhospital_fibrinolysis_bl_date_dt":
            arc = transition.in_arcs.pop()  # return a set
            inhospital_fibrinolysis_p = arc.source.name
            if inhospital_fibrinolysis_p is not None and inhospital_thrombectomy_p is not None and thrombolysis_emergency_p is not None:
                # if fibrinolysis_p is not None:
                break
    # return thrombectomy_p, fibrinolysis_p
    return inhospital_fibrinolysis_p, inhospital_thrombectomy_p, thrombolysis_emergency_p


def get_decision_mining(df, event_log):
    df_carac = df[
        ['patient_id', 'age_nm', 'sex_cd', 'hospital_cd', 'healthcare_area_cd', 'zip_code_cd', 'hospital_type_discharge_cd', 'ct_inhospital_bl', 'mri_inhospital_bl',
         'type_admission_cd', 'antiarrhythmics_prescription_bl', 'antihypertensive_prescription_bl', 'antiaggregants_prescription_bl','fibrinolitics_prescriptions_bl', 
         'modified_rankin_scale_cd','heart_failure_bl','hypertension_bl','diabetes_bl','atrial_fibrillation_bl','valvular_disease_bl']]
         
    event_log = event_log[['case:concept:name','concept:name','time:timestamp']]
    event_carac = event_log.merge(df_carac, left_on='case:concept:name', right_on='patient_id', how='left')
    event_carac['org:resource'] = ''
    
    # only for synthetic data
    np.random.seed(1234)
    remove_n = 3000
    drop_indices = np.random.choice(event_carac.index, remove_n, replace=False)
    event_carac = event_carac.drop(drop_indices)
    ####
    inductive_miner_algorithm(event_carac)
    net, im, fm = discover_petri_net_inductive(event_carac)
    gviz = pn_visualizer.apply(net, im, fm, parameters={pn_visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: True})
    pn_visualizer.save(gviz, '../../outputs/decision_mining_petri.png')
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.save(gviz, '../../outputs/decision_mining_petri_act.png')
    random.seed(1234)
    point_decision = get_points(net)
    for point in point_decision:
        try:
            clf, feature_names, classes = decision_mining.get_decision_tree(event_carac, net, im, fm,
                                                                            decision_point=point)
            importances = clf.feature_importances_
            tree_importances = pd.Series(importances, index=feature_names)
            fig, ax = plt.subplots()
            tree_importances.plot.bar(ax=ax)
            ax.set_title("Feature importances using MDI for point " + point)
            ax.set_xlabel("Mean decrease in impurity")
            fig.tight_layout()
            fig.savefig('../../outputs/barplot_features_importance_' + point + '.png')
            plt.close()
        except ValueError:
            print('It is not possible to carry out the decision mining process for the item: ' + point)

    return point_decision




