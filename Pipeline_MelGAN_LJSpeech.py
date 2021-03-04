"""
Train non-autoregressive spectrogram inversion model on the german single speaker dataset by Hokuspokus
"""

import os
import random
import warnings

import torch

from MelGAN.MelGANDataset import MelGANDataset
from MelGAN.MelGANGenerator import MelGANGenerator
from MelGAN.MelGANMultiScaleDiscriminator import MelGANMultiScaleDiscriminator
from MelGAN.melgan_train_loop import train_loop

warnings.filterwarnings("ignore")

torch.manual_seed(17)
random.seed(17)


def get_file_list():
    file_list = list()
    for wav_file in os.listdir("/mount/resources/speech/corpora/LJSpeech/16kHz/wav"):
        file_list.append("/mount/resources/speech/corpora/LJSpeech/16kHz/wav/" + wav_file)
    return file_list


if __name__ == '__main__':
    print("Preparing")
    fl = get_file_list()
    device = torch.device("cuda:2")
    train_dataset = MelGANDataset(list_of_paths=fl[:-100])
    valid_dataset = MelGANDataset(list_of_paths=fl[-100:])
    generator = MelGANGenerator()
    generator.reset_parameters()
    multi_scale_discriminator = MelGANMultiScaleDiscriminator()
    if not os.path.exists("Models/MelGAN/SingleSpeaker/LJSpeech"):
        os.makedirs("Models/MelGAN/SingleSpeaker/LJSpeech")
    print("Training model")
    train_loop(batchsize=32,
               epochs=60000,  # just kill the process at some point
               generator=generator,
               discriminator=multi_scale_discriminator,
               train_dataset=train_dataset,
               valid_dataset=valid_dataset,
               device=device,
               generator_warmup_steps=200000,
               model_save_dir="Models/MelGAN/SingleSpeaker/LJSpeech")