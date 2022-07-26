import matplotlib.pyplot as plt
from pycollisiondb import PyCollision

pycoll = PyCollision.get_datasets(archive_uuid='a5754f94-8051-4262-b17e-1982c567739e')
query = {'reactants': ['D2 v=4 X(1SIGMA+g)',],
         'products': ['D2 v=5 B(1SIGMA+u)',],
         'process_types': ['EXV'],
         'method': 'theory',
         'data_type': 'cross section'}
#pycoll = PyCollision.get_datasets(query=query)
print(pycoll)

fig, ax = plt.subplots()

pycoll.use_latex = True
pycoll.plot_all_datasets(ax)
plt.legend()
plt.show()

