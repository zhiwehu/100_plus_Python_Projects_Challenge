import speech_recognition as sr


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
        text = recognizer.recognize_google(audio)
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
        print(speech_text)
        # get your speech text
        speech_text = recognize_speech_from_mic(recognizer, microphone)

    if speech_text:
        print('{} {}'.format(speech_text, '✓'))
    else:
        print('Please try the speech recognization service later or change another one.')
