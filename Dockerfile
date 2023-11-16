FROM ghcr.io/cienciadedatosysalud/aspire:latest

USER root
RUN apt update && apt install -y --no-install-recommends \
  && apt install -y xdg-utils graphviz \
  && rm -rf /var/lib/apt/lists/*


# Set time Europe/Madrid

RUN micromamba -n aspire install tzdata -c conda-forge && micromamba clean --all --yes \
    && rm -rf /opt/conda/conda-meta
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN micromamba run -n aspire date

USER $MAMBA_USER

COPY --chown=$MAMBA_USER:$MAMBA_USER env_project.yaml /tmp/env_project.yaml

# Installing dependencies
RUN micromamba install -y -n aspire -f /tmp/env_project.yaml \
    && micromamba run -n aspire Rscript -e 'remotes::install_github("rstudio/tensorflow")' \
    && micromamba run -n aspire Rscript -e 'remotes::install_github("bupaverse/processpredictR")' \
    && micromamba run -n aspire Rscript -e 'remotes::install_github("bupaverse/bupaverse")' \
    #&& micromamba run -n aspire pip install pm4py \
    && micromamba run -n aspire pip cache purge \
    && micromamba clean --all --yes \
    && rm -rf /opt/conda/conda-meta /tmp/env_project.yaml

# Installing R packages not found in conda-forge

#RUN micromamba run -n aspire Rscript -e 'remotes::install_github("rstudio/tensorflow")'
#RUN micromamba run -n aspire Rscript -e 'remotes::install_github("bupaverse/processpredictR")'
#RUN micromamba run -n aspire Rscript -e 'remotes::install_github("bupaverse/bupaverse")'

ENV RETICULATE_PYTHON=/opt/conda/envs/aspire/bin/python

#RUN micromamba run -n aspire pip install pm4py

COPY --chown=$MAMBA_USER:$MAMBA_USER . /home/$MAMBA_USER/projects/concept-stroke

ENV APP_PORT=3000
ENV APP_HOST=0.0.0.0
EXPOSE 3000

WORKDIR /home/$MAMBA_USER

ENTRYPOINT ["micromamba","run","-n","aspire","/opt/entrypoint.sh"]
