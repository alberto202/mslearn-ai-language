from dotenv import load_dotenv
from datetime import datetime
from playsound import playsound
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk


def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure speech service
        
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        speech_config.speech_recognition_language = "es-ES"
        print('Ready to use speech service in:', speech_config.region)
        

        # Get spoken input
        command = TranscribeCommand()
        #if command.lower() == 'what time is it?':
        #    TellTime()

        if command.lower() == 'dime la hora.':
            TellTime()


    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)


    # Return the command
    return command


def TellTime():
    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = "es-ES-AlvaroNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    now = datetime.now()
    #response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)
    response_text = 'La hora en este momento es {}:{:02d}'.format(now.hour, now.minute)

    # Synthesize spoken output

    responseSsml = ' \
        <speak version="1.0" xml:lang="en-US" xmlns:mstts="http://www.w3.org/2001/mstts"> \
            <mstts:backgroundaudio src="https://www2.cs.uic.edu/~i101/SoundFiles/StarWars60.wav" volume="0.3" /> \
            <voice name="es-ES-AlvaroNeural"> \
                  <prosody pitch="high" rate="medium"> <emphasis level="strong"> ¡Oooo! </emphasis> </prosody> \
                  <prosody pitch="medium" rate="medium"> si son las {}:{:02d} </prosody> \
                  <break strength="weak" /> \
            </voice> \
            <voice name="es-ES-EstrellaNeural"> \
                <p> <s>Genial nos vamos a casa</s> </p> \
            </voice> \
        </speak>'.format(now.hour, now.minute)
    
    speak = speech_synthesizer.speak_ssml_async(responseSsml).get()

    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)    

    
    # Synthesize spoken output
    #speak = speech_synthesizer.speak_text_async(response_text).get()
    #if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
    #    print(speak.reason)

    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()