from pycollisiondb import PyCollision
import matplotlib.pyplot as plt

if False:
    pycoll = PyCollision()
    #pycoll.query_database_by_reactants('Be+ 1s2.2p')
    #pycoll.query_database_by_reactants('HD X(1SIGMA+g)')
    #pycoll.query_database_by_reactants(['Li+3', 'H 2p'])
#    pycoll.query(reactants=['Li+3', 'H 3s'], products=['Li+3', 'H 5d'])

    pycoll.query(reactants=['CH2+',],
                 process_types=['EXE', 'EDS'],
                 method='theory',
                 data_type='cross section')

    pycoll.download_datasets_archive_from_url()
    pycoll.unzip_dataset_archive()

else:
    archive_uuid = 'f9f8ccef-e026-4d85-8118-cb0bcd8a278a'
    pycoll = PyCollision(archive_uuid)

manifest = pycoll.get_manifest()
print(manifest)

pks = pycoll.get_dataset_pks_by_reaction()
print(pks)
print()

pycoll.read_all_datasets()

pycoll.summarize_datasets()

#import sys; sys.exit()

fig, ax = plt.subplots()

pycoll.use_latex = True
pycoll.plot_all_datasets(ax)
#pycoll.plot_datasets(ax, pks=pycols.pks)
plt.legend()
plt.show()

