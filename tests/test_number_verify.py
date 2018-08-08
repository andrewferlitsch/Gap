""" Test Number Verify
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""
import glob

test_files = [f for f in glob.glob("*_test.py")]

for file in test_files:
    if True:
        with open(file, 'r') as f:
            func_list = [line[8:16] for line in f if line[8:13]=='test_']
            func_unic = []
            func_dupl = []
            for func in func_list:
                if func not in func_unic:
                    func_unic.append(func)
               else:
                    func_dupl.append(func)

            if not func_dupl:
                print('Checked module {} not duplicate functions were found'.format(file))
            else:
                f.seek(0)
                f_name=file.split('.')
                cp = f_name[0]+'_cp.py'
                with open(cp,'w+') as f2:
                    i=1
                    for line in f:
                        if 'test_' in line and 'x' not in line:
                            f2.write(line.replace(line[8:16],'test_'+str(i).zfill(3)))
                            i+=1
                        else:
                            f2.write(line)
                    print('Checked module {} this functions were duplicates {} and fixed on {}'.format(file,func_dupl,cp))