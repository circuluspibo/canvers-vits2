## VCTK
import torch

import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    print(text, text_norm)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


CONFIG_PATH = "./configs/ko_base.json"
MODEL_PATH = "./logs/ko_base/G_1445000.pth"
#TEXT = "I am artificial intelligent voice made by circulus."
TEXT = "저는 서큘러스의 AI Voice 모델입니다."
SPK_ID = 45
#SPK_ID = 20
OUTPUT_WAV_PATH = "vits_test"

hps = utils.get_hparams_from_file(CONFIG_PATH)

if (
    "use_mel_posterior_encoder" in hps.model.keys()
    and hps.model.use_mel_posterior_encoder == True
):
    print("Using mel posterior encoder for VITS2")
    posterior_channels = 80  # vits2
    hps.data.use_mel_posterior_encoder = True
else:
    print("Using lin posterior encoder for VITS1")
    posterior_channels = hps.data.filter_length // 2 + 1
    hps.data.use_mel_posterior_encoder = False

net_g = SynthesizerTrn(
    len(symbols),
    posterior_channels,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model
).cuda()
_ = net_g.eval()

_ = utils.load_checkpoint(MODEL_PATH, net_g, None)

stn_tst = get_text(TEXT, hps)
import time 

with torch.no_grad():

    for i in range(0,SPK_ID):
        start = time.time()
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        sid = torch.LongTensor([SPK_ID]).cuda()
        audio = (
            net_g.infer(
                x_tst,
                x_tst_lengths,
                sid=sid,
                noise_scale=0.667,
                noise_scale_w=0.8,
                length_scale=1,
            )[0][0, 0]
            .data.cpu()
            .float()
            .numpy()
        )

        print(i, time.time() - start)
        write(data=audio, rate=hps.data.sampling_rate, filename=f"{OUTPUT_WAV_PATH}_{i}.wav")
