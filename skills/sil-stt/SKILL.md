---
name: sil-stt
description: Local speech-to-text using faster-whisper (multilingual, offline)
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins:
        - "~/.openclaw/tools/stt"
    install:
      - label: "Install faster-whisper"
        run: |
          pip3 install --break-system-packages faster-whisper
      - label: "Create wrapper script"
        run: |
          cat > ~/.openclaw/tools/stt << 'EOF'
#!/bin/bash
MODEL="${2:-base}"
AUDIO_FILE="$1"
python3 -c "
import sys
from faster_whisper import WhisperModel
model = WhisperModel('$MODEL', device='cpu', compute_type='int8')
segments, info = model.transcribe('$AUDIO_FILE', beam_size=5)
print(f'Idioma: {info.language} ({info.language_probability:.0%})')
for segment in segments:
    print(segment.text.strip())
"
EOF
          chmod +x ~/.openclaw/tools/stt
---

# sil-stt

Local speech-to-text using faster-whisper.

## Usage

```bash
stt audio.wav [--model tiny|base|small|medium]
```

## Examples

```bash
# Transcribir audio
stt recording.wav

# Usar modelo más preciso
stt recording.wav --model medium
```

## Models

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~40MB | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| base | ~70MB | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| small | ~250MB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| medium | ~500MB | ⚡⚡ | ⭐⭐⭐⭐⭐ |

## Notes

- Multilingual support (100+ languages)
- Automatic language detection
- CPU-optimized with int8 quantization
- Works offline after model download
