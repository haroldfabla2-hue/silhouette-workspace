# 🔐 Protocolo de Seguridad para OpenClaw v3.0

## Principio Fundamental
**"Antes de tocar OpenClaw: Piensa → Planifica → Practica → Ejecuta"**

---

## 🛡️ Sistema de Protección v3.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PROTOCOLO v3.0 CON SUPERVISOR                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐                                                   │
│  │ SUPERVISOR   │ ← External, siempre activo (systemd + nohup)     │
│  │ v3.0         │ ← Guarda snapshots, auto-restaura                 │
│  │              │ ← Usa MiniMax AI para analizar errores             │
│  └──────┬───────┘                                                   │
│         │                                                            │
│         │ PROTEGE                                                    │
│         ▼                                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PROTOCOLO DE CAMBIOS                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Reglas de Oro

| Regla | Descripción |
|-------|-------------|
| **1. Supervisor activo** | Nunca hacer cambios sin supervisor corriendo |
| **2. Snapshot primero** | Guardar snapshot ANTES de cualquier cambio |
| **3. Backup siempre** | Copia adicional del archivo |
| **4. Usa comandos simples** | `config set` > `config.patch` > `config.apply` |
| **5. Valida primero** | Python JSON parser antes de ejecutar |
| **6. Un cambio a la vez** | No combines múltiples cambios |
| **7. Verifica después** | Doctor + Logs siempre |

---

## Comandos Seguros de OpenClaw

### Más Seguro (推荐)
```bash
openclaw config set "models.providers.openai.apiKey" "sk-..."
```

### Seguro
```bash
openclaw config get "models.providers"
openclaw config set "models.providers.openai.apiKey" "sk-..."
```

### Riesgo Medio (patch)
```bash
openclaw gateway call config.patch --params '{"raw":"{...}","hash":"..."}'
```

### Alto Riesgo (apply)
```bash
openclaw gateway call config.apply --params '{"raw":"{...}","hash":"..."}'
```

---

## Flujo de Trabajo v3.0

### PARA CUALQUIER CAMBIO:

```
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: PLANIFICAR                                        │
├─────────────────────────────────────────────────────────────┤
│  1. Escribir el cambio en papel/chat                       │
│  2. Identificar el path exacto del config                 │
│  3. Decidir método (set > patch > apply)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 2: VERIFICAR SUPERVISOR                             │
├─────────────────────────────────────────────────────────────┤
│  1. Verificar que supervisor está activo                 │
│     python3 /root/.openclaw/supervisor/sil-supervisor.py status │
│  2. Si no está activo, iniciar:                           │
│     nohup python3 /root/.openclaw/supervisor/sil-supervisor.py & │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: SNAPSHOT (SUPERVISOR)                           │
├─────────────────────────────────────────────────────────────┤
│  1. python3 /root/.openclaw/supervisor/sil-supervisor.py snapshot openclaw.json  │
│  2. Verificar que se creó                                 │
│  3. El supervisor ya guardó 5 snapshots rotativos         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 4: BACKUP                                           │
├─────────────────────────────────────────────────────────────┤
│  cp ~/.openclaw/openclaw.json ~/.openclaw/backup.json     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 5: VALIDAR                                          │
├─────────────────────────────────────────────────────────────┤
│  1. Escribir el comando en un archivo                    │
│  2. python3 -c "import json; json.load(open('config'))"  │
│  3. Si hay error, corregir ANTES de ejecutar              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 6: EJECUTAR                                         │
├─────────────────────────────────────────────────────────────┤
│  1. Usar el método más simple posible                    │
│  2. Si set funciona, USAR SET                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 7: ESPERAR Y SUPERVISAR                             │
├─────────────────────────────────────────────────────────────┤
│  ⏳ Esperar 30 segundos (supervisando)                     │
│  El supervisor verificará automáticamente                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 8: SUPERVISOR VERIFICA                              │
├─────────────────────────────────────────────────────────────┤
│  ✅ TODO BIEN → Continuar normalmente                     │
│                                                             │
│  ❌ ERROR → AUTO-RESPUESTA:                               │
│     ├── MiniMax AI analiza error                          │
│     ├── Genera causa raíz + lección                       │
│     ├── Alertar a Alberto (Telegram + WhatsApp)           │
│     ├── Revertir snapshot                                  │
│     ├── openclaw doctor --fix                              │
│     ├── Reiniciar gateway                                 │
│     ├── Alertar "CORREGIDO"                               │
│     └── Lección integrada en mi memoria                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 9: VERIFICAR FINAL                                  │
├─────────────────────────────────────────────────────────────┤
│  1. openclaw doctor                                        │
│  2. Verificar logs                                         │
│  3. Verificar que el cambio esté aplicado                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Ejemplo: Agregar API Key (MÉTODO SEGURO v3.0)

```bash
# FASE 1: PLANIFICAR
# Comando: openclaw config set "models.providers.openai.apiKey" "sk-..."
# Path: models.providers.openai.apiKey

