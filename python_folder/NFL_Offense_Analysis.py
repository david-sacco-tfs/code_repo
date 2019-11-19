### For the defense prediction, get each week of NFL Data from the 2019 season for one team, and use that to predict the Points Against for each game and get a model for it.
### Then take the team's average offensive stats that they are playing against that week and enter it into the model and get the Points Against for that team for that game.










import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Importing passing data first
ad_pass = pd.read_csv("Advanced_Passing.csv", sep=',', header=0)
ad_pass.head(5)

# Renaming columns for naming conventions
ad_pass = ad_pass.rename(columns={'Cmp':'PassCmp', 'Att':'PassAtt', 'Yds':'PassYds', '1D':'FirstDowns'})

# Dropping the last row in the dataframe since it is of no use
ad_pass = ad_pass.drop(32)
ad_pass.drop(ad_pass.columns[[-1]], axis=1, inplace=True)

# Understanding data
ad_pass.describe()
ad_pass.info()

# Changings data types to appropriate values
ad_pass.Tm = ad_pass.Tm.astype(str)
ad_pass.G = ad_pass.G.astype(int)
ad_pass.info()

# Creating new variable to get all column headers into a list for histograms
new_cols = list(ad_pass.columns.values)
print(new_cols)

# Creating a new variable to use the `new_cols` variable with the data from above
plot_hists = ad_pass[new_cols]
plot_hists.drop(plot_hists.columns[[0,1]], axis=1, inplace=True)
plot_hists.head()

# Setting up a for loop to iterate through all the columns
for x in range(len(plot_hists.columns)):
    plt.hist(plot_hists.iloc[:,x].dropna(), bins=20)
    plt.title('%a' % plot_hists.columns[x])
    plt.show()

# Creating new variable to use the 'new_cols' variable for box-plots
box_plots = ad_pass[new_cols]
box_plots.drop(box_plots.columns[[0,1]], axis=1, inplace=True)
box_plots.head()

# Setting up a for loop to iterate through all the columns
for x in range(len(box_plots.columns)):
    plt.boxplot(box_plots.iloc[:,x].dropna())
    plt.title('%a' % box_plots.columns[x])
    plt.show()

# Setting up a correlation to determine if there are any major correlations in the data
correlation_pass = ad_pass.corr(method='spearman')

# Setting up a mask-hide for the upper triangle
hide = np.zeros_like(correlation_pass, dtype=np.bool)
hide[np.triu_indices_from(hide)] = True

# Creating the boxplot for the correlation
f, ax = plt.subplots(figsize = (11,9))

# Generating the map color
cmap = sns.diverging_palette(100, 200, as_cmap=True)

# Adding the heatmap for coolness
pass_heatmap = sns.heatmap(correlation_pass, mask=hide, cmap=cmap, vmin=-1, vmax=1, center=0, square=True, linewidths=0.6, cbar_kws={'shrink':0.5})
plt.show(pass_heatmap)

# Showing the numerical correlation
print(ad_pass.corr(method='spearman'))

# Listing all correlation values in ascending order for a better visual representation
ad_pass.corr().unstack().sort_values().drop_duplicates()
