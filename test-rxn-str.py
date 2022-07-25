from pycollisiondb import PyCollision
import matplotlib.pyplot as plt

if True:
    pycoll = PyCollision()
    pycoll.query_database_by_reaction_text(
            ['e- + LiH X(1SIGMA+g);v=10 → e- + LiH A(1SIGMA+g);v=2',
             'e- + LiH v=11;X(1Σ+g) -> LiH A(1SIGMA+g);v=9 + e'
            ])
    pycoll.download_datasets_archive_from_url()
    pycoll.unzip_dataset_archive()

#archive_uuid = 'eb2cd808-cfba-4742-bec3-c9adaf183e93'
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

pycoll.use_latex = True
#pycoll.plot_all_datasets(ax)
pycoll.plot_datasets(ax, pks=[68217, 68258])
plt.legend()
plt.show()
