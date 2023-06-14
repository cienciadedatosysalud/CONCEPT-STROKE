![Logo of the project](https://cienciadedatosysalud.org/wp-content/uploads/CONCEPT-h-color.png)

# CONCEPT-STROKE 
CONCEPT-STROKE is a study analysing the acute care received by patients with acute ischaemic stroke where the general aim is to estimate the effectiveness and efficiency of the care pathway followed by acute ischaemic stroke patients, using Real World Data (RWD) routinely collected by five Spanish Regional Health Systems.

### CONCEPT Project Coordinator
**[Enrique Bernal-Delgado MD PhD](https://orcid.org/0000-0002-0961-3298)**

Lead Researcher Senior Researcher in Healthcare Services and Policies.

Area of knowledge: Analysis of unjustified variations in healthcare performance. Comparative analysis of health systems. Methodology of research using real-world data.


## Main specific aims:

- To discover the actual care pathway of Acute Ischemic Stroke, from the admission to an emergency room in a public hospital to the appearance of an event of interest after discharge. 
- To compare that care pathway discovered with the theoretical pathway that a patient should follow according to the 
regional Stroke Plans.
- To analyse the impact of specific care interventions within and across care paths, in terms of patients survival.
- To compare the traditional analytical methods with process mining methods in terms of modeling quality, prediction performance and information provided.

## Analytical pipeline

### Project structure
```shell
.
├── analysis_concept.html
├── analysis_concept.qmd
├── inputs
│   └── synthetic_data_concept_stroke.csv
├── outputs
│   ├── alpha_miner_petri_net.png
│   ├── barplot_features_importance.png
│   ├── barplot_unique_traces.png
│   ├── confusion_matrix_predictions_bupar.png
│   ├── decision_mining_petri_act.png
│   ├── decision_mining_petri.png
│   ├── df_gam.csv
│   ├── directly_follows_graph_filtered.png
│   ├── directly_follows_graph.png
│   ├── gam_model.png
│   ├── heuristic_miner.png
│   ├── inductive_miner_petri_net.png
│   ├── inductive_miner_tree.png
│   ├── surv_analysis.png
│   ├── workflow_net_filtered.png
│   └── workflow_net.png
└── README.md

```
#### Main files

- **analysis_concept.qmd**: Quarto document containing the entire analytical pipeline (code, results and information on the analysis methodology followed).
- **analysis_concept.html**: Output self-contained HTML file containing the analysis results and additional project information.
- **synthetic_data_concept_stroke.csv**: Synthetic data compliant with the Common Data Model.

## R dependencies
Version of Rbase used: **4.2.2**

Version of [Quarto](https://quarto.org/) used: **1.1.149**

| library  |  version  | link |
|---|---|---|
| bupaverse  |  0.1.0 | https://doi.org/10.1016/j.knosys.2018.10.018  |
| Hmisc  |  4.7.1  | https://cran.r-project.org/package=Hmisc  |
| keras  | 2.11.1  | https://cran.r-project.org/package=keras  |
| knitr  | 1.41	 | https://yihui.org/knitr/  |
| mgcv  | 1.8.41	 |  https://cran.r-project.org/web/packages/mgcv/index.html |
| pacman  | 0.5.1	 | http://github.com/trinker/pacman  |
| processpredictR  | 0.1.0	 | https://cran.r-project.org/package=processpredictR  |
| rmarkdown  | 2.18	 |  https://github.com/rstudio/rmarkdown  |
| tensorflow  | 2.11.0	 | https://cran.r-project.org/package=tensorflow  |
| tidyverse  | 1.3.2	 | https://doi.org/10.21105/joss.01686  |

## Python dependencies
Version of Python used: **3.8**
| library  |  version  | link |
|---|---|---|
| pm4py  | 2.7.2  | https://pm4py.fit.fraunhofer.de/  |
| datetime  | 5.1  |   |
| pandas  | 1.5.3  | https://pandas.pydata.org/  |
| numpy  | 1.23.5  | https://numpy.org/  |
| matplotlib  |  3.6.2  | https://matplotlib.org/  |
| tabulate  | 0.9.0  | https://github.com/astanin/python-tabulate  |
| lifelines  | 0.27.4  | https://github.com/CamDavidsonPilon/lifelines  |
| scikit-learn  | 1.2.2  | https://scikit-learn.org/stable/  |

## Usage

Run it with your favorite IDE, for example Rstudio.

Follow the steps below to render once the analysis_concept.qmd file is opened in Rstudio:

https://quarto.org/docs/get-started/hello/rstudio.html

Or, once the dependencies have been correctly installed, run in terminal: 

```shell
quarto render analysis_concept.qmd
```

## Links

- Common Data Model: https://zenodo.org/record/8012966
- Summary of the protocol: https://cienciadedatosysalud.org/wp-content/uploads/Resumen_CONCEPT_STROKE-1.pdf
- Repository: https://github.com/cienciadedatosysalud/CONCEPT-STROKE
- Issue tracker: https://github.com/cienciadedatosysalud/CONCEPT-STROKE/issues
 
## Licensing
CC BY-NC-ND 4.0 https://creativecommons.org/licenses/by-nc-nd/4.0
