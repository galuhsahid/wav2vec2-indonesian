from __future__ import absolute_import, division, print_function
import os
import datasets
import random

# TODO: proper citation
_CITATION = """\
Speech Resources Consortium, National Institute of Informatics
"""

_DESCRIPTION = """\
TITML-IDN Dataset by Speech Resources Consortium, National Institute of Informatics
"""

_HOMEPAGE = "http://research.nii.ac.jp/src/en/TITML-IDN.html"
_LICENSE = "For research purpose only"

CORRUPTED_FILE_NAMES = ["m05-260_x.wav", "f07-300.wav", "f07-324.wav", "f07-307.wav"]

class TITMLIDNConfig(datasets.BuilderConfig):
    """BuilderConfig for TITML-IDN."""

    def __init__(self, name, **kwargs):
        description = f"The Indonesian Phonetically Balanced Speech Corpus was developed for training the acoustic models of an automatic speech recognition system. This database contains Bahasa Indonesia speech data from 20 Indonesian speakers. Each speaker was asked to read 343 phonetically balanced sentences most of which selected from a text corpus."

        super(TITMLIDNConfig, self).__init__(
            name=name,
            version=datasets.Version("6.1.0", ""),
            description=description,
            **kwargs,
        )


class TITMLIDN(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [TITMLIDNConfig(name="titml-idn")]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"path": datasets.Value("string"), "sentence": datasets.Value("string")}
            ),
            supervised_keys=("path", "sentence"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        self.archive_path = "titml_idn/data"
        return [
            datasets.SplitGenerator(
                name="train",
                gen_kwargs={"archive_path": os.path.join(self.archive_path, "train")},
            ),
            datasets.SplitGenerator(
                name="test",
                gen_kwargs={"archive_path": os.path.join(self.archive_path, "test")},
            ),
        ]

    def _load_transcript(self, transcript_path):
        transcript_dict = {}

        with open(transcript_path) as f:
            for line in f:
                line_split = line.split(": ")
                sound_no = line_split[0]
                text = line_split[1]
                transcript_dict[sound_no] = text

        return transcript_dict

    def _generate_examples(self, archive_path):
        speech_dir = os.path.join(archive_path, "speech")
        transcript_file = os.path.join(archive_path, "transcript.txt")

        transcript = self._load_transcript(transcript_file)

        for _id, file in enumerate(os.listdir(speech_dir)):
            if file.endswith(".wav") and file not in CORRUPTED_FILE_NAMES:
                wav_path = f"{speech_dir}/{file}"

                # Get transcript
                sound_no = file.split("-")[1].replace(".wav", "").replace("_x", "")
                label = transcript[sound_no].rstrip("\n")

            example = {"path": wav_path, "sentence": label}

            yield str(_id), example
