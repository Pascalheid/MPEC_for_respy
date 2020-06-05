import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def read_results():

    drop = ["theta_30", "theta_31", "theta_32", "theta_33"]
    results_ipopt = pd.read_pickle("results_ipopt").drop(columns=drop)
    results_nlopt = pd.read_pickle("results_nlopt").drop(columns=drop)
    results_nfxp = pd.read_pickle("results_nfxp").drop(columns=drop)
    
    for algorithm in [results_ipopt, results_nlopt, results_nfxp]:
        algorithm.loc[algorithm["Converged"] == 0] = np.nan
        algorithm.loc[algorithm["Converged"].isnull(), "Converged"] = 0
 
    return results_ipopt, results_nlopt, results_nfxp


def create_tables(results):
    
    discount_factor = [0.975, 0.985, 0.995, 0.999, 0.9995, 0.9999]
    approach = ["MPEC", "MPEC (numerical)"]
    statistic = ["Mean", "Standard Deviation"]
    index = pd.MultiIndex.from_product(
        [discount_factor, approach, statistic], names=["Discount Factor", "Approach", "Statistic"])
    
    tables = {}
    for i, algorithm in enumerate(["ipopt", "nlopt", "nfxp"]):
        if algorithm == "nfxp":
            approach = ["NFXP", "NFXP (numerical)"]
            index = pd.MultiIndex.from_product(
                [discount_factor, approach, statistic], names=["Discount Factor", "Approach", "Statistic"])

        table_temp = results[i].astype(float).groupby(
            level=["Discount Factor", "Approach"])
        tables[algorithm] = pd.DataFrame(index=index, columns=results[i].columns)
        tables[algorithm].loc(axis=0)[:,:,"Mean"] = table_temp.mean()
        tables[algorithm].loc(axis=0)[:,:,"Standard Deviation"] = table_temp.std()  
        
    return tables

def create_plots(results):
    for column in ["RC", "theta_11", "CPU Time", "# of Major Iter.", "# of Func. Eval."]:
        for i, algorithm in enumerate(["ipopt", "nlopt", "nfxp"]):
            fig, ax = plt.subplots()
    
            x = np.arange(1, int(results[i].shape[0]/2 + 1))
            if algorithm == "nfxp":
                y1 = results[i].loc(axis=0)[:, :, :, "NFXP"][column]
                y2 = results[i].loc(axis=0)[:, :, :, "NFXP (numerical)"][column]
            else:
                y1 = results[i].loc(axis=0)[:, :, :, "MPEC"][column]
                y2 = results[i].loc(axis=0)[:, :, :, "MPEC (numerical)"][column]

            if algorithm == "nlopt":
                ax.set_ylim(ylim)
            ax.plot(x, y1, label="analytical")
            ax.plot(x, y2, label="numerical")
            if algorithm == "ipopt" or algorithm == "nfxp":
                ylim = ax.get_ylim()
            ax.set_ylabel(column)
            ax.set_xlabel("Run")
            ax.set_title(algorithm)
            ax.legend()
            
def create_nfxp_plots(results):
    for column in ["# of Bellm. Iter.", "# of N-K Iter."]:
        fig, ax = plt.subplots()
        x = np.arange(1, int(results[2].shape[0]/2 + 1))
        y1 = results[2].loc(axis=0)[:, :, :, "NFXP"][column]
        y2 = results[2].loc(axis=0)[:, :, :, "NFXP (numerical)"][column]
        ax.plot(x, y1, label="analytical")
        ax.plot(x, y2, label="numerical")
        ax.set_ylabel(column)
        ax.set_xlabel("Run")
        ax.set_title("nfxp")
        ax.legend()
