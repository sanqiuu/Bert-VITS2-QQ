#!/usr/bin/env python
# coding: utf-8
import sys, os

if sys.platform == "darwin":
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
from . import commons
from .import utils
from .text.symbols import symbols
from scipy.io.wavfile import write
from .text import cleaned_text_to_sequence, get_bert
from .text.cleaner import clean_text
import torch
from torch import no_grad, LongTensor
from .models import SynthesizerTrn
import argparse


net_g = None

def get_text(text, language_str, hps):
    norm_text, phone, tone, word2ph = clean_text(text, language_str)
    phone, tone, language = cleaned_text_to_sequence(phone, tone, language_str)

    if hps.data.add_blank:
        phone = commons.intersperse(phone, 0)
        tone = commons.intersperse(tone, 0)
        language = commons.intersperse(language, 0)
        for i in range(len(word2ph)):
            word2ph[i] = word2ph[i] * 2
        word2ph[0] += 1
    bert = get_bert(norm_text, word2ph, language_str)
    del word2ph

    assert bert.shape[-1] == len(phone)

    phone = torch.LongTensor(phone)
    tone = torch.LongTensor(tone)
    language = torch.LongTensor(language)

    return bert, phone, tone, language

def infer(text, sdp_ratio, noise_scale, noise_scale_w, length_scale, sid):
    global net_g

    bert, phones, tones, lang_ids = get_text(text, "ZH", hps)
    with torch.no_grad():
        x_tst=phones.to(device).unsqueeze(0)
        tones=tones.to(device).unsqueeze(0)
        lang_ids=lang_ids.to(device).unsqueeze(0)
        bert = bert.to(device).unsqueeze(0)
        x_tst_lengths = torch.LongTensor([phones.size(0)]).to(device)
        del phones
        speakers = torch.LongTensor([sid]).to(device)
        audio = net_g.infer(x_tst, x_tst_lengths, speakers, tones, lang_ids, bert, sdp_ratio=sdp_ratio
                           , noise_scale=noise_scale, noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0,0].data.cpu().float().numpy()
        del x_tst, tones, lang_ids, bert, x_tst_lengths, speakers
        return audio

def tts_fn(text, speaker, sdp_ratio, noise_scale, noise_scale_w, length_scale):
    with torch.no_grad():
        audio = infer(text, sdp_ratio=sdp_ratio, noise_scale=noise_scale, noise_scale_w=noise_scale_w, length_scale=length_scale, sid=speaker)
    return audio


model = "BertVITS2\models\Genshin.pth"
config = "BertVITS2\configs\config.json"

hps = utils.get_hparams_from_file(config)


device = (
    "cuda:0"
    if torch.cuda.is_available()
    else (
        "mps"
        if sys.platform == "darwin" and torch.backends.mps.is_available()
        else "cpu"
    )
)
net_g = SynthesizerTrn(
        len(symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
_ = net_g.eval()
_ = utils.load_checkpoint(model, net_g, None, skip_optimizer=True)
    
def Trans_GS(text = "哎嘿",speaker_id=0,out_path='voice.wav'):

    audio = tts_fn(text, speaker_id, sdp_ratio=0.2,noise_scale=0.6, noise_scale_w=0.8, length_scale=1.0)
    write(out_path, hps.data.sampling_rate, audio)
    print('voice Successfully saved!')
    
    
    
