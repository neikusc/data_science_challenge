# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import pandas as pd

from datetime import datetime

# <codecell>

def most_common(lst):
    ''' Find the most common element from a list '''
    return max(set(lst), key=lst.count)

def abs_BalChange(lst):
    ''' Calculate the absolute change of bank balance '''
    if len(lst) < 1:
        mean_lst = 0
    else:
        ls1 = lst[1:]
        ls2 = lst[:-1]
        ls = abs(np.subtract(ls1,ls2))
        mean_lst = np.mean(ls)
    return mean_lst

def diff_days(d1,d2):
    #''' Calculate days different between two dates '''
	date_format = "%Y-%m-%d %H:%M:%S"
	da = datetime.strptime(d1, date_format)
	db = datetime.strptime(d2, date_format)
	delta = db - da
	return delta.days + delta.seconds/(24.*3600) + 1.e-4

# <codecell>

def processTurns(file_path):
    ''' Fill missing machine with Unknown; merge lobby with Lobby; sort data according to user_id and timestamp;
    Remove duplicates rows sharing the same information except timestamp '''
    turns = pd.read_csv(file_path)
    turns.drop(turns.index[[8943335]], inplace=True)
    turns['machine'] = turns['machine'].fillna('Unknown')

    # sort turns according to their id, and timstamp
    turns.sort(['user_id','timestamp'], inplace=True)
    turns['machine'] = ['Lobby' if x=='lobby' else x for x in turns['machine']]
    
    # drop duplicates, count only if user did not change machine, same level and bank balance 
    turns.drop_duplicates(cols=['user_id','machine','user_level','bank_balance'],take_last=False, inplace=True)

    # reset indices
    turns['index'] = range(0,len(turns))
    turns.set_index('index', inplace=True)
    
    return turns

# <codecell>

def buildFeatures(turns):
    ''' Building features from turns.csv '''
    s = pd.Series(['extra_id', '2014-07-06 09:59:59', 'XXX', 0, 0], 
                  index=['user_id', 'timestamp', 'machine', 'user_level', 'bank_balance'])
    df = turns.append(s, ignore_index=True)

    bag_of_times, bag_of_machines, features = [], [], []
    bag_of_levels, bag_of_balances, old_id = [], [], 'id'
    for index, row in df.iterrows():
        new_id = row['user_id']    
    
        if (old_id != new_id) and (index != 0):
            timestamp_start = bag_of_times[0]
            timestamp_end = bag_of_times[-1]
            # number of login times
            times = len(bag_of_times)
            
            # rate of changing levels
            level_change_rate = 1.0*(bag_of_levels[-1] - bag_of_levels[0])/times
            
            # rate of changing bank balance
            balance_change_rate = 1.0*(bag_of_balances[-1] - bag_of_balances[0])/times
            
            # which machine user played the most
            machine_play_most = most_common(bag_of_machines)
            
            # maximum level user obtained
            max_level = max(bag_of_levels)
            
            # maximum bank balance user obtained
            max_balance = max(bag_of_balances)
            
            # absolute change of bank balance
            abs_balance_change = abs_BalChange(bag_of_balances)
        
            features.append([old_id, timestamp_start, timestamp_end, times, machine_play_most, 
                             level_change_rate, max_level, balance_change_rate, abs_balance_change, max_balance])
            bag_of_times, bag_of_machines = [], []
            bag_of_levels, bag_of_balances = [], []
            #
        old_id = row['user_id']
    
        bag_of_times.append( row['timestamp'] )
        bag_of_machines.append( row['machine'] )    
        bag_of_levels.append( row['user_level'] )
        bag_of_balances.append( row['bank_balance'] )
    
    df1 = pd.DataFrame(features)
    df1.columns = ['user_id','timestamp_start','timestamp_end', 'times', 'machine_play_most',
               'level_change_rate','max_user_level', 'balance_change_rate', 'abs_balance_change','max_balance']
    #
    return df1

# <codecell>

def merge(users, payers, features):
    # merge users and payers (28243)
    rawdata = pd.merge(payers, users, on='user_id', how='left')
    
    # merge with features into a single file (27523), missing 720 users
    rawdata = pd.merge(rawdata, features, on='user_id', how='inner')    
    
    # add hour-minute-second into install_cohort
    rawdata['install_cohort'] = rawdata['install_cohort'] + ' 00:00:00'
    
    # find 
    rawdata['time_start'] = map(lambda x,y: diff_days(x,y), rawdata['install_cohort'], rawdata['timestamp_start'] )
    
    # find total period that users log-in
    rawdata['period'] = map(lambda x,y: diff_days(x,y), rawdata['timestamp_start'], rawdata['timestamp_end'] )
    
    # find an average time users log-in per day
    rawdata['avg_time'] = rawdata['times']/rawdata['period']
    
    # there are few missing values in abs_balance_change
    rawdata['abs_balance_change'] = rawdata['abs_balance_change'].fillna(0)
    
    data = rawdata[['user_id','payer_at_30','platform','gender','age_range','device_type','machine_play_most','avg_time',
                   'level_change_rate','max_user_level','balance_change_rate','abs_balance_change','max_balance','time_start']]
    
    return data

