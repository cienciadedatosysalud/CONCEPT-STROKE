
train_test_df_function <- function(df,perc_train_set){
  data_set_interv <- df %>% filter(intervention_bl %in% 1)
  data_set_nointerv <- df %>% filter(intervention_bl %in% 0)
  if(length(unique(data_set_interv$patient_id))>=(length(unique(data_set_nointerv$patient_id)))){
    split_nointerv <- data_set_nointerv %>% split_train_test(split = perc_train_set)
    train_df_nointerv <- split_nointerv$train_df
    patient_id_ <- data_set_interv[!duplicated(data_set_interv$patient_id),] 
    patient_id_ <- sample(patient_id_$patient_id, length(unique(train_df_nointerv$patient_id)))
    train_df_interv <- data_set_interv %>% filter(patient_id %in% patient_id_)
  }else{
    split_interv <- data_set_interv %>% split_train_test(split = perc_train_set)
    train_df_interv <- split_interv$train_df
    patient_id_ <- data_set_nointerv[!duplicated(data_set_nointerv$patient_id),] 
    patient_id_ <- sample(patient_id_$patient_id, length(unique(train_df_interv$patient_id)))
    train_df_nointerv <- data_set_nointerv %>% filter(patient_id %in% patient_id_)
  }
  test_df_interv <- data_set_interv %>% filter(patient_id %nin% train_df_interv$patient_id)
  test_df_nointerv <- data_set_nointerv %>% filter(patient_id %nin% train_df_nointerv$patient_id)
  test_df <- rbind(test_df_interv, test_df_nointerv)
  train_df <- rbind(train_df_nointerv,train_df_interv)
  list_df <- list(train=train_df,test=test_df)
  return(list_df)
}
compare_predict_observ <- function(predictions){
  compare_predictions <- predictions %>% group_by(patient_id) %>% 
    summarise(
      obs_path = paste0(activity, collapse=",")
    )
  compare_predictions_ <- predictions %>% group_by(patient_id) %>% 
    filter(pred_next_activity %nin% 'endpoint') %>% 
    summarise(pred_path = paste0(pred_next_activity, collapse=","))
  first_activity <- predictions %>% group_by(patient_id) %>% 
    summarise(activity = activity[1])
  
  compare_predictions_ <- left_join(compare_predictions_, first_activity, by = 'patient_id') %>% 
    group_by(patient_id) %>% 
    summarise(pred_path = paste0(activity,',',pred_path))
  compare_predictions <- left_join(compare_predictions, compare_predictions_, by = 'patient_id')
  compare_predictions <- compare_predictions %>% group_by(patient_id) %>% 
    mutate(
      intersection = length(intersect(unlist(strsplit(obs_path,split=',')), unlist(strsplit(pred_path,split=',')))),
      union = length(unlist(strsplit(obs_path,split=','))) + length(unlist(strsplit(pred_path,split=','))) - intersection,
      jaccard_simple = round(intersection/union,2)
    )
  
  return(compare_predictions)
}


predict_next_activity_function <- function(database_path,n_epochs_fit){
  
  con = dbConnect(duckdb::duckdb(), dbdir=database_path, read_only=FALSE)
  
  df <- dbGetQuery(conn = con, 'SELECT a.*,b.* FROM main.event_log a LEFT JOIN main.patient_view b ON a."case:concept:name" = b.patient_id')
  
  dbDisconnect(con, shutdown=TRUE)
  
  
  df <- df %>% rename(activity = `concept:name`, timestamp = `time:timestamp`) %>% 
    select(!ends_with("_dt"))
  
  
  df <- df %>% mutate(
    intervention = case_when(
      inhospital_thrombectomy_bl == 0 & inhospital_fibrinolysis_bl == 0 & thrombolysis_emergency_bl == 0 ~ 'none',
      inhospital_thrombectomy_bl == 0 & (inhospital_fibrinolysis_bl == 1 | thrombolysis_emergency_bl == 1) ~ 'fibrinolysis',
      inhospital_thrombectomy_bl == 1 & (inhospital_fibrinolysis_bl == 1 | thrombolysis_emergency_bl == 1) ~ 'combined',
      inhospital_thrombectomy_bl == 1 & inhospital_fibrinolysis_bl == 0 & thrombolysis_emergency_bl == 0 ~ 'thrombectomy_mec',
    )
  )
  
  df$intervention_bl[df$intervention %in% 'none'] <- 0
  df$intervention_bl[df$intervention %in% 'fibrinolysis'] <- 1
  df$intervention_bl[df$intervention %in% 'thrombectomy_mec'] <- 1
  df$intervention_bl[df$intervention %in% 'combined'] <- 1
  
  
  #### bupar
  
  p <- eventlog(df, case_id='patient_id',
                activity_id = 'activity',
                activity_instance_id = 'activity_instance',
                timestamp = 'timestamp',
                lifecycle_id = 'registration_type',
                resource_id = 'resource_id')
  df <- prepare_examples(p, task = "next_activity",
                         features = c('hospital_cd','ccaa_cd', 'healthcare_area_cd', 
                                      'age_nm', 'sex_cd', 'socioeconomic_level_cd','municipality_code_cd','type_admission_cd','heart_failure_bl','atc_code_antiaggregants_cd', 'barthel_index_nm', 'intervention_bl','intervention'))
  
  
  
  #### MODEL ####
  tryCatch(
    {
      
      set.seed(1234)
      
      perc_train_set <- 0.7
      
      train_test_df <- train_test_df_function(df,perc_train_set)
      
      model <- train_test_df$train %>% create_model(name = "my_model") 
      model %>% compile()
      # default loss function: log-cosh or the categorical cross entropy, for regression tasks 
      #(next time and remaining time) and classification tasks, respectively.
      
      hist <- fit(object = model, train_data = train_test_df$train, epochs = n_epochs_fit)
      
      eval <- model %>% evaluate(train_test_df$test)
    },
    error=function(cond) {
      message(paste0("error in model building"))
    }
  ) 
  
  tryCatch(
    {
      predictions <- model %>% predict(test_data = train_test_df$test, 
                                       output = "append") # default
      
      compare_predictions <- compare_predict_observ(predictions)
      
      # plot_confusion_matrix <- plot(predictions) +
      #   ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 90))
      
      
    },
    error=function(cond) {
      message(paste0("error in model prediction"))
    }
  ) 
  
  # png('../../outputs/confusion_matrix_predictions_bupar.png', width= 1280, height = 720)
  # plot(plot_confusion_matrix)
  # dev.off()
  
  eval_compare_predictions <- list(eval = eval, compare_predictions = compare_predictions, hist_fit = hist)
  return(eval_compare_predictions)
  #file.remove('../../outputs/event_log.csv')
  
}