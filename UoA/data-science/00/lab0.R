cars <- read.csv("/course/data/trade/car-imports.csv")
head(cars)

# fix data types
cars2 <- cars
cars2$vfd <- as.numeric(gsub(",", "", cars$vfd))
cars2$cif <- as.numeric(gsub(",", "", cars$cif))
cars2$Imports.Qty <- as.numeric(cars$Imports.Qty)
cars2$Month <- as.Date(paste0(cars$Month, "01"), format="%Y%m%d")
str(cars2)

# barplot country counts
tab <- table(cars2$Country)
par(mar=c(2,12,1,1))
barplot(tab[order(tab)], horiz=T, las=1)

# barplot country vfd sums
tab <- tapply(cars2$vfd, cars2$Country, sum)
par(mar=c(2,12,1,1))
barplot(tab[order(tab)], horiz=T, las=1)

# narrow scope to Germany, scale vfd to millions NZD, sort by Month
germany <- cars2[cars2$Country == 'Germany',]
germany$vfd <- germany$vfd / 1000000
germany <- germany[order(germany$Month),]

# reserve final 10% for testing
n <- nrow(germany)
pivot <- n - (n %/% 10)
train <- germany[1:pivot,]
test <- germany[-(1:pivot),]

# fit models and predict
mean_model <- mean(train$vfd)
linear_model <- lm(vfd ~ Month, data=train)
mean_pred <- rep(mean_model, 6)
fit_pred <- predict(linear_model, test)

rmse <- function(actual, predicted) {
    sqrt(mean((actual - predicted) ^ 2))
}
cat("RMSE for mean:", fill=T)
rmse(test$vfd, mean_pred)
cat("RMSE for linear model:", fill=T)
rmse(test$vfd, fit_pred)

# plot all data and fitted lines
plot(vfd ~ Month, data=germany, type='l',
xlab='Year', ylab='Value for Duty (millions NZD))')
abline(h=mean_model, col='blue')
abline(linear_model, col='red')
