# 🔐 Protocolo de Seguridad para OpenClaw

## Regla de Oro
**"Backup primero, verificar después"**

---

## Pasos para Cualquier Cambio en OpenClaw

### 1️⃣ BACKUP
```bash
# Copiar config actual
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)

# O para workspace completo:
cp -r ~/.openclaw/workspace ~/.openclaw/workspace.bak.$(date +%Y%m%d-%H%M%S)
```

### 2️⃣ OBTENER CONFIG ACTUAL
```bash
# Verificar estado antes de cambios
openclaw doctor

# Obtener hash del config actual
openclaw gateway call config.get --params '{}'
```

### 3️⃣ APLICAR CAMBIO (Mínimo)
```bash
# Usar config.patch para cambios parciales (NUNCA apply completo)
openclaw gateway call config.patch --params '{
  "raw": "{...solo lo que cambias...}",
  "baseHash": "<hash-del-get>",
  "restartDelayMs": 5000
}'
```

### 4️⃣ VERIFICAR
```bash
# Verificar que funciona
openclaw doctor

# Ver logs por errores
openclaw logs --tail 50
```

### 5️⃣ REVERTIR SI FALLA
```bash
# Restaurar backup
cp ~/.openclaw/openclaw.json.bak.* ~/.openclaw/openclaw.json

# Reiniciar
openclaw gateway restart
```

---

## Tipos de Cambios y Riesgos

| Cambio | Riesgo | Método Seguro |
|--------|--------|--------------|
| Agregar API key | Bajo | config.patch |
| Modificar config | Medio | config.patch + backup |
| Cambiar agentes | Alto | Backup completo + probar |
| Actualizar OpenClaw | Alto | Backup completo + rollback plan |

---

## Para APIs y Credenciales

### Método Preferido
1. Agregar al `.env` (si el script lo lee de ahí)
2. Solo modificar OpenClaw si es necesario

### Si Modificar OpenClaw
```bash
# Obtener config actual
openclaw gateway call config.get --params '{}' > /tmp/config-actual.json

# Editar solo el campo necesario
# Ejemplo agregar OpenAI:
{
  "models": {
    "providers": {
      "openai": {
        "apiKey": "sk-..."  // Solo esto
      }
    }
  }
}

# Aplicar patch
openclaw gateway call config.patch --params '{
  "raw": "{\"models\":{\"providers\":{\"openai\":{\"apiKey\":\"sk-...\"}}}}",
  "baseHash": "<hash>",
  "restartDelayMs": 5000
}'
```

---

## Lista de Verificación Pre-Cambio

- [ ] Backup creado
- [ ] Doctor ejecuta sin errores
- [ ] Hash capturado
- [ ] Cambio mínimo necesario
- [ ] Restart延迟 (5 segundos)
- [ ] Verificar post-cambio
- [ ] Logs revisados

---

## Logs y Auditoría

Todos los cambios se registran en:
- `/var/log/openclaw/`
- Backup files en `~/.openclaw/*.bak.*`

---

## Ejemplo Completo: Agregar OpenAI API

```bash
# 1. Backup
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
echo "✅ Backup creado"

# 2. Verificar estado
openclaw doctor
echo "✅ Doctor Passed"

# 3. Obtener hash
HASH=$(openclaw gateway call config.get --params '{}' | grep -o '"hash":"[^"]*"' | cut -d'"' -f4)
echo "Hash: $HASH"

# 4. Aplicar cambio
openclaw gateway call config.patch --params "{
  \"raw\": \"{\\\\\"models\\\\\":{\\\\\"providers\\\\\":{\\\\\"openai\\\\\":{\\\\\"apiKey\\\\\":\\\\\"sk-...\\\\\"}}}}\",
  \"baseHash\": \"$HASH\",
  \"restartDelayMs\": 5000
}"

# 5. Verificar
sleep 6
openclaw doctor
echo "✅ Verificado"
```

---

*Protocolo creado: 2026-02-06*
