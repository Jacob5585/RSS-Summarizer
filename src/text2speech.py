from kokoro import KPipeline
import soundfile as sf
pipeline = KPipeline(lang_code='a') # Set to American English
import numpy as np
import concurrent

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

def sanatize_text(text):
    text = text.replace("*", " ").replace("#", " ").replace("\n", " ").replace("'", "\'")
    return repr(text)

def save_audio(audio, file_name):
    sf.write(file_name, audio, 24000)

def run_text_2_speech(data, catagory, file_name):
    text = sanatize_text(data)
    print(f"file_name: {file_name}")
    audio = text_2_speech(text)
    save_audio(audio, f'../audio/{catagory}/{file_name}.mp3')

def convert_to_audio(data, catagory):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for item in data:
            executor.submit(run_text_2_speech, item['summary'], catagory, item['file_name'])

if __name__ == "__main__":
    # text = 'The article discusses the latest updates made by Apple for their iPhone users, particularly on the T-Mobile and Starlink satellite network. Here is a summary of key points:\n\n1. **Starlink Service**: Apple has enabled support for T-Mobile customers to send text messages even in areas where they don\'t have coverage.\n\n2. **Direct-to-Cell Satellitic Service (DTCS)**: This service allows users to receive text messages from their T-Mobile phone or Starlink satellite in locations without cell towers.\n\n3. **Beta Testing**: The update is currently being trialed by the companies involved, including SpaceX and Globalstar, which provides a similar service called the \"direct-to-cell\" service.\n\n4. **iPhone Beta Software Update (iOS 18.3)**: Users who have registered for beta testing are experiencing some changes. They\'ll need to update their iOS settings using \"Update to iOS 18.3\" to start receiving support for T-Mobile\'s Starlink satellite network and enabling text messaging on the iPhone.\n\n5. **Apple\u2019s partnership with Globalstar**: This service provides users with texting capabilities when they\'re out of coverage, similar to what Apple has in place for its own services.\n6. **Future Plans**: Apple is working on adding voice and data connectivity to give users more options in areas without cellular internet coverage.\n7. **Other Services**: The article mentions that Apple is also exploring various other services like NordVPN\'s NordWhisper protocol, which bypasses VPN blocks.\n\nThe update aims to provide a more seamless user experience across different networks and regions.'
    
    data = [
        {'summary': 'Text for audio 1', 'file_name': 'audio1'},
        {'summary': "Based on the provided information, here's a summary of the key points:\n\n1. Samsung has released the Galaxy S25 series in January 2025.\n\n2. The Samsung Galaxy S25 pre-orders will now be offered for free with Google's Circle to Search feature.\n\n3. Some notable new features and improvements on the pre-order offer include:\n   - Improved camera quality (up from 40MP to 50MP)\n   - Added wireless charger for free\n   - Case and charger included in some countries\n\n4. The Samsung Galaxy S25 series includes various models, including:\n\n- The 3D computer-generated influencer\n- A new hairstyle (pre-order option)\n- Better battery life \n- Improved display features (screenshot: Circle to Search)\n\nThe update is part of a broader strategy by Samsung to enhance the Galaxy line with new hardware and software improvements. Some fans are expressing concern about the decision to remove Bluetooth capabilities from the S Pen model.\n\n5. The pre-order offer provides limited benefits but offers good value for money considering the price point.\n\n6. Some changes include:\n\n- A new hairstyle (pre-order option)\n- Improved camera quality\n- Additional battery life\n\n7. It's not clear if this is a significant change or an ongoing update by Samsung to their Galaxy products line.\n\nI hope that helps summarize the key points! If you have any specific questions, feel free to ask.", 'file_name': 'audio2'},
        {'summary': 'Text for audio 3', 'file_name': 'audio3'}
    ]
    
    # convert_to_audio(text, 'tech', 'test_file')
    convert_to_audio(data, 'tech')