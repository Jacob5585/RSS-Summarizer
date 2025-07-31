from kokoro import KPipeline
import soundfile as sf
pipeline = KPipeline(lang_code='a') # Set to American English
import numpy as np
import logs

def text_2_speech(text, speaker = 'af_heart'):
    generator = pipeline(
        text, voice=speaker,
        speed=1
    )

    combined_audio = []
    for i, (gs, ps, audio) in enumerate(generator):
        combined_audio.append(audio)

    audio = np.concatenate(combined_audio)

    return audio

def sanitize_text(text):
    text = text.replace("*", " ").replace("#", " ").replace("\n", " ").replace("'", "\'")
    return repr(text)

def save_audio(audio, file_name):
    sf.write(file_name, audio, 24000)

def run_text_2_speech(data, category, file_name):
    text = sanitize_text(data)
    logs.create_info_logs(f'file_name: {file_name}')
    audio = text_2_speech(text)
    save_audio(audio, f'../audio/{category}/{file_name}.mp3')
    logs.create_info_logs(f'../audio/{category}/{file_name}.mp3')

if __name__ == "__main__":
    data = [
        {'summary': 'Text for audio 1', 'file_name': 'audio1'},
        {'summary': "Based on the provided information, here's a summary of the key points:\n\n1. Samsung has released the Galaxy S25 series in January 2025.\n\n2. The Samsung Galaxy S25 pre-orders will now be offered for free with Google's Circle to Search feature.\n\n3. Some notable new features and improvements on the pre-order offer include:\n   - Improved camera quality (up from 40MP to 50MP)\n   - Added wireless charger for free\n   - Case and charger included in some countries\n\n4. The Samsung Galaxy S25 series includes various models, including:\n\n- The 3D computer-generated influencer\n- A new hairstyle (pre-order option)\n- Better battery life \n- Improved display features (screenshot: Circle to Search)\n\nThe update is part of a broader strategy by Samsung to enhance the Galaxy line with new hardware and software improvements. Some fans are expressing concern about the decision to remove Bluetooth capabilities from the S Pen model.\n\n5. The pre-order offer provides limited benefits but offers good value for money considering the price point.\n\n6. Some changes include:\n\n- A new hairstyle (pre-order option)\n- Improved camera quality\n- Additional battery life\n\n7. It's not clear if this is a significant change or an ongoing update by Samsung to their Galaxy products line.\n\nI hope that helps summarize the key points! If you have any specific questions, feel free to ask.", 'file_name': 'audio2'},
        {'summary': 'Text for audio 3', 'file_name': 'audio3'}
    ]
    
    run_text_2_speech(data[1]['summary'], 'tech', data[1]['file_name'])