sink("../../outputs/summary_survival_general_COX_model.txt")
tryCatch(
  {
    print(summary(model_surv))
    
  },
  error=function(cond) {
    summary(model_surv)
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)


sink("../../outputs/summary_propensity_global_model.txt")
tryCatch(
  {
    print(summary(propensity_model_global))
    
  },
  error=function(cond) {
    print(paste0("error building model: propension to intervention (global)"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)



sink("../../outputs/summary_propensity_fibrinolisys_model.txt")
tryCatch(
  {
    print(summary(propensity_model_fibri))
    
  },
  error=function(cond) {
    print(paste0("error building model: propension to fibrinolisys intervention"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)


sink("../../outputs/summary_propensity_thrombectomy_model.txt")
tryCatch(
  {
    print(summary(propensity_model_throm_mec))
    
  },
  error=function(cond) {
    print(paste0("error building model: propension to thrombectomy mechanic intervention"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)

sink("../../outputs/summary_propensity_combined_model.txt")
tryCatch(
  {
    print(summary(propensity_model_combined))
    
  },
  error=function(cond) {
    print(paste0("error building model: propension to combined intervention"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)


sink("../../outputs/summary_exitus_ps_fibrinolisys_model.txt")
tryCatch(
  {
    print(summary(model_fibrinolysis))
    
  },
  error=function(cond) {
    print(paste0("error building model: propensity score fibrinolysis as covariable"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)


sink("../../outputs/summary_exitus_ps_thrombectomy_model.txt")
tryCatch(
  {
    print(summary(model_thrombectomy_mec))
    
  },
  error=function(cond) {
    print(paste0("error building model: propensity score thrombectomy mechanic as covariable"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)


sink("../../outputs/summary_exitus_ps_combined_model.txt")
tryCatch(
  {
    print(summary(model_combined))
    
  },
  error=function(cond) {
    print(paste0("error building model: propensity score combined as covariable"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)


sink("../../outputs/summary_exitus_ps_all_model.txt")
tryCatch(
  {
    print(summary(model_full))
    
  },
  error=function(cond) {
    print(paste0("error building model: final model (all propensity score as covariable)"))
  }
)
print(paste0('Summary for ccaa_cd: ',descriptive_values$ccaa_cd))
sink(file = NULL)
