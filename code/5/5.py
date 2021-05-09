import speech_recognition as sr
from aip import AipSpeech

# Please signup baidu ASR service：https://ai.baidu.com/tech/speech/asr
VOICE_APP_ID = 'YOUR_ASR_APP_ID'
VOICE_API_KEY = 'YOUR_ASR_APP_KEY'
VOICE_SECRET_KEY = 'YOUR_ASR_SECRET_KEY'
voice_client = AipSpeech(VOICE_APP_ID, VOICE_API_KEY, VOICE_SECRET_KEY)


# baidu asr service
def asr(audio_data):
    wav_data = audio_data.get_wav_data(
        convert_rate=16000,
        convert_width=2
    )
    res = voice_client.asr(wav_data, 'wav', 16000, {
        'dev_pid': 1737,
    })
    if res['err_no'] == 0:
        return ''.join(res['result'])
    else:
        return ''


def recognize_speech_from_mic(recognizer, microphone):
    '''
    Transcribe speech from recorded from `microphone`.
    :param recognizer:
    :param microphone:
    :return: `None` if speech could not be transcribed, otherwise a string containing the transcribed text
    '''
    print('Please read the English sentence')
    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # try recognizing the speech in the recording
    try:
        text = asr(audio)
    except Exception as e:
        print(e)
        text = None

    return text


if __name__ == '__main__':
    # input a English word or sentence
    text = input('Please input a English word or sentence: ').strip()

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get your speech text
    speech_text = recognize_speech_from_mic(recognizer, microphone)

    while speech_text != None and text.lower() != speech_text.lower():
        print('{} ×'.format(speech_text))
        # get your speech text
        speech_text = recognize_speech_from_mic(recognizer, microphone)

    if speech_text:
        print('{} {}'.format(speech_text, '✓'))
    else:
        print('Please try the speech recognization service later or change another one.')
