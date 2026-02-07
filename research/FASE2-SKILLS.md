# 📋 FASE 2: Exploración y Mejora de Skills
**Fecha:** 2026-02-05
**Versión:** 2.0 (Con Proactividad)

---

## 🎯 Principio de Proactividad

|Reactivo| Proactivo|
|---------|----------|
| Esperar pedidos | Anticipar necesidades |
| Responder preguntas | Ofrecer insights |
| Corregir errores | Prevenir errores |

### De investigación (McKinsey 2025):
> "AI agents don’t just respond — they proactively detect common issues, anticipate likely needs, and initiate resolution steps automatically"

---

## 📚 Referencias de Investigación

| Fuente | Concepto |
|--------|----------|
| McKinsey | Detectar proactivamente patrones, anticipar necesidades |
| Microsoft Copilot | Sugerir, automatizar, proporcionar insights |
| Salesforce Agentforce | Soporte autónomo y siempre activo |

---

## 📊 Resumen de Skills (11 Total)

| Skill | Descripción | Potencial | Prioridad |
|-------|-------------|-----------|-----------|
| **weather** | Clima sin API key (wttr.in, Open-Meteo) | Alertas proactivas | 🔴 ALTA |
| **google-workspace** | Gmail, Calendar, Drive, etc. | Automatización completa | 🔴 ALTA |
| **github** | GitHub CLI (issues, PRs, runs) | Auto-commit, CI monitoring | 🟡 MEDIA |
| **notion** | Notion API (pages, databases) | Automatización de docs | 🟡 MEDIA |
| **healthcheck** | Track water and sleep | Métricas personales | 🟡 MEDIA |
| **bird** | Twitter/X CLI | Auto-tweets | 🟢 BAJA |
| **gemini** | Gemini CLI para Q&A | Responder preguntas | 🟢 BAJA |
| **tmux** | Control tmux sessions | Automatización terminal | 🟢 BAJA |
| **wacli** | WhatsApp CLI | PAUSADO por Alberto | ⚫ PAUSADO |
| **sil-stt** | Speech-to-Text local | Transcripción audio | ⚫ CONFIGURADO |
| **skill-creator** | Crear nuevas skills | Solo si es necesario | ⚫ EMERGENCIA |

---

## 🌤️ WEATHER (ALTA PRIORIDAD)

### Lo que puede hacer:
```bash
# Clima actual
curl -s "wttr.in/Arequipa?format=3"
# Output: Arequipa: 🌤️ +22°C

# Pronóstico completo
curl -s "wttr.in/Arequipa?T"

# Open-Meteo (JSON, programático)
curl -s "https://api.open-meteo.com/v1/forecast?latitude=-16.4&longitude=-71.5&current_weather=true"
```

### Automatizaciones posibles:
1. **Alerta de lluvia** → Si probability > 40% → Notificar
2. **Resumen diario** → 7 AM con pronóstico del día
3. **Alerta de temperatura** → Si >35°C o <10°C → Notificar

### Script propuesto: `sil-weather-alert.sh`
```bash
#!/bin/bash
# Alerta de clima para Arequipa

LOCATION="Arequipa"
THRESHOLD_RAIN=40  # %
TEMP_HOT=35
TEMP_COLD=10

# Obtener datos
DATA=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=-16.4&longitude=-71.5&current_weather=true")

# Extraer temp y weather code
TEMP=$(echo $DATA | jq '.current_weather.temperature')
WEATHER_CODE=$(echo $DATA | jq '.current_weather.weathercode')

# Lógica de alertas
if [ $TEMP -gt $TEMP_HOT ]; then
    echo "🔥 CALOR EXTREMO: ${TEMP}°C"
fi

if [ $TEMP -lt $TEMP_COLD ]; then
    echo "🥶 FRÍO EXTREMO: ${TEMP}°C"
fi

# Weather code 51-67 = lluvia
if [ $WEATHER_CODE -ge 51 ] && [ $WEATHER_CODE -le 67 ]; then
    echo "🌧️ POSIBLE LLUVIA - Lleva paraguas"
fi
```

---

## 📧 GOOGLE-WORKSPACE (ALTA PRIORIDAD)

### Lo que puede hacer (gogcli):
```bash
# Gmail
gog gmail search 'newer_than:7d' --max 10
gog gmail send --to email --subject "Hi" --body "Hello"

# Calendar
gog calendar events --today
gog calendar events --from 2026-02-05 --to 2026-02-06

# Drive
gog drive search "filename" --max 10

# Contacts
gog contacts list --max 20
```

### Automatizaciones posibles:
1. **Resumen diario** → 8 AM: correos no leídos + eventos del día
2. **Crear evento** → Desde comando
3. **Buscar archivo** → En Drive por nombre

### Script propuesto: `sil-gog-daily.sh`
```bash
#!/bin/bash
# Resumen diario de Google Workspace

echo "📧 CORREOS (últimas 24h):"
gog gmail search 'newer_than:1d' --max 5

echo ""
echo "📅 EVENTOS DE HOY:"
gog calendar events --today

echo ""
echo "📁 ARCHIVOS RECIENTES:"
gog drive search "has:star" --max 3
```

---

## 🐙 GITHUB (MEDIA PRIORIDAD)

### Lo que puede hacer:
```bash
# PRs
gh pr checks 55 --repo owner/repo
gh pr list --repo owner/repo --json number,title,state

# Workflows
gh run list --repo owner/repo --limit 10
gh run view <run-id> --repo owner/repo --log-failed

# API avanzada
gh api repos/owner/repo/pulls/55 --jq '.title, .state'
```

