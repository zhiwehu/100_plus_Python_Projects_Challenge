# Check your English speech using Baidu AI cloud ASR service

## Requirements

1. Run the code in console using command line.
2. It'll let you input a English word or sentence, then it'll let you speak it.
3. It'll record your voice using mic and check if you speak correctly. If not it'll ask you speak it again until you speak it correctly.
4. It''ll will use Baidu AI Cloud ASR service: https://ai.baidu.com/tech/speech/asr

## What will we practice in this project?

- for loop
- input text
- Text lower case
- if conditions
- functions
- exception handle
- SpeechRecognition package (need to install by `pip install SpeechRecognition`)
- pyaudio package (need to install by `pip install pyaudio`)
- baidu-aip package(need to install by `pip install baidu-aip`)

## A reference code

```python
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

```

## Run the demo

- use `pip install requirements.txt` to install packages: `pyaudio`,`baidu-aip` and `SpeechRecognition`
- run it in console

```shell
python 5.py
```

![](images/challenge_5_en.png)

----


# 检测英语口语（使用百度云语音识别）

## 项目需求

1. 在命令行窗口运行；
2. 程序运行时，会让你输入一句英语，然后你需要对着麦克风读出这句英语；
3. 程序会判断你读的对不对，如果不对会让你重读，直到读对为止；
4. 使用百度云语音识别：https://ai.baidu.com/tech/speech/asr。

## Python编程知识点

- while循环
- 用户输入字符串
- 字符串小写
- 条件判断
- 自定义函数
- 异常处理
- SpeechRecognition 模块 (安装： `pip install SpeechRecognition`) 
- pyaudio 模块 (安装： `pip install pyaudio`)
- baidu-aip 模块(安装： `pip install baidu-aip`)

## 参考代码

```python
import speech_recognition as sr
from aip import AipSpeech

# 请自己注册百度云语音识别：https://ai.baidu.com/tech/speech/asr
VOICE_APP_ID = 'YOUR_ASR_APP_ID'
VOICE_API_KEY = 'YOUR_ASR_APP_KEY'
VOICE_SECRET_KEY = 'YOUR_ASR_SECRET_KEY'
voice_client = AipSpeech(VOICE_APP_ID, VOICE_API_KEY, VOICE_SECRET_KEY)


# 百度云语音识别
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
    麦克风录音并转文字 `microphone`.
    :param recognizer: 语音识别器
    :param microphone: 麦克风
    :return: `None` 如果识别失败返回None，否则返回语音文字
    '''
    print('开始朗读')
    # 录音并去除噪音
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # 使用百度云语音识别
    try:
        text = asr(audio)
    except Exception as e:
        print(e)
        text = None

    return text


if __name__ == '__main__':
    # 输入
    text = input('请输入一句英语: ').strip()

    # 创建语音识别器和麦克风
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # 录音并获取文字
    speech_text = recognize_speech_from_mic(recognizer, microphone)

    while speech_text != None and text.lower() != speech_text.lower():
        print('{} ×'.format(speech_text))
        speech_text = recognize_speech_from_mic(recognizer, microphone)

    if speech_text:
        print('{} {}'.format(speech_text, '✓'))
    else:
        print('语音识别服务暂不可用，请稍后再试。')

```
## 运行测试

- 使用 `pip install requirements.txt` 安装模块: `pyaudio` ，`SpeechRecognition`，`baidu-aip`
- 运行

```shell
python 5.py
```

![](images/challenge_5_cn.png)

