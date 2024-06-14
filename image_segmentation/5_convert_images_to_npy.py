import os
import cv2
import numpy as np
import tqdm


def preprocess(image_path, mask_path, image_size):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise IOError(f"Failed to read image: {image_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_CUBIC)

        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise IOError(f"Failed to read mask: {mask_path}")
        mask = cv2.resize(mask, (image_size, image_size), interpolation=cv2.INTER_NEAREST)
        mask[mask == 64] = 1
        mask[mask == 129] = 2
        mask[mask == 192] = 3
        mask[mask == 255] = 4

        return image, mask
    except Exception as e:
        print(f"Error in preprocess: {e}")
        return None, None


def save_batch(images, masks, batch_index, output_dir):
    images = np.array(images)
    masks = np.array(masks)

    try:
        np.save(os.path.join(output_dir, f'images_batch_{batch_index}.npy'), images)
        np.save(os.path.join(output_dir, f'masks_batch_{batch_index}.npy'), masks)
        print(f'Batch {batch_index} saved successfully.')
    except IOError as e:
        print(f"Error saving data: {e}")


def png_npy(input_dir, image_size=224, batch_size=10000):
    images = []
    masks = []
    batch_index = 0

    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return

    image_dir = os.path.join(input_dir, 'image')
    mask_dir = os.path.join(input_dir, 'mask')

    if not os.path.exists(image_dir) or not os.path.exists(mask_dir):
        print(f"Image or mask directory does not exist.")
        return

    image_paths = sorted(os.listdir(image_dir))

    for path in tqdm.tqdm(image_paths, desc=f"Processing {input_dir}", file=sys.stdout):
        image_path = os.path.join(image_dir, path)
        mask_path = os.path.join(mask_dir, path.replace("IMAGE", "MASK"))

        try:
            image, mask = preprocess(image_path, mask_path, image_size=image_size)
            if image is None or mask is None:
                continue

            images.append(image)
            masks.append(mask)

            if len(images) == batch_size:
                save_batch(images, masks, batch_index, input_dir)
                images = []
                masks = []
                batch_index += 1

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    if images:
        save_batch(images, masks, batch_index, input_dir)


if __name__ == '__main__':
    data_path = r'/home/lj/PycharmProjects/2D-image-Segmentation/dataset/data'

    train_input_dir = os.path.join(data_path, 'augmentation_train')
    test_input_dir = os.path.join(data_path, 'augmentation_test')

    png_npy(train_input_dir, image_size=224)
    png_npy(test_input_dir, image_size=224)
