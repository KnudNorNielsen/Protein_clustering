#! /usr/bin/python

import argparse
import numpy as np
import csv
import pandas as pd
import pickle
import copy

# # Creating an empty dictionary
dict = {}
 
# # Adding list as line
dict["Candida"] = [11, 12, 24, 25, 27]
# dict["Epidermophyton"] = [1]
# dict["Hortaea"] = [10]
dict["Malassezia"] = [15, 18, 19, 20]
# dict["Microsporum"] = [13, 14, 26, 30]
# dict["Nannizia"] = [2]
# dict["Pichia"] = [16, 31]
# dict["Trichophyton"] = [4, 5, 6, 7, 8, 9, 32, 35]
# dict["Trichosporon"] = [3]
dict["test"] = [4, 5, 6, 7, 8, 13, 14, 21, 23, 26]



#def main(args):
result_dict = {}
result_dict = {"Candida": [], "Malassezia": [], "test":[]}
with open("ortholog_counts_per_species.stats.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for line in rd:
        if line[0]=="Group_ID":
            pass
        elif len(line) < 29:
            pass
        else:
            line = list(map(int,line))
            for key, idx in dict.items():
                subset_a = np.array(line)[idx]
                if all(i > 0 for i in subset_a):
                    inverse_subset = copy.deepcopy(line)
                    for i in sorted(idx, reverse=True):
                        del inverse_subset[i]
                    if all(i > 0 for i in subset_a) and all(inverse_subset[i] == 0 for i in range(1, len(inverse_subset)-1)):
                        result_dict[key].append(inverse_subset[0])

    # with open("result_dict.pkl", "wb") as f:
    #     pickle.dump(result_dict, f)

    # convert to long format
    df = pd.DataFrame.from_dict(result_dict, orient='index')
    df=pd.DataFrame(data=df).T
    df = df.melt(var_name='Species', value_name='protein')

    # print the dataframe
    print(df)

    df.to_csv("result_dict.csv", sep=',',index=False)





# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         prog="ortho_groups.py", description="Find proteins that are share only by a select group of samples"
#     )
#     parser.add_argument("-i", dest="in", help="This should be the ortholog_counts_per_species.stats.tsv file from SonicParanoid")
#     #parser.add_argument("o", help="name of FASTA entry to compare")
#     args = parser.parse_args()
#     main(args)