import torch
import torchaudio
from datasets import concatenate_datasets, load_dataset, load_metric
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import re

cv_test_dataset = load_dataset("common_voice", "id", split="test")
titml_test_dataset = load_dataset("titml_idn", split="test")
cv_test_dataset = cv_test_dataset.remove_columns(
    [
        "client_id",
        "up_votes",
        "down_votes",
        "age",
        "gender",
        "accent",
        "locale",
        "segment",
    ]
)
assert cv_test_dataset.features.type == titml_test_dataset.features.type
test_dataset = concatenate_datasets([titml_test_dataset, cv_test_dataset])
wer = load_metric("wer")

processor = Wav2Vec2Processor.from_pretrained(
    "/workspace/output_models/wav2vec2-large-xlsr-indonesian"
)
model = Wav2Vec2ForCTC.from_pretrained(
    "/workspace/output_models/wav2vec2-large-xlsr-indonesian"
)
model.to("cuda")

chars_to_ignore_regex = "[\,\?\.\!\-\;\:\"\“\%\‘'\”\�]"


# Preprocessing the datasets.
# We need to read the audio files as arrays
def speech_file_to_array_fn(batch):
    batch["sentence"] = re.sub(chars_to_ignore_regex, "", batch["sentence"]).lower()
    speech_array, sampling_rate = torchaudio.load(batch["path"])
    resampler = torchaudio.transforms.Resample(sampling_rate, 16_000)
    batch["speech"] = resampler(speech_array).squeeze().numpy()
    return batch


test_dataset = test_dataset.map(speech_file_to_array_fn)

# Preprocessing the datasets.
# We need to read the aduio files as arrays
def evaluate(batch):
    inputs = processor(
        batch["speech"], sampling_rate=16_000, return_tensors="pt", padding=True
    )

    with torch.no_grad():
        logits = model(
            inputs.input_values.to("cuda"),
            attention_mask=inputs.attention_mask.to("cuda"),
        ).logits

    pred_ids = torch.argmax(logits, dim=-1)
    batch["pred_strings"] = processor.batch_decode(pred_ids)
    return batch


result = test_dataset.map(evaluate, batched=True, batch_size=8)

print(
    "WER: {:2f}".format(
        100
        * wer.compute(predictions=result["pred_strings"], references=result["sentence"])
    )
)
