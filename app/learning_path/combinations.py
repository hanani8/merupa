# Write a python script to generate all combinations of 25 courses
import re
from app.learning_path.models import *

afoundational = ["BSMA1001", "BSMA1002", "BSCS1001", "BSHS1001", "BSMA1003", "BSMA1004", "BSCS1002", "BSHS1002"]
adiploma_ds = ["BSCS2004", "BSMS2001", "BSCS2007", "BSCS2008", "BSMS2002", "BSSE2002"]
adiploma_dp = ["BSCS2001", "BSCS2002", "BSCS2003", "BSCS2005", "BSCS2006", "BSSE2001"]
adegree = ["BSCS3002", "BSCS3001", "BSCS3003", "BSCS3004", "BSGN3001"]	

foundational = [
    {1:["BSMA1001","BSMA1002","BSCS1001","BSHS1001"], 2:["BSMA1003","BSMA1004","BSCS1002","BSHS1002"]},
    {1:["BSMA1001","BSMA1002","BSCS1001"], 2:["BSMA1003","BSMA1004:","BSCS1002"], 3:["BSHS1001","BSHS1002"]},
    {1:["BSMA1001","BSMA1002","BSHS1001"], 2:["BSMA1003","BSMA1004:","BSCS1001"], 3:["BSCS1002","BSHS1002"]},
    {1:["BSMA1001","BSCS1001","BSHS1001"], 2:["BSMA1002","BSMA1003:","BSCS1002"], 3:["BSMA1004","BSHS1002"]},
    {1:["BSCS1001","BSHS1001"], 2:["BSMA1001","BSMA1002"], 3:["BSMA1003","BSMA1004"], 4:["BSCS1002","BSHS1002"]},
    {1:["BSMA1001","BSCS1001"], 2:["BSMA1002","BSHS1001"], 3:["BSMA1003","BSCS1002"], 4:["BSMA1004","BSHS1002"]},
    {1:["BSMA1001","BSHS1001"], 2:["BSMA1002","BSCS1001"], 3:["BSMA1003","BSHS1002"], 4:["BSMA1004","BSCS1002"]}
]

diploma_ds = [
    {1:["BSCS2004","BSMS2001","BSCS2007"], 2:["BSCS2008","BSMS2002","BSSE2002"]},
    {1:["BSCS2004","BSME2001"], 2:["BSCS2007","BSMS2002"], 3:["BSCS2008","BSSE2002"]}
]

diploma_dp = [
    {1:["BSCS2001","BSCS2002","BSCS2003","BSCS2005"], 2:["BSCS2006","BSSE2001"]},
    {1:["BSCS2001","BSCS2002","BSCS2003"], 2:["BSCS2005","BSCS2006","BSSE2001"]},
    {1:["BSCS2001","BSSE2001","BSCS2003"], 2:["BSCS2005","BSCS2006","BSCS2002"]},
    {1:["BSSE2001","BSCS2002"], 2:["BSCS2001","BSCS2003"], 3:["BSCS2005","BSCS2006"]},
    {1:["BSCS2001","BSCS2002"], 2:["BSCS2003","BSCS2005"], 3:["BSCS2006","BSSE2001"]},
    {1:["BSCS2001","BSCS2003"], 2:["BSCS2005","BSCS2006"], 3:["BSCS2002","BSSE2001"]}
]

