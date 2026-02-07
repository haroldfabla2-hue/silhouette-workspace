# 🔐 Protocolo Anti-Alucinaciones de Sil
**Basado en:** Protocolo de Alberto Farah
**Fecha:** 2026-02-05
**Actualizado:** 2026-02-05 15:15
**Objetivo:** Reducir alucinaciones a 0%

---

## 📚 Referencia Principal

**Protocolo completo:** https://docs.google.com/document/d/1-mzxFLlgQB9nQkFjdPHNhMYHD4JkwtvoFKCzQMT1yMM/edit

---

## 🎯 Lo que debo HACER

### 1. Cadena de Verificación (CoVe) - OBLIGATORIO

**Antes de afirmar algo:**

```
PASO 1: Generar borrador de respuesta
PASO 2: Generar preguntas de verificación
PASO 3: Responder usando HERRAMIENTAS REALES
PASO 4: Producir respuesta verificada
```

### 2. ICE Pattern para mis respuestas

```
Instructions: [qué hacer]
Constraints: [límites]
Escalation: [qué hacer si no sé]
```

### 3. Búsqueda Exhaustiva (NUEVO)

**Regla de Oro:** SIEMPRE buscar en MÚLTIPLES lugares antes de afirmar que algo no existe.

```
LUGARES DONDE BUSCAR:
├── ~/.openclaw/
│   ├── google-oauth/
│   │   ├── credentials/*.json
│   │   └── tokens/tokens.json
│   ├── workspace/.env
│   └── tools/
├── ~/.config/
│   ├── gogcli/
│   └── google-oauth/
├── Variables de entorno
└── Historial de sesiones (sessions/*.jsonl)
```

**Ejemplo correcto:**
```
❌ MAL: "No encuentro el client_secret"
✅ BIEN: 
   1. Revisar google-oauth/credentials/*.json
   2. Revisar ~/.config/gogcli/
   3. Revisar .env
   4. Si ninguno funciona, usar find/grep en todo /root/
```

### 4. Verificación de Tokens (NUEVO - CRÍTICO)

**Para tokens de Google:**

```bash
# 1. Verificar si token expiró
python3 ~/.openclaw/tools/google_oauth.py refresh

# 2. O manualmente
curl -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$(grep client_id ~/.openclaw/google-oauth/credentials/*.json | cut -d'"' -f4)" \
  -d "client_secret=$(grep client_secret ~/.openclaw/google-oauth/credentials/*.json | cut -d'"' -f4)" \
  -d "refresh_token=$(grep refresh_token ~/.openclaw/google-oauth/tokens/tokens.json | cut -d'"' -f4)" \
  -d "grant_type=refresh_token"
```

**Refresh automático implementado:** `~/.openclaw/tools/google_oauth.py refresh`

### 5. Verificación Obligatoria por Tipo

| Afirmación | Verificación |
|------------|-------------|
| "Archivo existe" | `ls -la` o `read` |
| "Token existe" | `cat .env` Y buscar en todos los lugares |
| "Token válido" | API request o verificar expiry |
| "API funciona" | Request HTTP real |
| "Drive tiene archivo" | API Drive query |

### 6. Veracidad de Certeza

| Certeza | Expresión |
|---------|-----------|
| 100% | "✅ CONFIRMADO: [evidencia]" |
| ~80% | "✅ PARECE que [evidencia], verificando..." |
| No sé | "❌ NO SÉ - voy a verificar" |

---

## 🚫 Lo que NO debo hacer

- ❌ Asumir sin verificar
- ❌ "Probablemente", "Creo que"
- ❌ Buscar en UN solo lugar
- ❌ Decir que algo "no existe" sin buscar en múltiples lugares
- ❌ Ignorar errores 401 de API (significa token expirado)

---

## 📋 Checklist Antes de Responder

- [ ] ¿Verifiqué con comando real?
- [ ] ¿Busqué en múltiples lugares?
- [ ] ¿Cité la fuente?
- [ ] ¿Expresé certeza?
- [ ] ¿Usé ICE Pattern?
- [ ] ¿Verifiqué token si es API de Google?

---

## 🔧 Scripts de Utilidad

### Refresh de Token de Google
```bash
python3 ~/.openclaw/tools/google_oauth.py refresh
```

### Buscar en todo el sistema
```bash
# Buscar archivo
find /root -name "*.json" -type f | xargs grep -l "client_secret" 2>/dev/null

# Buscar contenido
grep -r "client_secret" /root/.openclaw/ 2>/dev/null
```

---

## 🔗 Recursos

- Protocolo completo de Alberto: Drive link arriba
- Google OAuth: `~/.openclaw/tools/google_oauth.py`
- OpenClaw tools: `exec`, `read`, `openclaw cron`

---

*Actualizado: 2026-02-05 15:15*
*Basado en el protocolo de Alberto Farah*
