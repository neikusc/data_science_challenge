fineProcess <- function(rawdata) {
  rawdata$user_id <- NULL
  rawdata$payer_at_30 <- as.factor(rawdata$payer_at_30)
  rawdata$platform <- as.factor(rawdata$platform)
  rawdata$age_range <- as.factor(rawdata$age_range)
  rawdata$gender <- as.factor(rawdata$gender)
  rawdata$device_type <- as.factor(rawdata$device_type)
  rawdata$machine_play_most <- as.factor(rawdata$machine_play_most)
  return(rawdata)
}

# fineProcess <- function(rawdata) {
#   rawdata$user_id <- NULL
#   rawdata$install_cohort <- NULL
#   rawdata$publisher <- NULL
#   rawdata$payer_at_30 <- as.factor(rawdata$payer_at_30)
#   rawdata$age_range <- as.factor(rawdata$age_range)
#   rawdata$gender <- as.factor(rawdata$gender)
#   rawdata$device_type <- as.factor(rawdata$device_type)
#   return(rawdata)
# }