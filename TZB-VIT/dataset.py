import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import scipy.io as scio

# def data_process(data):
#     freq = data['FreqHz']
#     data_1 = torch.Tensor(abs(data['frame_Ev']))
#     data_2 = torch.Tensor(abs(data['frame_Eh']))
#     data_3 = torch.Tensor(data['frame_ElevationDegree']).repeat(401,1)
#     data_4 = torch.Tensor(data['frame_AzimuthDegree']).repeat(401,1)
#
#     dataset = torch.stack([data_1,data_2,data_3,data_4],0)
#     return dataset

def data_process(data):
    # [B, C, 401, 512] --> [B, 512, 804]
    # freq = data['FreqHz']
    Ev = torch.Tensor(abs(data['frame_Ev']))
    Eh = torch.Tensor(abs(data['frame_Eh']))
    # f_ED = torch.Tensor(data['frame_ElevationDegree'])
    # f_AD = torch.Tensor(data['frame_AzimuthDegree'])
    # dataset = torch.empty(1,804)
    # for i in range(Ev.shape[0]):
    #     data_tmp = torch.cat([Ev[i],Eh[i]], 0).reshape(1, -1)
    #
    #     dataset = data_tmp if i==0 else torch.cat([dataset, data_tmp], 0)
    dataset = torch.stack([Ev,Eh], 0)
    return dataset


class TrainSet(Dataset):
    def __init__(self, root, spilt):
        self.data_path = root
        self.dataset = []
        self.bn = torch.nn.BatchNorm2d(2)
        if spilt=='train':
            for i in range(10):
                path = self.data_path+str(i+1)+'/'
                for j in range(0,10):
                    data = scio.loadmat(path+'frame_'+str(j+1))
                    data_label = [data_process(data),i]
                    self.dataset.append(data_label)
                # for j in range((epoch+1)*50,250):
                #     data = scio.loadmat(path+'frame_'+str(j+1))
                #     data_label = [data_process(data),i]
                #     self.dataset.append(data_label)
        else:
            for i in range(10):
                path = self.data_path+str(i+1)+'/'
                for j in range(240,250):
                    data = scio.loadmat(path+'frame_'+str(j+1))
                    data_label = [data_process(data),i]
                    self.dataset.append(data_label)


    def __getitem__(self, index):
        return self.dataset[index][0],self.dataset[index][1]

    def __len__(self):
        return len(self.dataset)
