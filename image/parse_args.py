import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--initial_dir', help='input directory', default="D:/Projects/UNet/Data/wyh")
    parser.add_argument('--dataset_dir', help='output directory', default="D:/Projects/UNet/Dataset9")
    parser.add_argument('--aug_nums', help='Augmentation nums', default=5)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(args.dataset_dir)

