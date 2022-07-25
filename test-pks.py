from pycollisiondb import PyCollision
import matplotlib.pyplot as plt

if True:
    pycoll = PyCollision()
    #pycoll.query_database_by_pk([41303, 71746, 71797])
    pycoll.query_database_by_pk([3578, 3579])
    #pycoll.query_database_by_pk([69562, 69778])
    pycoll.download_datasets_archive_from_url()
    pycoll.unzip_dataset_archive()

#archive_uuid = '01c5a701-dcc6-47b3-b027-3d5fc1ba7cfa'
#archive_uuid = 'b0582a3c-9a95-4062-a84f-11861a14a7fd'
#pycoll = PyCollision(archive_uuid)

manifest = pycoll.get_manifest()
print(manifest)

pks = pycoll.get_dataset_pks_by_reaction()
print(pks)
print()
pycoll.summarize_datasets()

pycoll.read_all_datasets()

print(pycoll.datasets)
#import sys; sys.exit()

fig, ax = plt.subplots()

#pycoll.datasets[71797].plot_dataset(ax)
#pycoll.datasets[71746].plot_dataset(ax)

#pycoll.datasets[931].plot_dataset(ax)
#pycoll.datasets[933].plot_dataset(ax)
pycoll.use_latex = True
pycoll.plot_all_datasets(ax)
#pycoll.plot_datasets(ax, reaction_texts=[''])
plt.legend()
plt.show()
