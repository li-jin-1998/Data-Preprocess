import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', help='input directory', default="/home/lj/PycharmProjects/Data/Implant")
    parser.add_argument('--dataset_dir', help='output directory', default="/home/lj/PycharmProjects/2D-image-Segmentation/dataset")
    # parser.add_argument('--data_dir', help='input directory', default="/home/lj/PycharmProjects/Data/Edentulous")
    # parser.add_argument('--dataset_dir', help='output directory', default="/home/lj/PycharmProjects/wyh/dataset")
    parser.add_argument('--aug_nums', help='Augmentation nums', default=4)

    # parser.add_argument('--data_path', help='input directory', default=r'D:\Projects\UNet\Dataset14\data')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(args.dataset_dir)