### Automatizaciones posibles:
1. **Auto-commit diario** → Commit de progreso
2. **Notificación de CI fallido** → Si workflow falla → Notificar
3. **Resumen de PRs** → PRs pendientes de review

### Script propuesto: `sil-github-daily.sh`
```bash
#!/bin/bash
# Resumen diario de GitHub

REPO="${1:-haroldfabla2-hue/Silhouette}"

echo "🐙 GITHUB DAILY - $REPO"
echo "="50

echo ""
echo "📋 PRs pendientes:"
gh pr list --repo $REPO --state OPEN --json number,title --jq '.[] | "\(.number): \(.title)"'

echo ""
echo "⚠️ Workflows fallidos:"
gh run list --repo $REPO --limit 5 --json status,name,conclusion --jq '.[] | select(.conclusion == "failure") | "\(.name): \(.conclusion)"'

echo ""
echo "✅ Últimos commits:"
gh api repos/$REPO/commits --jq '.[0:3] | .[] | "\(.sha[0:7]): \(.commit.message | split("\n") |.[0])"'
```

---

## 📝 NOTION (MEDIA PRIORIDAD)

### Lo que puede hacer:
```bash
# Buscar páginas
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -d '{"query": "Brandistry"}'

# Crear página
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -d '{"parent": {"database_id": "xxx"}, "properties": {...}}'

# Actualizar propiedades
curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

### Automatizaciones posibles:
1. **Crear página de daily** → Desde script
2. **Actualizar estado de tareas** → Cuando se completan
3. **Sincronizar con Drive** → Exportar a Notion

### Script propuesto: `sil-notion-daily.sh`
```bash
#!/bin/bash
# Crear página de daily log en Notion

NOTION_KEY=$(cat ~/.config/notion/api_key)
DATABASE_ID="xxx"  # ID de la base de datos de daily logs

DATE=$(date +%Y-%m-%d)

# Crear página
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"database_id\": \"$DATABASE_ID\"},
    \"properties\": {
      \"Name\": {\"title\": [{\"text\": {\"content\": \"Daily $DATE\"}}]},
      \"Date\": {\"date\": {\"start\": \"$DATE\"}},
      \"Status\": {\"select\": {\"name\": \"Pendiente\"}}
    }
  }"

echo "✅ Página creada: $DATE"
```

---

## 🏃 HEALTHCHECK (MEDIA PRIORIDAD)

### Lo que puede hacer:
```bash
# Tracking de agua y sueño
healthcheck drink 500ml
healthcheck sleep 7h
healthcheck status
```

### Automatizaciones posibles:
1. **Recordatorio de agua** → Cada 2 horas
2. **Resumen semanal** → Métricas de la semana
3. **Integración con métricas de Alberto** → Tracking personal

### Script propuesto: `sil-health-summary.sh`
```bash
#!/bin/bash
# Resumen semanal de salud

echo "🏃 RESUMEN DE SALUD"
echo "=================="

echo ""
echo "💧 Agua (últimos 7 días):"
for day in {1..7}; do
    DATE=$(date -d "-${day}days" +%Y-%m-%d)
    echo "$DATE: $(healthcheck status --date $DATE | grep ml)"
done

echo ""
echo "😴 Sueño (últimos 7 días):"
for day in {1..7}; do
    DATE=$(date -d "-${day}days" +%Y-%m-%d)
    echo "$DATE: $(healthcheck status --date $DATE | grep h)"
done

echo ""
echo "📊 Progreso semanal:"
echo "   Agua total: $(healthcheck weekly --water)ml"
echo "   Sueño promedio: $(healthcheck weekly --sleep)h"
```

---

## 📋 PLAN DE IMPLEMENTACIÓN

### Scripts Implementados (5/5) ✅

| Script | Función | Tamaño |
|--------|---------|--------|
| sil-weather-alert.sh | Alertas de clima (lluvia, calor, frío) | 4KB |
| sil-gog-daily.sh | Resumen Gmail+Calendar+Drive | 3.7KB |
| sil-github-daily.sh | Resumen PRs, commits, CI | 2.7KB |
| sil-notion-daily.sh | Daily logs en Notion | 2.8KB |
| sil-health-summary.sh | Resumen semanal de salud | 2.3KB |

### Uso:

```bash
# Alertas de clima (7 AM)
./sil-weather-alert.sh

# Resumen Google Workspace (8 AM)
./sil-gog-daily.sh

# Resumen GitHub (8:30 AM)
./sil-github-daily.sh [repo]

# Daily log en Notion (8 PM)
./sil-notion-daily.sh

# Resumen de salud (9 PM, domingo)
./sil-health-summary.sh
```

### Integración con Cron:

```bash
# Weather Alert
openclaw cron add --name "Weather Alert" --cron "0 7 * * *" --session isolated --message "./sil-weather-alert.sh"

# Daily Summary
openclaw cron add --name "Daily Summary" --cron "0 8 * * *" --session isolated --message "./sil-gog-daily.sh && ./sil-github-daily.sh"
```

---

## ✅ ESTADO FINAL DE FASE 2

**Progreso:** 100% COMPLETADO

| Fase | Estado | Progreso |
|------|--------|----------|
| FASE 0 (Verificar) | ✅ | 100% |
| FASE 1 (Integraciones) | ✅ | 100% |
| FASE 2 (Skills) | ✅ | 100% |
| FASE 3 (Proactividad) | ⏳ | En progreso |

---

*Documento actualizado: 2026-02-05*
