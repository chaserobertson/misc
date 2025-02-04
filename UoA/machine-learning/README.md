# machine-learning

My practice with various machine learning models.

## 01 - Decision Tree
1. Load the datasets and deal with missing values if applicable.
2. Implement decision stump, unpruned decision tree, pruned decision tree. Apply each model on each dataset, using pre-pruning techniques as needed.
3. Select hyperparameters via cross-validation.
4. Compare the three methods' performance on each dataset.
5. Use post-pruning and compare.

## 02 - Naive Bayes
See details at the competition hosted on [Kaggle](https://www.kaggle.com/competitions/point-of-interest-categorization/overview). My results show on the leaderboard as `crob873`.

## 03 - Support Vector Machine - in progress
1. Design a dataset with at least 50 points for which the selection of C in a linear SVM makes a difference.
Load the data set (your own data set), train an SVM with a linear kernel on the full data set, and plot the data set with the decision boundary.
Carry out a leave-1-out cross-validation with an SVM on your dataset. Report the performance on training and test set.
Improve the SVM by changing C. Plot the data set and resulting decision boundary, give the performance.
Explain what C does and how it improved the SVM in this case.
2. DS2. Repeat step 1.2 and 1.3 from above with DS2. You can change the leave-1-out cross validation to something different. If you do so, explain what you did and why you chose this way evaluating.
Pick a kernel which will improve the SVM, plot the data set and resulting decision boundary, give the performance.
Explain which kernel you chose and why.
3. DS3. Repeat step 1.2 and 1.3 from above with DS3. You can change the leave-1-out cross validation to something different. If you do so, explain what you did and why you chose this way evaluating.
Pick a kernel and 2 parameters and optimize, optimize the parameters (similar to Assignment 1), plot again data set and decision boundary and give the performance.
Explain the results of the previous step.
