"""
This script organizes the speech data into train and test folders.
1-274: train
274-343: test

Unzip the original file and save it in the dataset/TITML-IDN folder.
"""
import os
from shutil import copyfile

DATASET_DIR = "dataset/TITML-IDN"
SPEECH_DIR = os.path.join(DATASET_DIR, "Speech")
TEST_SOUND_NO = 274

TRAIN_DIR = "titml_idn/data/train/speech"
TEST_DIR = "titml_idn/data/test/speech"

if not os.path.exists(TRAIN_DIR):
    os.makedirs(TRAIN_DIR)

if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR)

"""
Speech files.
"""
for _, speaker in enumerate(os.listdir(SPEECH_DIR)):
    SPEAKER_DIR = os.path.join(SPEECH_DIR, speaker)
    for _id, file in enumerate(os.listdir(SPEAKER_DIR)):
        sound_no = int(file.split("-")[1].replace(".wav", "").replace("_x", ""))

        old_file_name = os.path.join(SPEAKER_DIR, file)

        # Move to train folder
        if sound_no < TEST_SOUND_NO:
            new_file_name = os.path.join(TRAIN_DIR, file)
        else:
            new_file_name = os.path.join(TEST_DIR, file)

        copyfile(old_file_name, new_file_name)

"""
Transcript file.
"""
TRANSCRIPT_DIR = os.path.join(DATASET_DIR, "Transcript")
TRANSCRIPT_FILE = os.path.join(TRANSCRIPT_DIR, "transcript_all.txt")
TRANSCRIPT_TRAIN_FILE = os.path.join("titml_idn/data/train/", "transcript.txt")
TRANSCRIPT_TEST_FILE = os.path.join("titml_idn/data/test/", "transcript.txt")

copyfile(TRANSCRIPT_FILE, TRANSCRIPT_TRAIN_FILE)
copyfile(TRANSCRIPT_FILE, TRANSCRIPT_TEST_FILE)
