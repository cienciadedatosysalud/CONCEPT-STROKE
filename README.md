![Logo of the project](https://cienciadedatosysalud.org/wp-content/uploads/logo-Data-Science-VPM.png)

<small><i>This project follows the structure built using the [Common Data Model Builder](https://github.com/cienciadedatosysalud/cdmb), a tool that allows you to create common data models to facilitate interoperability and reproducibility of the analyses.</i></small>


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
## Outputs
Outputs structure and content is described below including the files and folders that are generated when creating a research project with the `cdmb` Python library. There are four main folders corresponding to:

- __docs/CDM/__
  - **cdmb_config.json**: Configuration file.
  - **cohort_definition_inclusion.csv**: csv file that defines the criteria (i.e., codes) for inclusion in a cohort.
  - **cohort_definition_exclusion.csv**: csv file that defines the criteria (i.e., codes) for exclusion in a cohort.
  - **common_datamodel.xlsx**: The definition of the common data model in Excel format.
  - **entities/**: Folder structure where, for each defined entity, the catalogs and the established validation rules are stored.
  - **ER.gv, ER.gv.png**: an Entity-Relationship Diagram of the entities included in the CDM.
  - **synthetic-data/**: Folder structure contaning an automatically generated set of 1000 synthetic records per entity included en the CDM.
  - **hashed_files_list.json**: List of the files generated or used after generating the project with their md5 hash. This file must be kept hidden 
and should be used to cross-check with the results obtained from the analysis from the original input files.
- __inputs/__
  - **data.duckdb**: Database that temporarily contains the data entered by the user (synthetic data by default)
- __outputs/__
  - (Default directory of all the outputs produced in the project execution)
- __src/__
  - __analysis-scripts/__
    - (directory where the analysis scripts developed by the user are stored)
    - **_quarto.yml**: File containing the Metadata to execute Quarto documents.
  - __check_load-scripts/__
    - **check_load.py**: Script in charge of the mapping between the files introduced by the user (./inputs) and map them to the defined entities (inputs/data.duckdb). 
    In the loading process, the following checks are performed: Name of the variables match; the format/type of the variables match those established in the configuration.
    - __inputs/__: Auxiliary folder for the script 'check_load.py'.
  - __dqa-scripts/__
    - **dqa.py**: Data Quality Assesment script by default.
  - **validation-scripts/**
    - **validator.py**: Script in charge of applying the validation rules to the data.
    - **valididator_report.qmd**: Quarto document that generates a report in html from the results obtained from 'validator.py'. 
    - **_quarto.yml**: File containing metadata to execute Quarto documents.
- **ro-crate-metadata.json**: Accessible and practical formal metadata description for use in a wider variety of situations, 
from an individual researcher working with a folder of data, to large data-intensive computational research environments. For more information, visit [RO-Crate](https://www.researchobject.org/ro-crate/).
- **man_container_deployment.md**: From Data Science for Health Services and Policy Research group we provide in the following
  GitHub repository, a solution, for the deployment of the generated project. This step is optional.
- **LICENSE.md**: Project license.
## Requirements/Dependencies 
__*Note that dependencies may vary depending on user modifications!*__

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

# Authoring

| Surname, name | Affiliation | ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) ORCID |
|---------------|-------------|------------------------------------------------------------------------------|
| Grupo de Investigación en Ciencia de Datos para Servicios y Políticas de Salud | Instituto Aragonés de Ciencias de la Salud (IACS), Instituto de Investigación Sanitaria de Aragón (IIS) | |
| Royo-Sierra, Santiago | Instituto Aragonés de Ciencias de la Salud (IACS) | https://orcid.org/0000-0002-0048-4370 |
| Estupiñan-Romero, Francisco | Instituto Aragonés de Ciencias de la Salud (IACS) | https://orcid.org/0000-0002-6285-8120 |
| González-Galindo, Javier | Instituto Aragonés de Ciencias de la Salud (IACS) | https://orcid.org/0000-0002-8783-5478 |
| Bernal-Delgado, Enrique | Instituto Aragonés de Ciencias de la Salud (IACS) | https://orcid.org/0000-0002-0961-3298 |

__Project leader: [Bernal-Delgado, Enrique](https://orcid.org/0000-0002-0961-3298)__


# Previous version(s):

# How to contribute
- Repository: https://github.com/cienciadedatosysalud/CONCEPT-STROKE
- Issue tracker: https://github.com/cienciadedatosysalud/CONCEPT-STROKE/issues

# References
- Data Science for Health Services and Policy Research group: https://cienciadedatosysalud.org/en/
- Common Data Model Builder library :https://github.com/cienciadedatosysalud/cdmb
- Analytic Software Pipeline Interface for Reproducible Execution (ASPIRE): https://github.com/cienciadedatosysalud/ASPIRE
- Atlas VPM community in Zenodo: https://zenodo.org/communities/atlasvpm
- Research Object Crate (RO-Crate): https://www.researchobject.org/ro-crate/
- ORCID: https://orcid.org/

[![DOI](https://zenodo.org/badge/653146110.svg)](https://zenodo.org/badge/latestdoi/653146110)
<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" ><img src="https://img.shields.io/badge/license-CC--BY%204.0-lightgrey" alt="License: CC-BY 4.0"></a>

