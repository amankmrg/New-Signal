from pyannote.audio import Pipeline

# Replace "${ACCESS_TOKEN_GOES_HERE}" with your authentication token
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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")

# Replace "${AUDIO_FILE_PATH}" with the path to your audio file
diarization = pipeline("C:/Users/amank/Downloads/WhatsApp Audio 2024-04-11 at 13.05.26_932b139d.mp3")

for segment, _, speaker in diarization.itertracks(yield_label=True):
    print(f'Speaker "{speaker}" - "{segment}"')
