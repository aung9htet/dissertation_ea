import numpy as np
import scipy.stats as stats

def statistical_analysis():
    select_candidates = np.random.randint(1,100001, 100)
    ea = np.load('results/ea_uf75_best_fitness_list.npy')
    symmetric_mexpoHD = np.load('results/symmetric_mexpoHD_uf75_best_fitness_list.npy')
    rls = np.load('results/rls_uf75_best_fitness_list.npy')
    opt_ia = np.load('results/opt_ia_uf75_best_fitness_list.npy')
    test_ea = np.array([])
    test_symmetric_mexpoHD = np.array([])
    test_rls = np.array([])
    test_opt_ia = np.array([])

    # select candidates
    for i in select_candidates:
        test_ea = np.append(test_ea, ea[i])
        test_symmetric_mexpoHD = np.append(test_symmetric_mexpoHD, symmetric_mexpoHD[i])
        test_rls = np.append(test_rls, rls[i])
        test_opt_ia = np.append(test_opt_ia, opt_ia[i])
    
    # hypothesis
    results = stats.wilcoxon(test_symmetric_mexpoHD, test_ea, alternative = "greater")
    print("hypothesis ea: ", results)
    results = stats.wilcoxon(test_symmetric_mexpoHD, test_rls, alternative = "greater")
    print("hypothesis rls: ", results)
    results = stats.wilcoxon(test_symmetric_mexpoHD, test_opt_ia, alternative = "greater")
    print("hypothesis opt ia: ", results)

    # alternative hypothesis
    results = stats.wilcoxon(test_symmetric_mexpoHD, test_ea, alternative = "less")
    print("alternative hypothesis ea: ", results)
    results = stats.wilcoxon(test_symmetric_mexpoHD, test_rls, alternative = "less")
    print("alternative hypothesis rls: ", results)
    results = stats.wilcoxon(test_symmetric_mexpoHD, test_opt_ia, alternative = "less")
    print("alternative hypothesis opt ia: ", results)

if __name__ == "__main__":
    statistical_analysis()