import caffe
import numpy as np
from PIL import Image
import os


caffe.set_device(0)
caffe.set_mode_cpu()

imgs = os.listdir('/home/ankdesh/ssd/datasets/tini-imagenet/tiny-imagenet-200/test/images/')
np100imgs = np.empty(shape=(100,3,395,395))

for i in range(100):
    readImage = Image.open(open('/home/ankdesh/ssd/datasets/tini-imagenet/tiny-imagenet-200/test/images/' + imgs[i]))
    readImage = readImage.resize((395,395))
    npimg = np.array(readImage)
    if (len(npimg.shape) != 3):
        print ('Skipping B/W image:' + str(imgs[i]))
        continue
    #HWC to CHW
    npimg = np.transpose(npimg,(2,0,1))
    np100imgs[i,:,:,:] = npimg

    # Preprocess
    np100imgs /= 255.
    np100imgs -= 0.5
    np100imgs *= 2.

net = caffe.Net('/home/ankdesh/ssd/models/caffe/inceptionv3/deploy_inception-v3.prototxt', \
                 '/home/ankdesh/ssd/models/caffe/inceptionv3/inception-v3.caffemodel', caffe.TEST)

net.blobs['data'].data[...] = npimg
_ = net.forward()

#print("Blobs:")
#for name, blob in net.blobs.iteritems():
#    print("{:<5}:  {}".format(name, blob.data.shape))

def getCellsFromModel(net, widthCell, heightCell):
    countCellZeros = 0
    countCellNonZeros = 0
   
    fileName = 'results' + str(heightCell) + 'x' + str(widthCell) + '.csv' 
    print ('Writing results to' + fileName)
    with open(fileName,'w') as f:
        f.write (','.join(['BlobName','NumZeroCells','NumNonZerosCells\n']))
        for name, blob in net.blobs.iteritems(): # iterate through all the fm blobs
            if name in net.layer_dict.keys(): # Some blobs like 'data' do not have layers with same name
                if net.layer_dict[name].type == 'Convolution': # Looking for convolution blocks only
                    #print ([x for x in net._layer_dict[name].blobs[0].shape])
                    filters4d = net.layer_dict[name].blobs[0]
                    filterNpData = filters4d.data
                    #print ("Processing {:<7}: FilterSize = {:<2} x {:<2} x {:<2} x {:<2} ".format (name, *[x for x in filters4d.shape]))
                    #print ("                       IFMSize = {:<3} x {:<3} x {:<3} x {:<3}".format(*[x for x in blob.shape]))
                    stride = 1 # *** ASSUMPTION ***
                    padEachSideX = filters4d.width / 2 
                    padEachSideY = filters4d.height / 2

                    paddedData = np.pad(blob.data,((0,0),(0,0), (padEachSideY,padEachSideY), (padEachSideX,padEachSideX)),'constant')
                    # print ("                Padded IFMSize = {:<3} x {:<3} x {:<3} x {:<3}".format(*paddedData.shape))
                    # Iterate all Data
                    countBlobZeros = 0
                    countBlobNonZeros = 0
                    for n in range(paddedData.shape[0]):
                        listChZeros = []
                        listChNonZeros = []
                        for c in range(paddedData.shape[1]):
                            #yield (paddedData[n,c,:,:])
                            countChZero = 0
                            countChNonZero = 0
                            for h in range(0, paddedData.shape[2] - widthCell + 1):
                                for w in range(0, paddedData.shape[3]- widthCell + 1):
                                    cell = paddedData[n, c, h:h+heightCell, w:w+widthCell]
                                    if np.count_nonzero(cell) == 0:
                                        countChZero += 1
                                    else :
                                        countChNonZero += 1 
                            listChZeros.append(countChZero)
                            listChNonZeros.append(countChNonZero)
                            countCellZeros += sum(listChZeros)
                            countCellNonZeros += sum(listChNonZeros)
                            countBlobZeros += sum(listChZeros) 
                            countBlobNonZeros += sum(listChNonZeros) 

                        #print (str(n) + '>' + ','.join(map(str,listChZeros)))
                        #print (str(n) + '<' + ','.join(map(str,listChNonZeros)))
                    f.write (','.join([name, str(countBlobZeros), str(countBlobNonZeros) + '\n']))
                

    return (countCellZeros, countCellNonZeros)

#print ('(CellZeros, CellNonZeros) = ' + ','.join(map(str,getCellsFromModel(net, 4, 4))))
getCellsFromModel(net,2,2)
