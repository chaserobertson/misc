#!/usr/bin/env python
# coding: utf-8

# # Compsci 753 Assignment 4
# ## Recommender Systems
# Latent Factor Modeling with and without bias terms on user-business review data.
# 
# Chase Robertson
# 
# UPI: crob873
# 
# ID: 686249907

# In[1]:


import json
import pandas as pd

# create pandas dataframe from specified file which contains
# a separate json object on each line for each observation
def read_file(filename):
    data = {}
    file = open(filename, 'r')
    for line in file.readlines():
        datum = json.loads(line)
        for k, v in datum.items():
            if k not in data:
                data[k] = []
            data[k].append(v)
    file.close()
    return pd.DataFrame(data)
    
# import each datafile and report shapes and colnames
train = read_file('train.json')
test = read_file('test.json')
val = read_file('val.json')
print(train.shape, test.shape, val.shape)
train.head()


# # Tasks
# ## Task 1
# Estimate global bias $b_g$, user specific bias $b_i$, and item specific bias $b_j$ on training data. Report global bias, and user/item specific bias estimates for one example user and business.
# 
# - First, all unique user and business ID's are collected from all datasets.

# In[2]:


import numpy as np
np.random.seed(12345)

# Collect all unique user and business ID's
user_ids = np.union1d(np.union1d(val['user_id'], test['user_id']), 
                      train['user_id'])
biz_ids = np.union1d(np.union1d(val['business_id'], test['business_id']), 
                     train['business_id'])


# - Then, global, per-user, and per-business biases are estimated by rating means.

# In[3]:


# estimate global, user, and item biases of reviews in dataframe
def get_bias(df):
    b_g = df['stars'].mean()
    
    # user and business biases are relative to global bias
    b_i = df.groupby('user_id')['stars'].mean() - b_g
    b_j = df.groupby('business_id')['stars'].mean() - b_g
    
    # use dictionaries to speed up lookup
    return b_g, b_i.to_dict(), b_j.to_dict()

b_g, b_i, b_j = get_bias(train)


# In[4]:


# display bias estimates: global, specific user and specific business
usr = 'b4aIMeXOx4cn3bjtdIOo6Q'
biz = '7VQYoXk3Tc8EZeKuXeixeg'

print(f'Global bias: {b_g:.2f}')
print(f'Bias of user "{usr}": {b_i[usr]:.2f}')
print(f'Bias of business "{biz}": {b_j[biz]:.2f}')


# - The user chosen tends to review below the global mean of reviews by half a star. The selected business is quite close to having an average mean review.
# 
# ## Task 2
# Train a Latent Factor Model without bias, with k=8 factors, for 10 epochs, with learning rate 0.01 and regularisation 0.3, reporting RMSE for each epoch.
# 
# - User and business k-length factor vectors are initialised from the standard normal distribution.
# - For each epoch, a rating prediction is calculated with the dot product of each training data point's user and business factor vectors. Squared error is then calcuated and used to update factors by the error gradient.

# In[5]:


# use progress bar if verbose training requested
from tqdm.notebook import trange, tqdm

train_obs = train.to_numpy()

# train Latent Factor Model without bias
def train_LFM(data=train_obs, k=8, n_epochs=10, lr=0.01, lmda=0.3, verbose=0):
    
    # init random factors for each user and business
    Q = {u: np.random.standard_normal(k) for u in user_ids}
    P = {b: np.random.standard_normal(k) for b in biz_ids}
    RMSE = np.zeros(n_epochs)

    for e in range(n_epochs):
        SE = np.zeros(len(data))
        
        # for each observation in training data (progress bar if verbose)
        t = trange(len(data), leave=False) if verbose else range(len(data))
        for i in t:
            # get business_id, user_id, and rating of this obs
            b, u, r = data[i][1:4]
            # compute predicted rating and error
            rhat = Q[u].dot(P[b])
            err = r - rhat
            SE[i] = err**2
            # update factors with gradient of error
            dLq = -2*err*P[b] + 2*lmda*Q[u]
            dLp = -2*err*Q[u] + 2*lmda*P[b]
            Q[u] -= lr * dLq
            P[b] -= lr * dLp
        RMSE[e] = np.sqrt(np.mean(SE))
        if verbose:
            print(f'Epoch {e} RMSE: {RMSE[e]:.4f}')
    return {'k': k, 'RMSE': RMSE, 'Q': Q, 'P': P}


# In[6]:


lfm8 = train_LFM(k=8, verbose=1)


# - There is a nicely exponential decline in RMSE over epochs, with 10 actually seeming an ideal stopping point, by chance.
# 
# ## Task 3
# Report RMSE on validation set of LFM trained with each k in {4,8,16}. Choose the model with best RMSE and report RMSE on test set.

# In[7]:


lfm4 = train_LFM(k=4)
lfm16 = train_LFM(k=16)


# In[8]:


# no-bias prediction: each prediction is just a dot product of factors
def get_predictions(lfm, dataset):
    Q = lfm['Q']
    P = lfm['P']
    data = dataset.to_numpy()
    return [Q[x[2]].dot(P[x[1]]) for x in data]

