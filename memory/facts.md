# Facts (Conocimientos)

> Generado automáticamente de memory.db el 2026-02-08 12:49

## Facts

| Key | Valor | Categoría | Confianza |
|-----|-------|-----------|------------|

| comando:35520f8b | sil.albertofarah.com... | comando | 1.0 |
| comando:3fe75fa3 | ui.sil.albertofarah.com... | comando | 1.0 |
| comando:cc1354b8 | sil-network... | comando | 1.0 |
| comando:abcf2ec7 | json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
... | comando | 1.0 |
| comando:665e9d17 | 

### URLs de Acceso

| Método | URL | Puerto | Estado |
|--------|-----|--------|--------|
| **Tail... | comando | 1.0 |
| comando:9809b8aa | 
- **Ubicación:** ... | comando | 1.0 |
| comando:f808111a | 

### Dispositivos Emparejados
- **Laptop (laptop-j5hbefd2):** Aprobado (2026-02-04 21:32)
- **iPhon... | comando | 1.0 |
| comando:ef449a99 | caddyfile
reverse_proxy 127.0.0.1:18789 {
    header_up Connection "upgrade"
    header_up Upgrade "... | comando | 1.0 |
| comando:2d2ccd04 | 

### Error 2: Not Found en Tailscale Serve

**Problema:** Tailscale Serve devolvía 404.

**Causa:**... | comando | 1.0 |
| comando:2336506f | bash
tailscale serve --bg --https=8443 127.0.0.1:18789
... | comando | 1.0 |
| comando:1112baad | 

### Error 3: Pairing Required

**Problema:** UI pedía "pairing required".

**Causa:** Primera cone... | comando | 1.0 |
| comando:c51ab722 | bash
openclaw devices list
openclaw devices approve <requestId>
... | comando | 1.0 |
| comando:8c458517 | 

---

## 🖥️ Chrome Profile (Sil)

### Profile Location
... | comando | 1.0 |
| comando:13b5f1eb | 
~/.config/chromium-profiles/sil/
... | comando | 1.0 |
| comando:9e8fd6a0 | 

### Commands
... | comando | 1.0 |
| comando:31101888 | bash
# Launch my profile
chromium-browser --user-data-dir=/root/.config/chromium-profiles/sil
... | comando | 1.0 |
| comando:924badfe | 

### Browser Relay (Remote Control)
- **Profile:** chrome
- **Attach:** Click OpenClaw Browser Rela... | comando | 1.0 |
| comando:d6ebb4d6 |  tool with ... | comando | 1.0 |
| comando:74e76b93 | 

---

## 🌐 Google Workspace Integration

### Reglas de Seguridad
⚠️ **Nunca:**
- Acceder al Gmail p... | comando | 1.0 |
| comando:cf252a7b | bash
# Variable de entorno
export GOG_ACCOUNT="alberto.farah.b@gmail.com"
export GOG_KEYRING_PASSWOR... | comando | 1.0 |
| comando:fb19e635 | 

### Comandos Útiles

**Gmail:**
... | comando | 1.0 |
| comando:f82588ea | bash
gog gmail labels list
gog gmail search 'newer_than:7d --max 10'
gog gmail send --to a@b.com --s... | comando | 1.0 |
| comando:acaa8ee9 | 

**Calendar:**
... | comando | 1.0 |
| comando:a0742fdc | bash
gog calendar events --today
gog calendar events --week
gog calendar search "meeting" --from 202... | comando | 1.0 |
| comando:74d62c57 | 

**Drive:**
... | comando | 1.0 |
| comando:7068093b | bash
gog drive ls
gog drive search "query"
gog drive upload ./file.txt --name "File"
... | comando | 1.0 |
| comando:9262e689 | 

**Sheets:**
... | comando | 1.0 |
| comando:a0cd0578 | bash
gog sheets get <sheetId> "Tab!A1:D10" --json
gog sheets update <sheetId> "Tab!A1" --values-json... | comando | 1.0 |
| comando:b280af78 | 

**Docs:**
... | comando | 1.0 |
| comando:64c0bdb4 | bash
gog docs cat <docId>
gog docs export <docId> --format txt --out /tmp/doc.txt
... | comando | 1.0 |
| comando:9b6ea0ca | 

**Tasks:**
... | comando | 1.0 |
| comando:f315d1eb | bash
gog tasks list <tasklistId>
... | comando | 1.0 |
| comando:e6bb3dbc | 

**Contacts:**
... | comando | 1.0 |
| comando:d1ea01ae | bash
gog contacts list --max 20
... | comando | 1.0 |
| comando:92282c94 | 

### Slides
Slides no tiene comando nativo, se accede via Drive:
... | comando | 1.0 |
| comando:3e07f1c3 | bash
# Buscar slides
gog drive search "mimeType='application/vnd.google-apps.presentation'"

# Expor... | comando | 1.0 |
| comando:2044683d | 

---

## Reglas de Seguridad Aplicadas

1. ✅ Firewall UFW habilitado
2. ✅ SSH hardening (no root lo... | comando | 1.0 |
| comando:b4608488 | 

### Google Cloud TTS
- **Instalado:** ✅
- **Voces:** es-ES-Neural2-A (femenina natural)
- **Gratis... | comando | 1.0 |
| comando:f8814496 | 
- **Voz por defecto:** es-ES-Neural2-A

#### Uso de TTS
... | comando | 1.0 |
| comando:f2d80f00 | bash
# Generar audio
~/.openclaw/tools/google-tts.py "Hola mundo" --voice es-ES-Neural2-A

# Listar ... | comando | 1.0 |
| comando:566d7f68 | 

---

## 🌐 Google OAuth Completo - 2026-02-05

### Sistema de Tokens Unificado

**Ubicación:** ... | comando | 1.0 |
| comando:a4331116 | 
- **Credenciales:** ... | comando | 1.0 |
| comando:d2283d89 | 
- **Tokens:** ... | comando | 1.0 |
| comando:d58abbf1 | 
- **Gestor:** ... | comando | 1.0 |
| comando:e2680c89 | 

### Scopes Autorizados (13/13)

| Servicio | Scope | Funcionalidades |
|----------|-------|-------... | comando | 1.0 |
| comando:1075cc99 |  | Leer correos |
| | ... | comando | 1.0 |
| comando:19f3de16 |  | ✅ Enviar correos |
| | ... | comando | 1.0 |
| comando:249b4e5f |  | ✅ Organizar, etiquetar |
| | ... | comando | 1.0 |
| comando:457fea18 |  | ✅ Crear borradores |
| **Calendar** | ... | comando | 1.0 |
| comando:7a7c6e25 |  | ✅ Crear/modificar/eliminar eventos, invitar |
| **Drive** | ... | comando | 1.0 |
| comando:64d98ba2 |  | ✅ Gestionar archivos |
| **Docs** | ... | comando | 1.0 |
| comando:ba3d3366 |  | ✅ Editar documentos |
| **Sheets** | ... | comando | 1.0 |
| comando:37d8e8e2 |  | ✅ Editar hojas de cálculo |
| **Tasks** | ... | comando | 1.0 |
| comando:8e966a98 |  | ✅ Gestionar tareas |
| **Contacts** | ... | comando | 1.0 |
| comando:5a636d0e |  | ✅ Leer contactos |
| | ... | comando | 1.0 |
| comando:1aa97e80 |  | ✅ Agregar/editar contactos |
| **Meet** | ... | comando | 1.0 |
| comando:b539ea85 |  | ✅ Crear reuniones |
| **Cloud TTS** | ... | comando | 1.0 |
| comando:36b6b168 |  | ✅ Voces naturales |

### Scripts Disponibles

| Script | Uso |
|--------|-----|
| ... | comando | 1.0 |
| comando:e241a4ea |  | Ver estado de tokens |
| ... | comando | 1.0 |
| comando:672b82a0 |  | Renovar tokens |
| ... | comando | 1.0 |
| comando:0dc45047 |  | Listar correos |
| ... | comando | 1.0 |
| comando:d52d3161 |  | Enviar correo |
| ... | comando | 1.0 |
| comando:9d1555e0 |  | Ver eventos |
| ... | comando | 1.0 |
| comando:f2d5719f |  | Crear evento |
| ... | comando | 1.0 |
| comando:49ba64c3 |  | Listar contactos |
| ... | comando | 1.0 |
| comando:283863b3 |  | Agregar contacto |
| ... | comando | 1.0 |
| comando:2512e9db |  | Crear reunión |
| ... | comando | 1.0 |
| comando:194802bd |  | Generar voz |

### Token Status
- **Cuenta:** alberto.farah.b@gmail.com
- **Expiry:** Renovado au... | comando | 1.0 |
| comando:6e9a0cc2 |  - Gestor de tokens OAuth
- ... | comando | 1.0 |
| comando:3b55e5a1 |  - Gestión Gmail
- ... | comando | 1.0 |
| comando:e5df74ce |  - Gestión Calendar
- ... | comando | 1.0 |
| comando:448e4f33 |  - Gestión Contacts
- ... | comando | 1.0 |
| comando:dc1a0802 |  - Gestión Meet
- ... | comando | 1.0 |
| comando:f107e3e3 |  - Text to Speech
- ... | comando | 1.0 |
| comando:c046bb23 |  - Intercambio código por tokens

---

## 📋 Configuración gogcli (anterior)

**Nota:** gogcli aún ti... | comando | 1.0 |
| comando:836e0286 |  directamente.

---

## Próximos Pasos

1. [ ] Probar UI desde laptop (ya funcionando)
2. [ ] Config... | comando | 1.0 |
| comando:ffe9219f |  a git
- Usar siempre claves SSH para acceso
- Revisar logs regularmente: ... | comando | 1.0 |
| comando:dea1db80 | 
- Mantener sistema actualizado: ... | comando | 1.0 |
| comando:bf42a339 | 
- Gateway debe quedarse en loopback para seguridad
- Acceso remoto por Tailscale Serve (puerto 8443... | comando | 1.0 |
| comando:49807268 | bash
# Estado de Tailscale
tailscale status

# Estado del serve
tailscale serve status

# Reiniciar ... | comando | 1.0 |
| comando:da33b986 | 

---

## 🔍 Investigación OpenClaw - Casos Avanzados (2026-02-05)

### Voces TTS - Descubrimiento Im... | comando | 1.0 |
| comando:d3907ee1 |  (femenina) - La más natural
  - ... | comando | 1.0 |
| comando:2aad748e |  (femenina) - Clásica y muy natural
- **Alternativas para acento peruano:**
  - ElevenLabs ($5-11/me... | comando | 1.0 |
| comando:53016709 |  |
| **Protocolo Anti-Alucinaciones** | Drive: "Pt titiló de mitigación de alucinaciones" |
| **USER... | comando | 1.0 |
| comando:8486794b |  |
| **MEMORY.md actualizado** | ... | comando | 1.0 |
| drive:drive.google.com | https://drive.google.com... | drive_link | 1.0 |
| drive:1KAL82md9CU67Fsns3rM7iiPZmJed1dkC | https://drive.google.com/drive/folders/1KAL82md9CU67Fsns3rM7iiPZmJed1dkC... | drive_link | 1.0 |
| comando:b8e4694a | 
INPUT: Query → Web Search → Web Fetch → AI Analysis → OUTPUT
                                      ... | comando | 1.0 |
| comando:f8f3d56c | 
QUERY → 🔍 Web → 📄 Fetch → 🧠 IA → 🖼️ GLM-Image → ☁️ Drive
                                          ... | comando | 1.0 |
| comando:ea4e384c | 

### 🎯 HERRAMIENTAS DEL ECOSISTEMA

... | comando | 1.0 |
| comando:a7b59845 | 
┌─────────────────────────────────────────────────────────────┐
│                    ECOSISTEMA SIL... | comando | 1.0 |
| comando:771e83b0 | 

### 📋 PRÓXIMAS TAREAS

1. **Probar Auto-Researcher** con query real
2. **Testear PDF** con ReportL... | comando | 1.0 |
| comando:f630c508 | 
QUERY → 🔍 Brave Search → 📄 Fetch → 🧠 AI Analysis → 🖼️ GLM → 📑 PDF
... | comando | 1.0 |
| comando:ef023483 | 

**Resultados:**
- ✅ 5 fuentes encontradas (IBM, Google, MIT, etc.)
- ✅ 5 artículos extraídos
- ⚠️ ... | comando | 1.0 |
| comando:c3ab9408 |  |
| **Brave Search** | ... | comando | 1.0 |
| comando:ebe2a229 |  | ✅ ... | comando | 1.0 |
| comando:dc92fbf7 |  |
| **MiniMax** | Integrado en OpenClaw | ⏳ Para integrar directamente |

### Archivos Generados
- ... | comando | 1.0 |
| comando:5391bd95 |  (3.4 KB)
- ... | comando | 1.0 |
| contacto:+51927845269 | +51927845269... | contacto | 1.0 |
| comando:31e80685 | /root/.openclaw/settings/tts.json... | comando | 1.0 |
| comando:8add52b5 | auto: "always"... | comando | 1.0 |
| comando:df513778 | openclaw.json... | comando | 1.0 |
| comando:23d0f000 | settings/tts.json... | comando | 1.0 |
| comando:20b0b20f | /root/.openclaw/workspace/data/contacts.db... | comando | 1.0 |
| comando:20bb344d | bash
openclaw message send --channel whatsapp --target "+51927845269" --message "Tu mensaje aquí"
... | comando | 1.0 |
| comando:03b634d8 | 

### Pasos para Nuevos Contactos
1. Agregar a la base de datos SQLite: ... | comando | 1.0 |
| comando:3a651739 | 
2. Usar el comando ... | comando | 1.0 |
| comando:4dff3268 | 

### Contactos Existentes
| Nombre | Teléfono |
|--------|----------|
| Alberto Farah | +5192784526... | comando | 1.0 |
| comando:c19844fd | 
- Keys probadas: 2 diferentes
- Ambas fallaban

### Descubrimiento
... | comando | 1.0 |
| comando:2b0ae361 | 
Variable de entorno: eef6f87167c343c390de5f66429e14d3.cHam1KOy1iDO3tcX (49 chars)
Archivo .env:    ... | comando | 1.0 |
| comando:ca4bd30c | 

**Causa:** El ... | comando | 1.0 |
| comando:e991dd65 |  tenía la key sin el sufijo después del punto

### Solución
1. Actualizar ... | comando | 1.0 |
| comando:6f8cb9af |  con key completa
2. Verificar funcionamiento (Status 200 ✅)

---

## 📦 GitHub Backup Creado

- **Re... | comando | 1.0 |
| comando:ecce64c2 |  como ... | comando | 1.0 |
| comando:cc4fbe2e | 
2. **API Keys:** Verificar que estén completas (no truncadas)
3. **Scripts:** Borrar duplicados ant... | comando | 1.0 |
| comando:6db26f69 |  con ... | comando | 1.0 |
| comando:15712abd |  para links compartibles
4. **Z.ai funciona:** API key con sufijo completo (... | comando | 1.0 |
| comando:bb3a95ce | )
5. **WhatsApp vía OpenClaw:** ... | comando | 1.0 |
| comando:6584f3d6 | 

---

## 🔐 Recordatorio de Permisos Drive

Para compartir links públicamente:
... | comando | 1.0 |
| comando:eb04c8f4 | python
requests.post(
    f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions",
    he... | comando | 1.0 |
| drive:1T9MojQxPxDLIZvmhdHI7r2pKnDpRY2d0 | https://drive.google.com/drive/folders/1T9MojQxPxDLIZvmhdHI7r2pKnDpRY2d0... | drive_link | 1.0 |
| comando:6b959b8e | --store=/root/.openclaw/credentials/whatsapp... | comando | 1.0 |
| comando:e367e0e8 | sil-whatsapp.service... | comando | 1.0 |
| comando:027c407d | /root/.openclaw/credentials/whatsapp.backup... | comando | 1.0 |
| comando:2aa60aa7 | session-*.json... | comando | 1.0 |
| comando:cf1d7d65 | pre-key-*.json... | comando | 1.0 |
| comando:337239c1 | sender-key-*.json... | comando | 1.0 |
| comando:c48681d5 | app-state-sync-key-*.json... | comando | 1.0 |
| comando:58ee2d23 | creds.json... | comando | 1.0 |
| comando:c0d10805 | tctoken-*.json... | comando | 1.0 |
| comando:f32676b5 | bash
# Verificar estado con credenciales de OpenClaw
export PATH=$PATH:/root/go/bin && wacli --store... | comando | 1.0 |


## Patterns (Patrones)

| Patrón | Contexto | Ejemplos |
|--------|----------|----------|

