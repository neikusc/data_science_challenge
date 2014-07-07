# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import time
import numpy as np
import pandas as pd
from funcs import *

from datetime import datetime

# <codecell>

if __name__ == '__main__':
    t0 = time.clock()
    
    turns = processTurns('challenge_data/turns.csv')
    features = buildFeatures(turns)
    
    users = pd.read_csv('challenge_data/users.csv')
    payers = pd.read_csv('challenge_data/payer_at_30.csv')
    
    rawdata = merge(users, payers, features)
    
    # merg all data into single file for predictive modeling
    rawdata.to_csv('challenge_data/merge.csv', index=False)
    
    print 'Running time = ' + str(time.clock() - t0)

