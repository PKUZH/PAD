""" Run hypoInverse (main function)
  Usage:
    1. modify template hyp control file to tune HypoInverse params
    2. manually write velo mod (e.g., CRE file), include ref ele if necessary
    3. set i/o paths in config file
    4. python run_hyp.py
  Output:
    csv catalog & phase
    sum file (hyp)
    arc file (hyp)
"""
import os, glob
import numpy as np
import multiprocessing as mp
import subprocess
import config

# i/o paths
cfg = config.Config()
ctlg_code = cfg.ctlg_code
ztr_rng = cfg.ztr_rng
ref_ele = cfg.ref_ele
fhyp_temp = cfg.fhyp_temp
f=open(fhyp_temp); lines=f.readlines(); f.close()
fsta = cfg.fsta_out
fpha = cfg.fpha_out
pmod = cfg.pmod
smod = cfg.smod
pos = cfg.pos
get_prt = cfg.get_prt
get_arc = cfg.get_arc
num_workers = cfg.num_workers

# format input
print('formatting input station file')
#os.system('python mk_sta.py')
print('formatting input phase file')
#os.system('python mk_pha.py')
for fname in glob.glob(cfg.fsums): os.unlink(fname)

def run_hyp(ztr):
    # 1. set control file
    fhyp = 'input/%s-%s.hyp'%(ctlg_code, ztr)
    fout=open(fhyp,'w')
    for line in lines:
        if line[0:3]=='ZTR': line = "ZTR %s \n"%ztr
        if line[0:3]=='STA': line = "STA '%s' \n"%fsta
        if line[0:3]=='PHS': line = "PHS '%s' \n"%fpha
        if line[0:5]=='CRE 1': line = "CRE 1 '%s' %s T \n"%(pmod, ref_ele)
        if line[0:5]=='CRE 2': line = "CRE 2 '%s' %s T \n"%(smod, ref_ele)
        if line[0:3]=='POS': line = "POS %s \n"%(pos)
        if line[0:3]=='SUM': line = "SUM 'output/%s-%s.sum' \n"%(ctlg_code, ztr)
        if line[0:3]=='PRT': 
            line = "PRT 'output/%s-%s.ptr' \n"%(ctlg_code, ztr) if get_prt else ''
        if line[0:3]=='ARC': 
            line = "ARC 'output/%s-%s.arc' \n"%(ctlg_code, ztr) if get_arc else ''
        fout.write(line)
    fout.close()
    # 2. run hypoinverse
    p = subprocess.Popen(['hypoInv'], stdin=subprocess.PIPE)
    s = "@{}".format(fhyp)
    p.communicate(s.encode())

# for all ztr
pool = mp.Pool(num_workers)
pool.map_async(run_hyp, ztr_rng)
pool.close()
pool.join()

# format output
print('converting output sum files')
os.system('python sum2csv.py')
for fname in glob.glob('fort.*'): os.unlink(fname)
for fname in glob.glob('input/%s-*.hyp'%ctlg_code): os.unlink(fname)
