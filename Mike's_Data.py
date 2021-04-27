#%%
from numpy.lib.arraypad import pad
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
def create_plots(data, elements):
    Treatment = data.Treatment.unique().tolist()
    Tissue = data.Tissue.unique().tolist()
    fig_num = 0
    for tis in Tissue:
        Line = data.Line.unique().tolist()
        for lin in Line:
            for elem in elements:
                elem_avg = elem + ' AVG'
                elem_se = elem + ' SE'
                plt.figure(fig_num)
                shapes = ['o', '^', 's', 'd']
                leg_label = []
                tick_label = []
                i = 0
                max_avg = 0
                Tis_max = data[np.equal.outer(data.to_numpy(copy=False), [tis]).any(axis=1).all(axis=1)]
                Tis_max = Tis_max[elem_avg].max()
                if Tis_max > max_avg:
                    max_avg = Tis_max
                for trt in Treatment:
                    Line = data[np.equal.outer(data.to_numpy(copy=False), [tis, lin, trt]).any(axis=1).all(axis=1)]
                    Line = Line[['Tissue','Line', 'Harvest', 'Treatment', elem_avg, elem_se]]
                    yerr = [Line[elem_se].values.tolist(), Line[elem_se].values.tolist()]
                    plt.errorbar('Harvest', elem_avg, data=Line, yerr=yerr, marker=shapes[i], markersize=10, linewidth=3, solid_capstyle='projecting', elinewidth=1, ecolor='black', capsize=2, capthick=1)
                    handles, labels = plt.gca().get_legend_handles_labels()
                    leg_label.append(trt.split('_')[1])
                    i += 1
                plt.title(lin.split('_')[1] + ' ' + elem + ' Concentrations (' + tis.split('_')[1] + ')')
                plt.legend(handles, leg_label, bbox_to_anchor=(1.05, 1), loc='upper left', markerscale=.65)
                plt.ylim(0, max_avg * 2)
                plt.ylabel(elem + ' Conc. (ppm)')
                plt.xlabel('Harvest')
                plt.xlim(-0.15, 3.15)
                ax = plt.gca()
                plt.draw()
                x_ticks = ax.get_xticklabels()
                for lab in x_ticks:
                    tick_label.append(lab.get_text().split('_')[1])
                ax.set_xticklabels(tick_label)
                plt.savefig("Mike's Plots/" + tis + '/' + lin + '/' + lin.split('_')[1] + ' ' + elem + ' Concentrations (' + tis.split('_')[1] + ')' + '.jpg', bbox_inches='tight', pad_inches=1.1)
                plt.close()
                plt.show()
                fig_num += 1

#%%
data = pd.read_csv("Full data set_felix_rice_Updated root and peduncle values.csv")
#%%
elements = ['Mg', 'P', 'S', 'Ca', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Cd']

#%%
Harvest = data.Harvest.unique().tolist()
# %%

data['Harvest'] = pd.Categorical(data['Harvest'], categories=data['Harvest'].unique())
data = data.groupby(['Tissue', 'Line', 'Harvest', 'Treatment'], as_index=False).first()
# %%
create_plots(data, elements)
# %%
print(data)
# %%
