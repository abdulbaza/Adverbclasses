import os
for f in os.listdir('.'):
    if f.startswith('run'):
        continue
    threshold = f.split('_')[-1]
    if threshold.startswith('glove'):
        name = threshold[:5]
        threshold = threshold[5:-4]
    else:
        name = threshold[:3]
        threshold = threshold[3:-4]
    print(f, threshold)
    os.system('python ../precision_recall.py {} {} {} {}'.format(f,threshold,name,f[:-4] + '.png'))
