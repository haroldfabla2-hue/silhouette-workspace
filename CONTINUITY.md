# CONTINUITY.md - Para leer después de reiniciar OpenClaw

## 📋 Sistema de Continuidad Automática

### Scripts de Continuidad

| Script | Cuándo ejecutarlo | Qué hace |
|--------|-------------------|----------|
| `sil-startup.sh` | Al iniciar OpenClaw | Restaura contexto |
| `sil-shutdown.sh` | Antes de reiniciar | Consolida memoria |

---

## 📖 Instrucciones de Uso

### Antes de Reiniciar:
```bash
# 1. Consolidar memoria
/root/.openclaw/tools/sil-shutdown.sh

# 2. Verificar que se generó el reporte
cat /root/.openclaw/workspace/REPORT_BEFORE_RESTART.md

# 3. Ahora sí, reiniciar
openclaw gateway restart
```

### Después de Iniciar:
```bash
# 1. Restaurar contexto
/root/.openclaw/tools/sil-startup.sh

# 2. Verificar tareas pendientes
cat /root/.openclaw/workspace/TASKS.md

# 3. Continuar con el trabajo
```

---

## 📋 Estado del Proyecto (2026-02-05 17:10 GMT-5)

### Objetivo Principal
Configurar Google Cloud TTS con voz **es-ES-Chirp3-HD-Aoede** (femenina)

### Lo que se ha completado:
- ✅ Google OAuth configurado y funcionando
- ✅ Token refrescado automáticamente
- ✅ Script google-tts.py funciona correctamente
- ✅ Voz Aoede funciona en el script manual
- ✅ Memoria consolidada en MEMORY.md y daily logs
- ✅ Tareas documentadas en TASKS.md
- ✅ Scripts de continuidad creados:
  - `sil-startup.sh` - Restaura contexto al iniciar
  - `sil-shutdown.sh` - Consolida memoria antes de reiniciar

### Lo que está en progreso:
- ⏳ Integrar Google Cloud TTS con OpenClaw
- ⏳ Plugin personalizado para OpenClaw

### Problema Identificado:
OpenClaw usa ElevenLabs/OpenAI/Edge TTS por defecto.
**Google Cloud TTS NO está soportado nativamente.**

---

## 🔧 Plan de Acción

### Paso 1: Crear Plugin de Google Cloud TTS
```bash
# Crear directorio del plugin
mkdir -p /usr/lib/node_modules/openclaw/extensions/google-tts/
cd /usr/lib/node_modules/openclaw/extensions/google-tts/

# Crear archivos del plugin
- openclaw.plugin.json
- index.js (plugin principal)
```

### Paso 2: Integrar con Sistema de TTS
El plugin debe:
1. Exportar función de TTS
2. Conectar con el sistema de mensajes de OpenClaw
3. Generar audio cuando se envíe un mensaje con TTS

### Paso 3: Probar y Validar
1. Ejecutar `sil-shutdown.sh` antes de reiniciar
2. Reiniciar OpenClaw
3. Ejecutar `sil-startup.sh` después de iniciar
4. Enviar mensaje con TTS
5. Verificar que use voz Aoede

---

## 📁 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `/root/.openclaw/tools/sil-startup.sh` | Script de inicio (leer al despertar) |
| `/root/.openclaw/tools/sil-shutdown.sh` | Script de cierre (ejecutar antes de dormir) |
| `/root/.openclaw/tools/google-tts.py` | Script de Google Cloud TTS |
| `/root/.openclaw/tools/tts-wrapper.sh` | Wrapper para ejecutar TTS |
| `/root/.openclaw/workspace/MEMORY.md` | Memoria consolidada |
| `/root/.openclaw/workspace/TASKS.md` | Tareas pendientes |
| `/root/.openclaw/workspace/memory/2026-02-05.md` | Log diario |
| `/root/.openclaw/workspace/REPORT_BEFORE_RESTART.md` | Reporte antes de reiniciar |
| `/root/.openclaw/workspace/REPORT_AFTER_STARTUP.md` | Reporte después de iniciar |

---

## 🔑 Comandos para Continuar

```bash
# 1. Verificar estado del proyecto
cat /root/.openclaw/workspace/CONTINUITY.md

# 2. Ver tareas pendientes
cat /root/.openclaw/workspace/TASKS.md

# 3. Ver memoria consolidada
cat /root/.openclaw/workspace/MEMORY.md | tail -50

# 4. Probar script de TTS
/root/.openclaw/tools/tts-wrapper.sh "Hola, soy Sil"

# 5. Verificar token de Google
python3 /root/.openclaw/tools/google_oauth.py check

# 6. Antes de reiniciar
/root/.openclaw/tools/sil-shutdown.sh

# 7. Después de iniciar
/root/.openclaw/tools/sil-startup.sh
```

---

## ⚠️ Notas Importantes

1. **Token de Google:** Se refresca automáticamente con google_oauth.refresh_token()
2. **Voz:** es-ES-Chirp3-HD-Aoede (femenina, natural)
3. **Output:** /tmp/sil-tts-output.mp3
4. **Credenciales:** En /root/.openclaw/google-oauth/

---

## 📋 Flujo de Trabajo Recomendado

```
┌─────────────────────────────────────────────────────┐
│                    OPENCLAW                        │
│                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │  INICIAR   │ →  │  TRABAJAR  │ →  │ DORMIR  │ │
│  │            │    │            │    │         │ │
│  │sil-startup │    │  ...       │    │sil-shutd│ │
│  └─────────────┘    └─────────────┘    └─────────┘ │
│        ↓                  ↓                   ↓      │
│   Lee contexto      Trabaja          Consolida     │
│   Lee Tasks.md     normal            memoria       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Siguiente Paso

1. Crear plugin de Google Cloud TTS para OpenClaw
2. Integrar con sistema de TTS
3. Probar con voz Aoede

---

*Creado: 2026-02-05 16:59 GMT-5*
*Última actualización: 2026-02-05 17:10 GMT-5*
*Este archivo se leerá automáticamente después de reiniciar OpenClaw*


---

## 📋 CONSOLIDACIÓN DE MEMORIA: AMBOS

### Timing:
- **ANTES del reinicio** (sil-shutdown.sh)
- **DESPUÉS del reinicio** (sil-startup.sh)

### Shutdown (Antes):
```bash
/root/.openclaw/tools/sil-shutdown.sh
```
Guarda: Estado actual, tareas pendientes, reporte

### Startup (Después):
```bash
/root/.openclaw/tools/sil-startup.sh
```
Restaura: Contexto, memoria, tareas

---

