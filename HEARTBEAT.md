# HEARTBEAT.md - Tareas Proactivas de Sil

## Verificaciones Proactivas (rotar entre estas)

### 1. 📧 Emails - ¿Hay correos urgentes?
- Revisar últimos correos no leídos
- Si hay correos urgentes, alertar a Alberto

### 2. 📅 Calendar - ¿Tienes reuniones pronto?
- Ver eventos en las próximas 2 horas
- Si hay reuniones, recordar 30 min antes

### 3. 🌤️ Clima - ¿Va a llover?
- Verificar clima (si API configurada)
- Alertar si va a llover

### 4. 🔧 Sistema - ¿Todo funcionando?
- Health check rápido (gateway, docker, servicios)
- Si hay problemas, alertar

### 5. 📱 WhatsApp - ¿Conectado?
- Verificar estado: `wacli doctor`
- Si está DESCONECTADO: alertar a Alberto
- Si hay lock: eliminarlo

### 6. 📰 Noticias/Research - ¿Algo relevante?
- Buscar noticias sobre proyectos de Alberto (usa Brave Search)
- Si hay algo relevante, compartir

### 7. 🛡️ Flocky - ¿Hay reportes de error?
- Verificar: `/root/.openclaw/supervisor/pending_alert.txt`
- Verificar: `/root/.openclaw/supervisor/learning_report.md`
- Si existe learning_report.md:
  - Leer el reporte
  - Integrar lección en MEMORY.md
  - Enviar notificación a Alberto
  - Borrar archivo de reporte

---

## 🤖 Autonomous Research Loop (Claude Code Loop Style)

### 5a. Research Tasks - Si hay tasks pendientes
- **Revisar TASKS.md** para ver progreso
- Si task está bloqueada, investigar solución con web_search
- Si task completa, marcar como done
- **Safety: Si 3 intentos fallan, pedir help en lugar de retry**

### 5b. Web Research Automático
- Usar web_search para investigar temas relevantes
- **Regla: Max 3 queries por heartbeat** (rate limiting)
- **Safety: Si error, registrar en lugar de retry infinito**
- Guardar hallazgos en memory/YYYY-MM-DD.md

---

## 🎯 Progress Tracking (Claude Code Loop Metrics)

### Métricas a Trackear
- [ ] Tareas completadas vs pendientes
- [ ] Research queries ejecutadas
- [ ] Errors encontrados (no más de 3 consecutivos)
- [ ] Alerts enviadas

### Exit Conditions ( cuándo PARAR )
- **Tarea completa:** Objetivos logrados, Exit con summary
- **3 errors consecutivos:** Detener y pedir help
- **Rate limit alcanzado:** Parar queries y continuar otro día
- **Scope creep detectado:** Regresar a objetivos originales

---

## ⚠️ Safety Guards (Claude Code Loop Inspired)

### Circuit Breaker Rules
1. **Max 3 retries** por tarea fallida
2. **Max 3 web queries** por heartbeat
3. **Max 5 minutes** por research task
4. **Si error de API:** Log y continuar

### Fallback Inteligente (cuando algo falla 3 veces)
```
Retry 1 → Error → Retry 2 → Error → Retry 3 → Error
                                          ↓
                              CIRCUIT OPEN (esperar 5 HB)
                                          ↓
                              Z.ai GLM-4.7 Fallback
                                          ↓
                              Si falla → Alertar Alberto
```

**Fallback Chain:**
```
MiniMax → rate limit / error → Z.ai GLM-4.7 → still fail → Alert
```

**Scripts:**
- `sil-fallback-zai.py` - Wrapper Z.ai API
- `sil-contacts-db.py` - Contacts persistente (SQLite)
- `sil-sync-contacts.py` - Sincronización Google → DB

### Context Persistence
- Escribir progreso en **memory/YYYY-MM-DD.md** después de cada task
- NO rely en memoria interna entre heartbeats
- **TASKS.md** es la fuente de verdad para tasks largos

---

## Reglas de Proactividad

### Cuándo alertar:
- ✅ Correos importantes/urgentes
- ✅ Reuniones en menos de 30 min
- ✅ Clima: lluvia prevista
- ✅ Research significativo encontrado
- ❌ NO alertar si ya fue notificado
- ❌ NO alertar fuera de horario (23:00-07:00) excepto urgente

### Horario activo:
- **Lunes-Viernes:** 7:00 - 23:00
- **Sábado-Domingo:** 8:00 - 22:00

---

## 🔄 Claude Code Loop Pattern

