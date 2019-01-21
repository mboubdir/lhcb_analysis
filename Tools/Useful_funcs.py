import ROOT
import numpy as np
import pandas as pd

#---------------DALITZ PLOTS-------------------#
def dalitz(df):
    m_pdg_mu = [105.6583]*len(df['mu_prim_PE'])
    m_pdg_pi = [139.5702]*len(df['pi_PE'])
    
    df['m12_squared']   = np.power(m_pdg_mu,2) + np.power(m_pdg_pi,2) + 2*((df['pi_PE']*df['mu_prim_PE'] )- \
                     (df['pi_PX']*df['mu_prim_PX'] + df['pi_PY']*df['mu_prim_PY']+df['pi_PZ']*df['mu_prim_PZ']))
    df['m13_squared']   = np.power(m_pdg_mu,2) + np.power(m_pdg_pi,2) + 2*((df['pi_PE']*df['mu_sec_PE'] )- \
                     (df['pi_PX']*df['mu_sec_PX'] + df['pi_PY']*df['mu_sec_PY']+df['pi_PZ']*df['mu_sec_PZ']))
    df['m23_squared']   = 2*np.power(m_pdg_mu,2) + 2*((df['mu_sec_PE']*df['mu_prim_PE'] )- \
                     (df['mu_sec_PX']*df['mu_prim_PX'] + df['mu_sec_PY']*df['mu_prim_PY']+df['mu_sec_PZ']*df['mu_prim_PZ']))
    df['m_N_1'] = np.sqrt(df['m12_squared'])
    df['m_N_2'] = np.sqrt(df['m13_squared'])

#-----Calculate Vetoes for Prompt signal------#
#Make pion mass to muon (pdg) and cut out J/psi, psi and D0 out of mass range
def vetoes(df):
    m_pdg_mu    = [105.6583]*len(df['pi_PE']) #muon Mass in MeV
    df['mu_prim_v']  = np.sqrt(np.power(m_pdg_mu,2) + np.power(df['mu_prim_M'],2) + \
                             2*((df['pi_PE']*df['mu_prim_PE'] )- \
                                (df['pi_PX']*df['mu_prim_PX'] + df['pi_PY']*df['mu_prim_PY']+df['pi_PZ']*df['mu_prim_PZ'])))
    df['mu_sec_v']   = np.sqrt(np.power(m_pdg_mu,2) + np.power(df['mu_sec_M'],2) + \
                             2*((df['pi_PE']*df['mu_sec_PE'] )- \
				(df['pi_PX']*df['mu_sec_PX'] + df['pi_PY']*df['mu_sec_PY']+df['pi_PZ']*df['mu_sec_PZ'])))

    df['q1_squared'] =2*np.power(m_pdg_mu,2) + 2*((df['mu_prim_PE']*df['pi_PE'] )- \
                     (df['mu_prim_PX']*df['pi_PX'] + df['mu_prim_PY']*df['pi_PY']+df['mu_prim_PZ']*df['pi_PZ']))

    df['q2_squared'] =2*np.power(m_pdg_mu,2) + 2*((df['mu_sec_PE']*df['pi_PE'] )- \
                     (df['mu_sec_PX']*df['pi_PX'] + df['mu_sec_PY']*df['pi_PY']+df['mu_sec_PZ']*df['pi_PZ']))
    return df

#---------------Bin Reweighter function-------------------#
def get_weights(data_reweight, data_x, data_y, bins, weights_x=None, weights_y=None, range=None):
    """
    Args:
      data_reweight: The data points to compute weights for.
      data_x: Data to reweight to.
      data_y: Data to reweight from.
      bin: Number of bins or bin edges
      weights_x: Extra weights for data_x.
      weights_y: Extra weights for data_y.
      range: Left and right edge
    Returns:
      Numpy array with weights.
    """
    range_x = (np.min(data_x), np.max(data_x))
    print("Range X {}".format(range_x))
    range_y = (np.min(data_y), np.max(data_y))
    print("Range Y {}".format(range_y))
    data_ = np.concatenate([data_x, data_y])
    
    #range_ = (np.min(data_), min(np.max(data_x),np.max(data_y)))
    range_ = (np.min(data_), np.max(data_))
    print range_
    # Compute probabilities.
    p_x, bin_edges = np.histogram(data_x, range=range_ ,bins=bins, normed=True, weights=weights_x)
    p_y, _ = np.histogram(data_y, range=range_, bins=bin_edges, normed=True, weights=weights_y)
    

    # Divide histograms safely.
    p_y[p_y == 0.] = -1.0
    weights = p_x / p_y
    weights[p_y == -1.0] = 0.
    #print(weights)
    
    # Only keep values within the range.
    bin_edges[1] += 1e-10
    include = (data_reweight > bin_edges[0]) & (data_reweight < bin_edges[-1])
    idx = pd.cut(data_reweight[include], bin_edges, labels=False)
    result = data_reweight * 0.
    
    result[include] = weights[idx]
    return result


#---------------plot reweighted Vars--------------------#
def plot_reweighted(reweighted_vars, DATAS_df, MC_df):
    
    import matplotlib.pyplot as plt
    from matplotlib_hep import histpoints
    
    # Plot the reweighted variables
    for id, col in enumerate(reweighted_vars, 1):
        #print id, col
        #print MC_df.name
        plt.figure()

        if col=='B_PT':
            range =(0, 50000)
            #plt.xlim(0.0, 50000)
        if col =='nTracks':
            range=(0,600)
        else:
            range=None

        data_col = DATAS_df[col].values
        mc_col   = MC_df[col].values
        #mc_rewcol= MC_df['weights_{}'.format(col)].values

        y_data, y_data, norm_data = histpoints(data_col, range=range, color='black', normed=True, bins=100, \
                                               label='sWeighted DATA', markersize=3. , marker='o', weights=DATAS_df['nSig_sw'])
        
        x_uncorr, y_uncorr, norm_uncorr = histpoints(mc_col, range=range, color='red', normed=True, bins=100, label='MC', markersize=3., marker='o')
        
        x_corr, y_corr, norm_corr = histpoints(mc_col, range=range, color= 'green', normed=True,  bins=100, weights=MC_df['wghts_tot'], markersize=3., \
                                               label='Reweighted MC', marker='o')



        plt.xlabel(vars_to_reweight_dict[col][0])
        plt.ylabel('Events')


        plt.legend(prop={'size': 10})
    
        plt.show()




        
#---------------Compare train test function-------------------#
clf_dict = {"AdaBoost":"AdaBoost",
            "uGB+knnAda": "uGB+knnAda",
            "uGB+FL": "uGB+FL",
            "uBoostBDT_SAMME": "uBDT",
            "uBoostBDT_SAMME_R": "uBDTR",
            
}

def compare_train_test(clf, trainX, trainY, testX, testY, bins=40):
    decisions = []
    import matplotlib.pyplot as plt
    import matplotlib.axis as ax
    plt.figure()
    for X,y in ((trainX, trainY), (testX, testY)):
        d1 = clf.decision_function(X[y>0.5]).ravel()
        d2 = clf.decision_function(X[y<0.5]).ravel()
        decisions += [d1, d2]

    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)

    plt.hist(decisions[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='S (train)')
    plt.hist(decisions[1],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='B (train)')

    hist, bins = np.histogram(decisions[2],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')

    hist, bins = np.histogram(decisions[3],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')
    
    plt.xlabel("{} output".format(clf_dict[clf][0]))
    plt.ylabel("Arbitrary units")
    plt.legend(loc='best')

    


    
#---------------MAIN-------------------#
if __name__ == '__main__':
    main()
