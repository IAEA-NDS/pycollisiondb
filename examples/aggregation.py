import numpy as np
import pandas as pd

def aggregate(pycoll):
    
    compatible, (data_type, frame, columns) = pycoll.datasets_compatible(None, raise_exception=False)
    if not compatible:
        print('Cannot aggregate incompatible datasets')
        return
    print(data_type, frame, columns)
    
    d = {}
    nrps = None
    for pk, ds in pycoll.datasets.items():
        r_rps, p_rps = [], []
        for _, reactant_rp in ds.reaction.reactants:
            reactant_rp = (reactant_rp)
            r_rps.append(reactant_rp)
        for _, product_rp in ds.reaction.products:
            product_rp = (product_rp)
            p_rps.append(product_rp)
        if not nrps:
            nrps = len(r_rps) + len(p_rps)
        else:
            assert nrps == len(r_rps) + len(p_rps)
        rps = tuple(r_rps + p_rps)
        d[rps] = pd.Series(ds.y, index=ds.x)
        
    df = pd.DataFrame(d)
    
    rp_counts = [len(set(e[i] for e in d.keys())) for i in range(nrps)]
    rp_counts = np.array(rp_counts, dtype=np.int8)

    # Only allow one RP position to be greater than 1
    assert sum(rp_counts==1) == nrps - 1

    drop_level_idx = np.where(rp_counts == 1)[0]
    df = df.droplevel(list(drop_level_idx), axis=1)

    wildcarded_rps = []
    j = 0
    for i, rp  in enumerate(r_rps):
        if i in drop_level_idx:
            wildcarded_rps.append(str(rp))
        else:
            wildcarded_rps.append(str(rp.formula) + ' (*)')
    wildcarded_reactants = ' + '.join(wildcarded_rps)

    wildcarded_rps = []
    for i, rp  in enumerate(p_rps, start=len(r_rps)):
        if i in drop_level_idx:
            wildcarded_rps.append(str(rp))
        else:
            wildcarded_rps.append(str(rp.formula) + ' (*)')
    wildcarded_products = ' + '.join(wildcarded_rps)

    wildcarded_rxn = ' -> '.join([wildcarded_reactants, wildcarded_products])

    return wildcarded_rxn, df