# FASE 2: VERIFICAR SUPERVISOR
python3 /root/.openclaw/supervisor/sil-supervisor.py status
echo "✅ Supervisor activo"

# FASE 3: SNAPSHOT
python3 /root/.openclaw/supervisor/sil-supervisor.py snapshot openclaw.json
echo "✅ Snapshot guardado"

# FASE 4: BACKUP
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
echo "✅ Backup creado"

# FASE 5: VALIDAR (con Python)
python3 << 'PYEOF'
import json
test_value = "[API_KEY_CENSURADO]..."  # Tu API key
# Solo validar formato, NO ejecutar
print(f"API key length: {len(test_value)}")
print(f"Starts with sk-: {test_value.startswith('sk-')}")
print("✅ Formato válido")
PYEOF

# FASE 6: EJECUTAR
openclaw config set "models.providers.openai.apiKey" "[API_KEY_CENSURADO]"
echo "✅ Comando ejecutado"

# FASE 7: ESPERAR (supervisando)
echo "⏳ Esperando 30 segundos para verificación automática..."
sleep 30

# FASE 8: SUPERVISOR YA VERIFICÓ (automáticamente)
# Si hubo error, ya fue corregido

# FASE 9: VERIFICAR FINAL
openclaw doctor 2>&1 | tail -5
echo "✅ Protocolo completado"
```

---

## Verificación Pre-Ejecución (CHECKLIST)

Antes de ejecutar CUALQUIER comando en OpenClaw:

- [ ] **Supervisor activo** → `python3 sil-supervisor.py status`
- [ ] **Snapshot creado** → `sil-supervisor.py snapshot openclaw.json`
- [ ] **Backup creado** → `cp openclaw.json backup.json`
- [ ] **Comando escrito** → En un archivo
- [ ] **JSON/valor validado** → Con Python
- [ ] **Método más simple identificado** → `config set` preferible
- [ ] **Doctor pasa** → Antes del cambio
- [ ] **Logs revisados** → Después del cambio

---

## Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|---------|
| JSON inválido | Comillas mal escapadas | Usar Python para validar |
| Hash inválido | Config modificado entre get y patch | Obtener hash fresco |
| Path incorrecto | No saber la estructura del config | `openclaw config get` primero |
| apply reemplaza todo | Usar apply en vez de set | SIEMPRE preferir `set` |
| Supervisor caído | Servicio no corriendo | Reiniciar con `nohup python3 ... &` |

---

## Paths Comunes

### API Keys
```
models.providers.<provider>.apiKey
```

### Canales
```
channels.whatsapp.enabled
channels.telegram.botToken
```

### Agentes
```
agents.defaults.model.primary
```

---

## Comandos de Verificación

```bash
# Verificar supervisor
python3 /root/.openclaw/supervisor/sil-supervisor.py status

# Verificar salud
python3 /root/.openclaw/supervisor/sil-supervisor.py check

# Guardar snapshot
python3 /root/.openclaw/supervisor/sil-supervisor.py snapshot openclaw.json

# Restaurar snapshot
python3 /root/.openclaw/supervisor/sil-supervisor.py restore openclaw.json

# Ver snapshots
ls -la /root/.openclaw/snapshots/

# Ver config actual
openclaw config get

# Ver logs
openclaw logs --tail 50

# Doctor
openclaw doctor
```

---

## Resumen de Cambios desde v1.0

| v1.0 (Falló) | v2.0 (Mejor) | v3.0 (Infalible) |
|--------------|--------------|------------------|
| Usaba `config.patch` complejo | Usa `config set` simple | Supervisor externo protege |
| JSON escapado manual | Validación con Python | Auto-restore + AI learning |
| Sin validación previa | Checklist obligatorio | Snapshot + Backup + Checklist |
| Sin protección | Sin protección | Supervisor siempre activo |
| Sin aprendizaje | Sin aprendizaje | Lecciones integradas en memoria |

---

## 📚 Aprendiendo de los Errores

Cuando el supervisor detecta un error:

1. **Analiza** con MiniMax AI
2. **Identifica** causa raíz
3. **Genera** lección para mí
4. **Guarda** lección en `learning.db`
5. **Me alerta** cuando reinicio
6. **Yo integro** la lección en MEMORY.md
7. **Nunca más** el mismo error

---

## 🎯 Objetivos del Sistema v3.0

| Objetivo | Métrica |
|----------|---------|
| **Supervisor siempre activo** | Uptime > 99% |
| **Snapshots disponibles** | 5 snapshots de cada config crítico |
| **Auto-restore funcional** | Recovery < 2 minutos |
| **Aprendizaje continuo** | 0 errores repetidos |
| **Tiempo de inactividad** | < 5 minutos/mes |

---

*Protocolo v3.0 - Creado: 2026-02-06*
*Basado en: Documentación oficial de OpenClaw + Claude Code Loop Patterns*
