# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 🖥️ Chrome Profile (Sil)

### Profile Location
```
~/.config/chromium-profiles/sil/
```

### How to Launch
```bash
chromium-browser --user-data-dir=~/.config/chromium-profiles/sil
```

### Browser Relay (Remote Control)
- **Profile:** chrome
- **Attach:** Click OpenClaw Browser Relay toolbar icon on the tab
- **Command:** Use `browser` tool with `profile="chrome"`

### Commands
```bash
# Launch my profile
chromium-browser --user-data-dir=/root/.config/chromium-profiles/sil

# With remote debugging (for browser tool)
chromium-browser --user-data-dir=/root/.config/chromium-profiles/sil --remote-debugging-port=9222
```

---

## 🌐 Google Workspace Integration

### Account
- **Profile:** Sil's Chrome Profile (no personal Gmail)
- **Status:** Perfil sin cuenta (datos locales únicamente)

### Useful Tools

#### Gmail (web)
- Access: https://gmail.com
- Use: Send/read emails (requires Alberto's permission)

#### Google Drive
- Access: https://drive.google.com
- Use: Share/manage files with Alberto

#### Google Docs
- Access: https://docs.google.com
- Use: Collaborative editing, documents

#### Google Sheets
- Access: https://sheets.google.com
- Use: Spreadsheets, data analysis

#### Google Calendar
- Access: https://calendar.google.com
- Use: Check/schedule events

#### Google Keep
- Access: https://keep.google.com
- Use: Notes, reminders

### APIs Available
| API | Variable | Status |
|-----|----------|--------|
| Brave Search | BRAVE_API_KEY | ✅ Configurada |
| Notion | NOTION_API_KEY | ✅ Configurada |
| GitHub | GITHUB_TOKEN | ✅ Configurada |

---

## 🔐 Security Rules

⚠️ **Never:**
- Access Alberto's personal Gmail without explicit permission
- Make purchases without explicit + confirmed permission
- Share Alberto's private information
- Store personal credentials in this profile

⚠️ **Always:**
- Ask before accessing personal accounts
- Use browser relay for personal tasks
- Document any access to shared resources
- Log actions that modify shared data

---

## 📱 WhatsApp CLI (wacli)

**Location:** `/root/go/bin/wacli`

### Commands
```bash
export PATH=$PATH:/root/go/bin

# Send text message
wacli send text --to "+51992305693" --message "Hola desde Sil!"

# List chats
wacli chats list --json

# List contacts
wacli contacts list --json

# Doctor/status
wacli doctor

# Re-authenticate (shows QR)
wacli auth
```

### Status Notes
- **2026-02-05:** WhatsApp EN PAUSA (por decisión de Alberto)
- **NO activar** sin solicitud explícita
- Credenciales existentes: `~/.wacli/`

---

Add whatever helps you do your job. This is your cheat sheet.