diplomas = [
    {1:["BSCS2004","BSMS2001","BSCS2007"], 2:["BSCS2008","BSMS2002","BSSE2002"], 3:["BSCS2001","BSCS2002","BSCS2003","BSCS2005"], 4:["BSCS2006","BSSE2001"]},
    {1:["BSCS2004","BSMS2001","BSCS2007"], 2:["BSCS2008","BSMS2002","BSSE2002"], 3:["BSCS2001","BSCS2002","BSCS2003"], 4:["BSCS2005","BSCS2006","BSSE2001"]},
    {1:["BSCS2004","BSMS2001","BSCS2007"], 2:["BSCS2008","BSMS2002","BSSE2002"], 3:["BSCS2001","BSSE2001","BSCS2003"], 4:["BSCS2005","BSCS2006","BSCS2002"]},
    {1:["BSCS2004","BSMS2001","BSCS2007"], 2:["BSCS2008","BSMS2002","BSSE2002"], 3:["BSSE2001","BSCS2002"], 4:["BSCS2001","BSCS2003"], 5:["BSCS2005","BSCS2006"]},
    {1:["BSCS2004","BSMS2001","BSCS2007"], 2:["BSCS2008","BSMS2002","BSSE2002"], 3:["BSCS2001","BSCS2002"], 4:["BSCS2003","BSCS2005"], 5:["BSCS2006","BSSE2001"]},
    {1:["BSCS2004","BSMS2001","BSCS2007"], 2:["BSCS2008","BSMS2002","BSSE2002"], 3:["BSCS2001","BSCS2003"], 4:["BSCS2005","BSCS2006"], 5:["BSCS2002","BSSE2001"]},
    {1:["BSCS2004","BSME2001"], 2:["BSCS2007","BSMS2002"], 3:["BSCS2008","BSSE2002"], 4:["BSCS2001","BSCS2002","BSCS2003","BSCS2005"], 5:["BSCS2006","BSSE2001"]},
    {1:["BSCS2004","BSME2001"], 2:["BSCS2007","BSMS2002"], 3:["BSCS2008","BSSE2002"], 4:["BSCS2001","BSCS2002","BSCS2003"], 5:["BSCS2005","BSCS2006","BSSE2001"]},
    {1:["BSCS2004","BSME2001"], 2:["BSCS2007","BSMS2002"], 3:["BSCS2008","BSSE2002"], 4:["BSCS2001","BSSE2001","BSCS2003"], 5:["BSCS2005","BSCS2006","BSCS2002"]},
    {1:["BSCS2004","BSME2001"], 2:["BSCS2007","BSMS2002"], 3:["BSCS2008","BSSE2002"], 4:["BSSE2001","BSCS2002"], 5:["BSCS2001","BSCS2003"], 6:["BSCS2005","BSCS2006"]},
    {1:["BSCS2004","BSME2001"], 2:["BSCS2007","BSMS2002"], 3:["BSCS2008","BSSE2002"], 4:["BSCS2001","BSCS2002"], 5:["BSCS2003","BSCS2005"], 6:["BSCS2006","BSSE2001"]},
    {1:["BSCS2004","BSME2001"], 2:["BSCS2007","BSMS2002"], 3:["BSCS2008","BSSE2002"], 4:["BSCS2001","BSCS2003"], 5:["BSCS2005","BSCS2006"], 6:["BSCS2002","BSSE2001"]},
    {1:["BSCS2001","BSCS2003","BSCS2004","BSMS2001"], 2:["BSCS2003","BSCS2006","BSMS2002","BSCS2007"], 3:["BSCS2005","BSSE2001","BSCS2008","BSSE2002"]},
    {1:["BSCS2001","BSCS2003","BSCS2004","BSCS2007"], 2:["BSCS2003","BSCS2006","BSCS2002","BSCS2008"], 3:["BSCS2005","BSSE2001","BSMS2002","BSSE2002"]},
    {1:["BSCS2001","BSCS2002","BSCS2004","BSCS2007"], 2:["BSCS2003","BSCS2005","BSCS2002","BSCS2008"], 3:["BSCS2006","BSSE2001","BSMS2002","BSSE2002"]},
    {1:["BSCS2001","BSCS2002","BSCS2004","BSMS2001"], 2:["BSCS2003","BSCS2005","BSMS2002","BSCS2007"], 3:["BSCS2006","BSSE2001","BSCS2008","BSSE2002"]},
    {1:["BSCS2002","BSCS2004","BSMS2001"], 2:["BSCS2001","BSCS2005","BSCS2007"], 3:["BSCS2003","BSMS2002","BSCS2008"], 4:["BSCS2006","BSSE2001","BSSE2002"]},
    {1:["BSCS2005","BSCS2004","BSCS2007"], 2:["BSCS2001","BSCS2002","BSMS2001"], 3:["BSCS2003","BSMS2002","BSCS2008"], 4:["BSCS2006","BSSE2001","BSSE2002"]},
    {1:["BSCS2001","BSMS2001","BSCS2004"], 2:["BSCS2003","BSCS2005","BSCS2007"], 3:["BSCS2006","BSMS2002","BSCS2008"], 4:["BSCS2002","BSSE2001","BSSE2002"]},
    {1:["BSCS2001","BSCS2003","BSCS2004"], 2:["BSCS2006","BSMS2001","BSCS2007"], 3:["BSCS2002","BSMS2002","BSCS2008"], 4:["BSCS2005","BSSE2001","BSSE2002"]},
    {1:["BSCS2001","BSCS2003","BSMS2001"], 2:["BSCS2006","BSMS2002"], 3:["BSCS2004","BSCS2007","BSSE2001"], 4:["BSCS2005","BSCS2008"], 5:["BSCS2002","BSSE2002"]},
    {1:["BSCS2001","BSCS2004"], 2:["BSCS2003","BSCS2007"], 3:["BSCS2006","BSCS2008"], 4:["BSCS2002","BSMS2001","BSSE2002"], 5:["BSCS2005","BSMS2002","BSSE2001"]}
]

degree =[
    {1:["BSCS3003","BSCS3004","BSGN3001"], 2:["BSCS3001","BSCS3002"]},
    {1:["BSCS3001","BSCS3002","BSGN3001"], 2:["BSCS3003","BSCS3004"]},
    {1:["BSCS3004","BSGN3001"], 2:["BSCS3003","BSCS3001"], 3:["BSCS3002"]}
]

def combos(f,dip, deg):
    final_f=[]
    final_dip=[]
    final_deg=[]
    for f_dict in f:
        i=1
        s="/1/_"
        for f_key,f_val in f_dict.items():
            for f_c in f_val:
                s += f_c + "_"
            i+=1
            s+="/"+ str(i) +"/_"
        final_f.append(s)


    for dip_dict in dip:
        for path in final_f:
            for dip_key,dip_val in dip_dict.items():
                m=re.search('(?s:.*)/(.+)/', path)
                if m:
                    i=int(m.group(1))
                for dip_c in dip_val:
                    path += dip_c + "_"
                i+=1
                path += "/" + str(i) + "/_"
            final_dip.append(path)

    for deg_dict in deg:
        for paths in final_dip:
            for deg_key,deg_val in deg_dict.items():
                m=re.search('(?s:.*)/(.+)/', paths)
                if m:
                    i=int(m.group(1))
                for deg_c in deg_val:
                    paths += deg_c + "_"
                i+=1
                paths += "/" + str(i) + "/_"
            final_deg.append(paths)
    return final_deg

all_lps = combos(foundational, diplomas, degree)

# for lps in all_lps:
#     s = LearningPath(path = lps)
#     db.session.add(s)
#     db.session.commit()
#     db.session.flush()