def get_rmse(lfm, dataset):
    pred = get_predictions(lfm, dataset)
    return np.sqrt(np.mean((dataset['stars'] - pred)**2))


# In[9]:


lfms = [lfm4, lfm8, lfm16]
rmses = [get_rmse(lfm, val) for lfm in lfms]

for lfm, rmse in zip(lfms, rmses):
    print(f'LFM k={lfm["k"]} validation RMSE: {rmse:.5f}')


# In[10]:


best_lfm = lfms[rmses.index(min(rmses))]
print(f'Best LFM (k={best_lfm["k"]}) test RMSE: {get_rmse(best_lfm, test):.5f}')


# - The validation performance is quite similar across models. The test RMSE is also not very good - predictions are nearly 2 stars away from their true value.
# 
# ## Task 4
# Add bias terms to LFM, initialising with the estimated bias from Task 1. Train a model like that in Task 2, reporting RMSE of each epoch and specific bias of a single user and business.
# 
# - Initial bias estimates, addition of bias to rating prediction calculation, and user/business bias gradient updates are added to the previous LFM training code.

# In[11]:


import copy

# Latent Factor Model with bias (starting from initial estimates)
def LFM_bias(b_g, b_u, b_b, data=train_obs, k=8, n_epochs=10, lr=0.01, lmda=0.3, verbose=0):
    # ensure user and bias estimates are not overwritten across models 
    b_u = copy.deepcopy(b_u)
    b_b = copy.deepcopy(b_b)
    Q = {u: np.random.standard_normal(k) for u in user_ids}
    P = {b: np.random.standard_normal(k) for b in biz_ids}
    RMSE = np.zeros(n_epochs)

    for e in range(n_epochs):
        SE = np.zeros(len(data))
        rng = trange(len(data), leave=False) if verbose else range(len(data))
        for i in rng:
            b, u, r = data[i][1:4]
            # now we include bias estimates in prediction
            rhat = b_g + b_u[u] + b_b[b] + Q[u].dot(P[b])
            err = r - rhat
            SE[i] = err**2
            dLq = -2*err*P[b] + 2*lmda*Q[u]
            dLp = -2*err*Q[u] + 2*lmda*P[b]
            Q[u] -= lr * dLq
            P[b] -= lr * dLp
            # also update bias estimates by error gradient
            b_u[u] -= lr * (-2*err + 2*lmda*b_u[u])
            b_b[b] -= lr * (-2*err + 2*lmda*b_b[b])
        RMSE[e] = np.sqrt(np.mean(SE))
        if verbose:
            print(f'Epoch {e} RMSE: {RMSE[e]:.4f}')
    return {'k': k, 'RMSE': RMSE, 'Q': Q, 'P': P, 'b_i': b_u, 'b_j': b_b}


# In[12]:


lfm8_b = LFM_bias(b_g, b_i, b_j, k=8, verbose=1)


# - RMSE started at a much lower value now that bias is included - it seems that starting with reasonable bias estimates makes quite a big impact upfront.

# In[13]:


usr = 'b4aIMeXOx4cn3bjtdIOo6Q'
biz = '7VQYoXk3Tc8EZeKuXeixeg'

print(f'Global bias: {b_g:.2f}')
print(f'Bias of user "{usr}": {lfm8_b["b_i"][usr]:.2f}')
print(f'Bias of business "{biz}": {lfm8_b["b_j"][biz]:.2f}')


# - The selected user and business bias estimates are not too far off from their naive estimates after training, but have changed somewhat.
# 
# ## Task 5
# Report RMSE on validation set of LFM trained with bias on each k in {4,8,16}. Choose the model with best RMSE and report RMSE on test set.

# In[14]:


lfm4_b = LFM_bias(b_g, b_i, b_j, k=4)
lfm16_b = LFM_bias(b_g, b_i, b_j, k=16)


# - I've chosen to default to a user/business bias of zero, if the user/business does not already have a bias estimate.

# In[15]:


# prediction using LFM with bias
def bias_predictions(lfm, dataset):
    Q = lfm['Q']
    P = lfm['P']
    b_u = lfm['b_i']
    b_b = lfm['b_j']
    data = dataset.to_numpy()
    
    rhat = [0 for x in data]
    for i, x in enumerate(data):
        b, u, r = x[1:4]
        if u not in b_u:
            b_u[u] = 0
        if b not in b_b:
            b_b[b] = 0
        rhat[i] = b_g + b_u[u] + b_b[b] + Q[u].dot(P[b])
    return rhat

def bias_rmse(lfm, dataset):
    pred = bias_predictions(lfm, dataset)
    return np.sqrt(np.mean((dataset['stars'] - pred)**2))

for lfm in [lfm4_b, lfm8_b, lfm16_b]:
    print(f'LFM with bias k={lfm["k"]} validation RMSE: {bias_rmse(lfm, val):.5f}')


# In[16]:


print(f'Best LFM with bias (k=4) test RMSE: {bias_rmse(lfm4_b, test):.5}')


# - The test RMSE of the best model with bias terms included is much better than the best without bias from Task 3. Adding bias led to a nearly 50% improvement, an impressive gain in performance for a relatively minor change. The model with k=4 seems best now, though not by much.
