# HEARTBEAT.md - Sistema Completo de Verificaciones

> Actualizado: 2026-02-08

## 📊 Resumen del Sistema

### ✅ CREDENCIALES CONFIGURADAS
| API/Service | Status | Location |
|--------------|--------|----------|
| Google Cloud OAuth | ✅ | ~/.config/gcloud/, ~/.openclaw/google-oauth/ |
| ElevenLabs | ✅ | ~/.config/elevenlabs/api_key.txt |
| GitHub | ✅ | /root/.openclaw/.env |
| Replicate | ✅ | /root/.openclaw/.env |
| MiniMax | ✅ | /root/.openclaw/.env |
| Brave Search | ✅ | /root/.openclaw/.env |
| Z.AI GLM | ✅ | /root/.openclaw/.env |

---

## 📦 SKILLS DEL WORKSPACE (14)

| Skill | Status | Propósito |
|-------|--------|-----------|
| **auto-researcher** | ✅ | Research automation |
| **bird** | ✅ | X/Twitter CLI |
| **gemini** | ✅ | Gemini CLI |
| **github** | ✅ | GitHub CLI |
| **google-tts** | ✅ | Google Cloud TTS |
| **google-workspace** | ✅ | Google Workspace (gog) |
| **healthcheck** | ✅ | Water/sleep tracking |
| **notion** | ✅ | Notion API |
| **sil-stt** | ✅ | Speech-to-text |
| **skill-creator** | ✅ | Create skills |
| **tmux** | ✅ | Remote control |
| **video-frames** | ✅ | Extract frames from video |
| **wacli** | ⏸️ | WhatsApp (paused) |
| **weather** | ✅ | Weather |

---

## 📦 SKILLS DEL SISTEMA (55+)

| Categoría | Skills |
|-----------|--------|
| **Messaging** | discord, slack, wacli |
| **Notes/Productivity** | apple-notes, bear-notes, notion, obsidian |
| **AI/ML** | coding-agent, gemini, github, openai-whisper-api |
| **Voice/TTS** | sag (ElevenLabs), sherpa-onnx-tts, voice-call |
| **Images** | camsnap, openai-image-gen |
| **Media** | gifgrep, spotify-player, sonoscli, songsee |
| **Productivity** | gog, healthcheck, weather, trello |
| **Utilities** | 1password, bluebubbles, clawhub, session-logs |
| **Automation** | tmux, video-frames, summarizer |

---

## 🤖 APIs DISPONIBLES

| API | Status | Propósito |
|-----|--------|----------|
| **MiniMax** | ✅ | IA principal |
| **Brave Search** | ✅ | Web search |
| **Z.AI GLM** | ✅ | Generación de imágenes |
| **OpenAI Whisper** | ✅ | Speech-to-text |
| **OpenWeatherMap** | ✅ | Clima |
| **GitHub (gh)** | ✅ | Git CLI |
| **Replicate** | ✅ | Modelos IA |
| **Google Workspace** | ✅ | Gmail, Drive, Docs, Sheets, Calendar |

---

## 🛠️ HERRAMIENTAS LOCALES (40+ scripts)

### Chrome & Browser
| Script | Propósito |
|--------|----------|
| chrome-auto.py | Automation básico |
| chrome-auto-v2.py | Automation v2 |
| chrome-controller.py | Controlador CDP |

### Google Workspace
| Script | Propósito |
|--------|----------|
| google-tts.py | Text-to-Speech |
| google_oauth.py | OAuth manager |
| google-contacts.py | Contacts |
| google-drive-read.py | Drive reader |
| google-gmail.py | Gmail integration |
| google-meet.py | Google Meet |
| google-refresh-helper.py | Token refresh |

### GLM Image Generation
| Script | Propósito |
|--------|----------|
| glm-image.py | Generador de imágenes |
| glm-image-v2.py | Generador v2 |
| glm-download.py | Downloader |
| glm-drive.py | Upload a Drive |
| glm-workflow.py | Pipeline completo |

### AI & Fallback
| Script | Propósito |
|--------|----------|
| replicate.py | Replicate API |
| sil-fallback-zai.py | Z.AI fallback |
| sil-google-token.py | Token manager |
| sil-stt.py | Speech-to-text |
| tts.py | TTS wrapper |

### Memory & Contacts
| Script | Propósito |
|--------|----------|
| sil-memory-db.py | SQLite memory |
| sil-memory-maintenance.py | Maintenance |
| memory-query.py | Query conversations |
| migrate-memory.py | Migration |
| sil_contacts_db.py | Contacts DB |
| sil-sync-contacts.py | Sync contacts |

### Notifications & Alerts
| Script | Propósito |
|--------|----------|
| notify-alberto.py | Notify Alberto |
| notify-emergency.py | Emergency alerts |
| sil-google-health-monitor.py | Health monitor |

### WhatsApp
| Script | Propósito |
|--------|----------|
| send-whatsapp-robust.py | Robust sender |
| sil-whatsapp-send.py | Send messages |
| sil-whatsapp-send-v3.py | v3 sender |
| sil-wacli-daemon.py | Daemon |

### Utilities
| Script | Propósito |
|--------|----------|
| sil-conversation-logger.py | Logger |
| sil-flocky-processor.py | Flocky processor |
| sil-heartbeat-manager.py | Heartbeat manager |
| iris-escalate.py | Escalation |
| oauth-exchange.py | OAuth exchange |

---

## 🛡️ SUPERVISOR (Flocky v4)

| Componente | Status | Location |
|------------|--------|----------|
| Logs | ✅ | /root/.openclaw/logs/supervisor.log |
| Snapshots | ✅ | /root/.openclaw/supervisor/snapshots/ |
| Alerts | ✅ | /root/.openclaw/supervisor/alerts/ |
| Flocky v4 | ✅ | /root/.openclaw/supervisor/flocky_v4.py |
| Sil Supervisor | ✅ | /root/.openclaw/supervisor/sil-supervisor.py |

---

## 🌐 SERVICIOS ACTIVOS

| Servicio | Puerto | Status |
|----------|--------|--------|
| openclaw-gateway | 18792 | ✅ |
| sil-chrome | 9222 | ✅ |
| caddy | 2019 | ✅ |
| tailscaled | - | ✅ |
| dockerd | - | ✅ |

---

## 📝 BASES DE DATOS

| DB | Location | Propósito |
|----|----------|----------|
| memory.db | /root/.openclaw/workspace/ | Memoria persistente |
| contacts.db | /root/.openclaw/tools/ | Contactos |

---

## Commands de Verificación Rápida

```bash
# Gateway
systemctl --user is-active openclaw-gateway

# Chrome CDP
ss -tlnp | grep 9222

# Credenciales
ls ~/.config/gcloud/*.json
cat ~/.config/elevenlabs/api_key.txt
grep -E "GITHUB|MINIMAX|REPLICATE|BRAVE" /root/.openclaw/.env

# Skills workspace
ls /root/.openclaw/workspace/skills/

# Skills sistema
ls /usr/lib/node_modules/openclaw/skills/

# Servicios
systemctl --user list-units --type=service --state=running

# Cronjobs
openclaw cron list

# Supervisor
tail -5 /root/.openclaw/logs/supervisor.log

# Memoria
python3 /root/.openclaw/tools/sil-memory-db.py stats
```

---

## Resumen de Hoy

[Agregar notas de hoy aquí]
