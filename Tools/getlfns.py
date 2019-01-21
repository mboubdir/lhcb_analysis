#Download LFNs from Dirac

import sys
jobNumber = int(sys.argv[1])
j = jobs(jobNumber)
length = len(j.subjobs.select(status='failed'))
#file = open('LFNs.txt','w')
ds = LHCbDataset()
for sj in j.subjobs.select(status="failed"):
      ds.extend(sj.inputdata)
j.copy()
s = str(ds.getLFNs())
print s
file.write(s)
#for i in range(0,length):
      #output = j.subjobs(i).backend.getOutputDataLFNs()
#      s = str(ds.getLFNs())
#     print s
#      file.write(s)    
#      file.write('\n')
file.close()
