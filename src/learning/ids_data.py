import csv

import torch


class IdsData:
    filename = ''
    data = {}
    args = {}
    training_ids = torch.Tensor()
    test_ids = torch.Tensor()
    count_list = torch.Tensor()
    double_count_list = torch.Tensor()

    def __init__(self, filename, g):
        self.filename = filename

        us = []
        ts = []
        ls = []
        tag_matrix = []

        with open(filename) as f:
            reader = csv.reader(f)
            
            for row in reader:
                u = int(row[1])
                t = int(row[2])
                l = int(row[3])
                tags = [int(t) for t in row[4].split(",")]

                us.append(u)
                ts.append(t)
                ls.append(l)
                tag_matrix.append(tags)

        us = torch.LongTensor(us)
        ts = torch.LongTensor(ts)
        ls = torch.LongTensor(ls)
        tag_matrix = torch.LongTensor(tag_matrix)
        self.data = {
            'u': us,
            't': ts,
            'l': ls,
            'tag': torch.transpose(tag_matrix, 0, 1)
        }

        self.args = {
            'G': g,
            'U': int(torch.max(us).item()) + 1,
            'L': int(torch.max(ls).item()) + 1,
            'W': int(torch.max(tag_matrix).item()) + 1,
            'T': int(torch.max(ts).item()) + 1,
            'R': len(us),
            'lenW': tag_matrix.shape[1]
        }

        print('user: ', torch.min(us), ' ~ ', torch.max(us))
        print('location: ', torch.min(ls), ' ~ ', torch.max(ls))
        print('tag: ', torch.min(tag_matrix), ' ~ ', torch.max(tag_matrix))
        
        print(self.args)

    def divide_dataset(self, ratio=0.9):
        size = self.args['R']
        test_size = round((1 - ratio) * size)

        self.test_ids = torch.unique(torch.randint(size, (test_size,)))
        self.training_ids = torch.Tensor([x for x in torch.arange(size) if x not in self.test_ids]).type(torch.long)
        self.count_appearance()

    def get_training_set(self):
        training_data = {}

        for k, v in self.data.items():
            if k == 'tag':
                training_data[k] = torch.stack([torch.take(tags, self.training_ids) for tags in v])
            else:
                training_data[k] = torch.take(v, self.training_ids)

        training_args = self.args.copy()
        training_args['R'] = len(self.training_ids)

        return training_data, training_args

    def get_test_set(self):
        test_data = {}

        for k, v in self.data.items():
            if k == 'tag':
                test_data[k] = torch.stack([torch.take(tags, self.test_ids) for tags in v])
            else:
                test_data[k] = torch.take(v, self.test_ids)

        test_args = self.args.copy()
        test_args['R'] = len(self.test_ids)

        return test_data, test_args

    def count_appearance(self):
        count_list = torch.zeros(self.args['W'])
        double_count_list = torch.zeros(self.args['W'], self.args['W'])
        tag_data = torch.transpose(self.data['tag'], 0, 1)
        for tags in tag_data:
            for t in tags:
                count_list[t] += 1
                for tj in tags:
                    double_count_list[t][tj] += 1
                    double_count_list[tj][t] += 1

        self.count_list = count_list
        self.double_count_list = double_count_list

    def get_appearance_count(self, tag_id):
        return self.count_list[tag_id]

    def get_simultanious_count(self, tag_id1, tag_id2):
        return self.double_count_list[tag_id1, tag_id2]
