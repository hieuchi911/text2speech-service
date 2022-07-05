import os

from sanic import Sanic
import soundfile as sf
from sanic.response import json

from vietTTS.vietTTS.synthesizer import nat_normalize_text, text2mel, mel2wave

app = Sanic("TTS-Server")

@app.route('/to-speech', methods=['POST'])
async def text_to_speech(request):
    # Retreive input
    slot = request.json['slot'] # set slot, a dictionary {name: slot_name, value: slot_val}
    uid = request.json['uid'] # user id
    # retrieve logits
    lexicon_file = 'vietTTS/assets/infore/lexicon.txt'

    folder_name = f"audio/user-{uid}"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
    output = folder_name + f'/{slot["name"]}.wav'

    model_infere(text=slot["value"], lexicon_file=lexicon_file,
                 silence_duration=-1, output=output, sample_rate=16000)
    
    return json({'url': output})

def model_infere(text, lexicon_file, silence_duration, output, sample_rate):
    text =  nat_normalize_text(text)
    
    mel =  text2mel(text, lexicon_file, silence_duration)
    
    wave =  mel2wave(mel)
    sf.write(str(output), wave, samplerate=sample_rate)

if __name__ == '__main__':
    app.run()
