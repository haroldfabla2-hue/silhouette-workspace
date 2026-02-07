---
name: google-tts
description: Google Cloud Text-to-Speech for Spanish audio generation. Use when you want to convert text to audio.
homepage: https://cloud.google.com/text-to-speech
metadata:
  {
    "openclaw":
      {
        "emoji": "🎤",
        "requires": { "bins": ["python3"] },
        "install": [],
      },
  }
---

# Google Cloud TTS

Use this skill to generate Spanish audio from text.

## Commands

### Generate Audio
```bash
python3 /root/.openclaw/tools/google-tts.py synthesize "Tu texto aquí"
```

### List Voices
```bash
python3 /root/.openclaw/tools/google-tts.py voices
```

## Best Voice for Spanish
- **es-ES-Chirp3-HD-Aoede** (FEMALE) - Best quality
- **es-ES-Chirp3-HD-Algieba** (MALE) - Alternative

## Usage Examples

When you want to convert text to audio:

1. Use the command to generate audio
2. Share the audio file with the user
3. The file is saved as MP3 in /tmp/

## Notes
- Requires Google OAuth tokens (already configured)
- No API key needed - uses OAuth automatically
- Works offline once tokens are refreshed
