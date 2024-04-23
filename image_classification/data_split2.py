import os
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def copy(dst, item: str, paths: list):
    for path in tqdm(paths):
        p = path.split("\\")
        shutil.copy(path, os.path.join(dst, item, p[-2] + '_' + p[-1]))

if __name__ == '__main__':
    origin_path = r'D:\Projects\ScanSceneClassification\data'
    
    result_path = r'D:\Projects\ScanSceneClassification\dataset'
    
    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.mkdir(result_path)
    
    train_path = os.path.join(result_path, 'train')
    test_path = os.path.join(result_path, 'test')
    
    os.mkdir(train_path)
    os.mkdir(test_path)
    
    for item in ['intra', 'extra']:
        os.mkdir(os.path.join(train_path, item))
        os.mkdir(os.path.join(test_path, item))
        paths = []
        for path in os.listdir(os.path.join(origin_path, item)):
            for i in os.listdir(os.path.join(origin_path, item, path)):
                paths.append(os.path.join(origin_path, item, path, i))
        print(len(paths))
        if item == 'intra':
            paths = paths[::3]
        if item == 'extra':
            paths = paths[::2]
        print(len(paths))
        train, test = train_test_split(paths, test_size=0.3, random_state=26)
    
        print(len(train), len(test))
        copy(train_path, item, train)
        copy(test_path, item, test)
    
        # for path in tqdm(train):
        #     p = path.split("\\")
        #     shutil.copy(path, os.path.join(train_path, item, p[-2] + '_' + p[-1]))
        #     # print(os.path.join(train_path, item, p[-2] + '_' + p[-1]))
        # for path in tqdm(test):
        #     p = path.split("\\")
        #     shutil.copy(path, os.path.join(test_path, item, p[-2] + '_' + p[-1]))
