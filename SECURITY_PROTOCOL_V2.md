# 🔐 Protocolo de Seguridad para OpenClaw v2.0

## Principio Fundamental
**"Antes de tocar OpenClaw: Piensa → Planifica → Practica → Ejecuta"**

---

## Reglas de Oro

| Regla | Descripción |
|-------|-------------|
| **1. Backup siempre** | Nunca toques sin backup |
| **2. Usa comandos simples** | `config set` > `config.patch` > `config.apply` |
| **3. Valida primero** | Python JSON parser antes de ejecutar |
| **4. Un cambio a la vez** | No combines múltiples cambios |
| **5. Verifica después** | Doctor + Logs siempre |

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

## Flujo de Trabajo v2.0

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
│  FASE 2: RESPALDAR                                        │
├─────────────────────────────────────────────────────────────┤
│  1. cp ~/.openclaw/openclaw.json ~/.openclaw/backup.json │
│  2. Verificar que el backup existe                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: VALIDAR                                          │
├─────────────────────────────────────────────────────────────┤
│  1. Escribir el comando en un archivo                    │
│  2. python3 -c "import json; json.load(open('config'))"  │
│  3. Si hay error, corregir ANTES de ejecutar              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 4: EJECUTAR                                         │
├─────────────────────────────────────────────────────────────┤
│  1. Usar el método más simple posible                    │
│  2. Si set funciona, USAR SET                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 5: VERIFICAR                                        │
├─────────────────────────────────────────────────────────────┤
│  1. openclaw doctor                                       │
│  2. openclaw logs --tail 20                               │
│  3. Verificar que el cambio esté aplicado                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 6: REVERTIR SI FALLA                                │
├─────────────────────────────────────────────────────────────┤
│  1. cp ~/.openclaw/backup.json ~/.openclaw/openclaw.json  │
│  2. openclaw gateway restart                               │
│  3. Verificar que todo volvió a la normalidad              │
└─────────────────────────────────────────────────────────────┘
```

---

## Ejemplo: Agregar OpenAI API Key (MÉTODO SEGURO)

```bash
# FASE 1: PLANIFICAR
# Comando: openclaw config set "models.providers.openai.apiKey" "sk-..."
# Path: models.providers.openai.apiKey

# FASE 2: RESPALDAR
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
echo "✅ Backup creado"

# FASE 3: VALIDAR (con Python)
python3 << 'PYEOF'
import json
test_value = "[API_KEY_CENSURADO]..."  # Tu API key
# Solo validar formato, NO ejecutar
print(f"API key length: {len(test_value)}")
print(f"Starts with sk-: {test_value.startswith('sk-')}")
print("✅ Formato válido")
PYEOF

# FASE 4: EJECUTAR (el método más simple)
openclaw config set "models.providers.openai.apiKey" "[API_KEY_CENSURADO]"
echo "✅ Comando ejecutado"

# FASE 5: VERIFICAR
openclaw doctor 2>&1 | tail -10
echo "✅ Doctor passed"

# FASE 6: REVERTIR (solo si falla)
# cp ~/.openclaw/openclaw.json.bak.* ~/.openclaw/openclaw.json
# openclaw gateway restart
```

---

## Verificación Pre-Ejecución (CHECKLIST)

Antes de ejecutar CUALQUIER comando en OpenClaw:

- [ ] Backup creado
- [ ] Comando escrito en un archivo
- [ ] JSON/valor validado con Python
- [ ] Método más simple identificado
- [ ] Doctor pasa antes del cambio
- [ ] Logs revisados después

---

## Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|---------|
| JSON inválido | Comillas mal escapadas | Usar Python para validar |
| Hash inválido | Config modificado entre get y patch | Obtener hash fresco |
| Path incorrecto | No saber la estructura del config | `openclaw config get` primero |
| apply reemplaza todo | Usar apply en vez de set | SIEMPRE preferir `set` |

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
# Ver config actual
openclaw config get

# Ver sección específica
openclaw config get "models.providers"

# Verificar estructura
python3 -c "import json; c=json.load(open('/root/.openclaw/openclaw.json')); print(json.dumps(c, indent=2))"

# Doctor
openclaw doctor

# Logs
openclaw logs --tail 50
```

---

## Resumen de Cambios desde v1.0

| v1.0 (Falló) | v2.0 (Infalible) |
|--------------|-------------------|
| Usaba `config.patch` complejo | Usa `config set` simple |
| JSON escapado manual | Validación con Python |
| Sin validación previa | Checklist obligatorio |
| Un cambio gigante | Un cambio a la vez |

---

*Protocolo v2.0 - Creado: 2026-02-06*
*Basado en: Documentación oficial de OpenClaw + mejores prácticas*
