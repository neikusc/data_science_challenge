# install.packages('gridExtra')
setwd('/home/neik/Kaggle/Scopely')
require(ggplot2)
require(gridExtra)
source("funcs.r")
require(caTools)
# require(glmnet)

set.seed(2014)
data <- read.csv("challenge_data/merge.csv")
merge <- fineProcess(data)

samples <- sample(nrow(merge), nrow(merge)*0.3)
train <- merge[samples, ]
test <- merge[-samples, -c(1)]
truth <- merge[-samples, c(1)]

# ======================================================= #
# build glm model for binary classification
# ======================================================= #
model <- glm(payer_at_30 ~., family=binomial, data=train)
pred <- predict(model, newdata=test, type='response')

# summary of model
summary(model)
# ======================================================= #


# ======================================================= #
#     random forest model
# ======================================================= #
# require(caret)
require(randomForest)
model <- randomForest(payer_at_30 ~., data=train, ntree=1000)
pred <- predict(model, newdata=test, type="prob")
# ======================================================= #



# ======================================================= #
# calculate ROC area under curve and plot it
# ======================================================= #
# glm
colAUC(pred, truth, plotROC=TRUE, alg=c("Wilcoxon","ROC"))
# random Forest
# colAUC(pred[,1], truth, plotROC=TRUE, alg=c("Wilcoxon","ROC"))

# find the best cut-off
require(pROC)
roc.model <-  roc(truth, pred)
coords <- coords( roc.model, "best", best.method="closest.topleft", ret=c("threshold", "accuracy"))
coords

# data exploratory
grid.arrange(ggplot(merge, aes(x=machine_play_most, fill=payer_at_30)) + geom_bar(), 
             ggplot(merge, aes(x=machine_play_most, fill=payer_at_30)) + geom_bar(position='fill'), 
             nrow=2)