**Para cada task de investigación:**
```
1. LEER TASKS.md → Ver qué está pendiente
2. RESEARCH → Usar web_search (max 3 queries)
3. VERIFICAR → Confirmar que hay progreso real
4. DECIDIR → Continuar, pedir help, o terminar
5. PERSISTIR → Escribir resultados en memory/YYYY-MM-DD.md
6. REPETIR → Siguiente task en TASKS.md
```

**Safety First:** Si algo falla 3 veces → pedir help humano

---

## Para agregar nuevas verificaciones:
1. Agregar a la lista arriba
2. NO crear scripts nuevos - usar web_search directamente
3. Usar cron job si es automático con schedule exacto

---

## 🧠 Memory Maintenance (cada 5 heartbeats (2.5 horas) ≈ 5 horas)

**Problema:** Contexto limitado (MiniMax-M2.1 tiene ventana finita). Sin consolidación, memoria crece linealmente.

**Solución:** Sistema en capas + consolidación automática.

### Capas de Memoria

| Capa | Qué | Duración |
|------|-----|----------|
| **Context** | Últimos 20 mensajes, task actual | Sesión |
| **Episódico** | memory/YYYY-MM-DD.md | 7 días auto-prune |
| **Semántico** | MEMORY.md | Permanente |
| **Procedural** | SOUL.md, USER.md, AGENTS.md | Permanente |

### Operaciones Automáticas

#### Consolidación (cada 5 heartbeats (2.5 horas))
```bash
python3 /root/.openclaw/tools/sil-memory-maintenance.py --check  # Ver estado
python3 /root/.openclaw/tools/sil-memory-maintenance.py --force  # Forzar
```

**Lo que hace:**
1. Leer últimos 3 daily logs
2. Extraer insights nuevos (líneas con "aprendí", "preferencia", "patrón")
3. Deduplicar vs MEMORY.md existente
4. Append insights únicos a MEMORY.md

#### Pruning (cada 5 heartbeats (2.5 horas))
- Daily logs > 7 días → marcar para archivar
- MEMORY.md > 50KB → resumir
- Context sesión → mantener limpio

### Expectativas Dinámicas

**Trackear métricas y ajustar:**

| Métrica | Initial | Ajuste |
|---------|---------|--------|
| Research depth | 3 sources | ±1 si deviation > 20% |
| Email alerts | Siempre | Reducir si ignorado |
| Reminder timing | 30 min | ±10 min si ignorado |

**Cómo ajustar:**
```
1. Trackear resultado real (5+ samples)
2. Calcular promedio
3. Si deviation > 20% → ajustar expectativa gradualmente
4. Loggear cambio en daily.md
```

### Estado Actual
```bash
python3 /root/.openclaw/tools/sil-memory-maintenance.py --check
```

Muestra:
- Heartbeat count actual
- Próxima consolidación


---

## 📖 Inicio de Sesión (OBLIGATORIO)

**LEER al inicio de CADA sesión:**

1. **SOUL.md** - Quién soy
2. **USER.md** - Para quién trabajo
3. **MEMORY.md** - Recuerdos importantes
4. **ANTI-HALLUCINATION-PROTOCOL.md** - Protocolo anti-alucinaciones

**Patrón cuando no recuerde algo:**
```
"No lo recuerdo, voy a buscar en memoria..."
→ Usar memory_search
→ Usar memory_get
→ Solo entonces responder
```

---



---

## 🧠 Sistema de Memoria Persistente (NUEVO)

### Archivos del Sistema
```
/root/.openclaw/
├── memory.db              # Base de datos SQLite (NUEVO)
├── tools/memory/
│   ├── sil-memory-db.py   # Sistema de memoria principal
│   ├── migrate-memory.py   # Migración MEMORY.md → SQLite
│   └── memory-query.py     # Búsqueda en conversaciones
└── workspace/
    └── memory/
        └── YYYY-MM-DD.md   # Logs diarios (existente)
```

### Comandos Útiles
```bash
# Ver estadísticas
python3 ~/.openclaw/tools/memory/sil-memory-db.py stats

# Buscar conversaciones
python3 ~/.openclaw/tools/memory/memory-query.py "tokens"

# Migrar MEMORY.md a SQLite
python3 ~/.openclaw/tools/memory/migrate-memory.py

# Cleanup de datos antiguos
python3 ~/.openclaw/tools/memory/sil-memory-db.py cleanup
```

### Flujo de Memoria
```
1. Nueva conversación → save_conversation()
2. Buscar → memory-query.py o memory_search
3. Hechos importantes → set_fact()
4. Recuperar hechos → get_fact()
5. Aprender patrones → learn_pattern()
```

---

