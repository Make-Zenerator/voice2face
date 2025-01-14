"""공용 함수
    * File IO
    * Logger
    * System
"""
import logging
# import pickle5 as pickle
import pickle
import json
import yaml

import PIL
import torch
import torchvision.transforms as T
import numpy as np

# Imagenet macros
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

INV_IMAGENET_MEAN = [-m for m in IMAGENET_MEAN]
INV_IMAGENET_STD = [1.0 / s for s in IMAGENET_STD]

STANDARD_MEAN = [0.5, 0.5, 0.5]
STANDARD_STD = [0.5, 0.5, 0.5]

INV_STANDARD_MEAN = [-m for m in STANDARD_MEAN]
INV_STANDARD_STD = [1.0 / s for s in STANDARD_STD]

VOX_MEL_MEAN = [10.9915,]
VOX_MEL_STD = [3.1661,]

def imagenet_preprocess(normalize_method='imagenet'):
    if normalize_method == 'imagenet':
        return T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    elif normalize_method == 'standard':
        return T.Normalize(mean=STANDARD_MEAN, std=STANDARD_STD)
    elif normalize_method == 'vox_mel':
        return T.Normalize(mean=VOX_MEL_MEAN, std=VOX_MEL_STD)

"""
File IO
"""
def save_pickle(path, obj):
    
    with open(path, 'wb') as f:
        
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_pickle(path):

    with open(path, 'rb') as f:

        return pickle.load(f)


def save_json(path, obj, sort_keys=True)-> str:
    
    try:
        
        with open(path, 'w') as f:
            
            json.dump(obj, f, indent=4, sort_keys=sort_keys)
        
        msg = f"Json saved {path}"
    
    except Exception as e:
        msg = f"Fail to save {e}"

    return msg

def load_json(path):

	with open(path, 'r', encoding='utf-8') as f:

		return json.load(f)


def save_yaml(path, obj):
	
	with open(path, 'w') as f:

		yaml.dump(obj, f, sort_keys=False)
		

def load_yaml(path):

	with open(path, 'r') as f:
		return yaml.load(f, Loader=yaml.FullLoader)

"""
Logger
"""
def get_logger(name: str, file_path: str, stream=False, level='info')-> logging.RootLogger:

    level_map = {
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    
    logger = logging.getLogger(name)
    logger.setLevel(level_map[level])  # logging all levels
    
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(file_path)

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    if stream:
        logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger



def rescale(x):
    lo, hi = x.min(), x.max()
    return x.sub(lo).div(hi - lo + 1e-5)


def imagenet_deprocess(rescale_image=True, normalize_method='imagenet'):
    if normalize_method == 'imagenet':
        transforms = [
            T.Normalize(mean=[0, 0, 0], std=INV_IMAGENET_STD),
            T.Normalize(mean=INV_IMAGENET_MEAN, std=[1.0, 1.0, 1.0]),
        ]
    elif normalize_method == 'standard':
        transforms = [
            T.Normalize(mean=[0, 0, 0], std=INV_STANDARD_STD),
            T.Normalize(mean=INV_STANDARD_MEAN, std=[1.0, 1.0, 1.0]),
        ]
    if rescale_image:
        transforms.append(rescale)
    return T.Compose(transforms)


def fast_imagenet_deprocess_batch(imgs, normalize_method='imagenet'):
    '''
    ImageNet deprocess batch's non-loop and backpropable implementation
    '''
    if normalize_method == 'imagenet':
        mean = IMAGENET_MEAN
        std = IMAGENET_STD
    elif normalize_method == 'standard':
        mean = STANDARD_MEAN
        std = STANDARD_STD
    mean = torch.tensor(mean).type(imgs.type())
    std = torch.tensor(std).type(imgs.type())
    # Initialize broadcasting Dims
    mean = mean.unsqueeze(0).unsqueeze(-1).unsqueeze(-1)
    std = std.unsqueeze(0).unsqueeze(-1).unsqueeze(-1)

    img_de = imgs * std + mean
    img_de = img_de.mul(255).clamp(0, 255)

    return img_de

def set_mel_transform(mel_normalize_method=None):
    mel_transform = [T.ToTensor(), ]
    print('Called mel_normalize_method:',
        mel_normalize_method)
    if mel_normalize_method is not None:
        mel_transform.append(imagenet_preprocess(
            normalize_method=mel_normalize_method))
    mel_transform.append(torch.squeeze)
    mel_transform = T.Compose(mel_transform)
    return mel_transform

def fast_mel_deprocess_batch(log_mels, normalize_method='vox_mel'):
    '''
    Mel Spectrogram deprocess batch's non-loop and backpropable implementation
    '''
    if normalize_method == 'vox_mel':
        mean = VOX_MEL_MEAN[0]
        std = VOX_MEL_STD[0]
    mean = torch.tensor(mean).type(log_mels.type())
    std = torch.tensor(std).type(log_mels.type())
    log_mels_de = log_mels * std + mean

    return log_mels_de


def window_segment(log_mel, window_length, stride_length):
    """
    Sliding window segmentation on a log_mel tensor
    """
    mel_length = log_mel.shape[1]
    # Calulate the number of windows that can be generated
    num_window = 1 + (mel_length - window_length) // stride_length
    # Sliding Window
    segments = []
    for i in range(0, num_window):
        start_time = i * stride_length
        segment = log_mel[:, start_time:start_time + window_length]
        segments.append(segment)
    segments = torch.stack(segments)
    return segments


def imagenet_deprocess_batch(imgs, rescale=False, normalize_method='imagenet'):
    """
    Input:
    - imgs: FloatTensor of shape (N, C, H, W) giving preprocessed images

    Output:
    - imgs_de: ByteTensor of shape (N, C, H, W) giving deprocessed images
      in the range [0, 255]
    """
    if isinstance(imgs, torch.autograd.Variable):
        imgs = imgs.data
    imgs = imgs.cpu().clone()
    deprocess_fn = imagenet_deprocess(
        rescale_image=rescale, normalize_method=normalize_method)
    imgs_de = []
    for i in range(imgs.size(0)):
        img_de = deprocess_fn(imgs[i])[None]
        img_de = img_de.mul(255).clamp(0, 255).byte()
        imgs_de.append(img_de)
    imgs_de = torch.cat(imgs_de, dim=0)
    return imgs_de


def deprocess_and_save(image, normalize_method, save_path):
    '''
    Deprocess a image Tensor generated by VoxDataset, and save its image as a
    jpg
    '''
    deprocess_fn = imagenet_deprocess(normalize_method=normalize_method)
    image = deprocess_fn(image)
    #print('deprocessed image shape:', image.shape)
    img = np.array(image)
    img = np.transpose(img, (1, 2, 0))
    img = (img * 255).astype(np.uint8)
    #print(img.shape)
    #print(np.max(img), np.min(img))
    img = PIL.Image.fromarray(img)
    img.save(save_path)


def unpack_var(v):
    if isinstance(v, torch.autograd.Variable):
        return v.data
    return v
