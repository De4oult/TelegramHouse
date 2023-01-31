import speech_recognition as sr

reco = sr.Recognizer()

def translate(filename) -> str:
    file = sr.AudioFile(filename)
    try:
        with file as source:
            reco.adjust_for_ambient_noise(source)
            audio = reco.record(source)
            result = reco.recognize_google(audio, language="ru-RU")
        
        return result
    except:
        print('Плохо слышно')