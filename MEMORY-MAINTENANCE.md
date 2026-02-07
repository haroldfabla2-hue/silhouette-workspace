# Memory Maintenance System - Sil v1.0

## Problema
La ventana de contexto de MiniMax-M2.1 es limitada. Sin consolidación, la memoria crece linealmente y degrada performance.

## Solución: Sistema de Memoria en Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORIA DE SIL                           │
├─────────────────────────────────────────────────────────────┤
│  CONTEXT (en sesión)                                        │
│  - Últimos 20 mensajes                                      │
│  - Task actual                                             │
│  - Estado del heartbeat                                    │
├─────────────────────────────────────────────────────────────┤
│  EPISÓDICO (daily logs)                                    │
│  - memory/YYYY-MM-DD.md                                     │
│  - Últimos 7 días (auto-prune después)                      │
├─────────────────────────────────────────────────────────────┤
│  SEMÁNTICO (consolidado)                                   │
│  - MEMORY.md                                               │
│  - Preferencias, metas, aprendizajes                        │
│  - No crece con frecuencia                                  │
├─────────────────────────────────────────────────────────────┤
│  PROCEDURAL (cómo hacer cosas)                              │
│  - SOUL.md, USER.md, AGENTS.md                             │
│  - Templates, workflows                                    │
└─────────────────────────────────────────────────────────────┘
```

## Operaciones Automáticas

### 1. Consolidación Diaria
Cada heartbeat, extraer aprendizajes de daily logs y mover a MEMORY.md.

```python
def consolidate_memory():
    # 1. Leer últimos daily logs
    recent_logs = read_logs(last_n_days=3)
    
    # 2. Extraer "insights" nuevos
    new_insights = []
    for log in recent_logs:
        insights = extract_insights(log)
        new_insights.extend(insights)
    
    # 3. Deduplicar vs MEMORY.md existente
    unique_insights = deduplicate(new_insights, MEMORY.md)
    
    # 4. Si hay insights nuevos, append a MEMORY.md
    if unique_insights:
        append_to_memory(unique_insights)
```

### 2. Pruning Automático
- Daily logs > 7 días: archivar o eliminar
- Context en sesión: mantener últimos 20 mensajes
- Verificar tamaño de MEMORY.md (si > 50KB, resumir)

### 3. Expectativas Dinámicas
```python
def update_expectations():
    # Trackear métricas
    metrics = {
        'research_sources_found': [],
        'email_response_rating': [],
        'calendar_reminder_usefulness': []
    }
    
    # Después de N samples, calcular promedio
    if len(metrics) >= 5:
        avg = sum(metrics) / len(metrics)
        
        # Ajustar expectativa si deviation > 20%
        if abs(avg - current_expectation) > 0.2 * current_expectation:
            new_expectation = avg * 0.9 + current_expectation * 0.1  # weighted
            log_expectation_change(current_expectation, new_expectation)
```

## Heartbeat Modificado (cada 30min)

```markdown
## HEARTBEAT.md - Con Memory Maintenance

### Checks (existente)
1. 📧 Emails
2. 📅 Calendar
3. 🌤️ Weather
4. 🔧 System

### NEW: Memory Maintenance (cada 10 heartbeats = 5 horas)

#### 5a. Consolidate Recent Learning
- [ ] Leer últimos 3 daily logs
- [ ] Extraer insights nuevos
- [ ] Append a MEMORY.md si son únicos

#### 5b. Update Expectations
- [ ] Calcular métricas de las últimas 5 interacciones
- [ ] Ajustar expectativas si deviation > 20%
- [ ] Loggear cambios en daily.md

#### 5c. Prune Old Context
- [ ] Archivar daily logs > 7 días
- [ ] Verificar tamaño MEMORY.md
- [ ] Resumir si > 50KB

#### 5d. Health Check
- [ ] Tasks completadas vs pendientes
- [ ] Success rate de últimos trabajos
- [ ] Identificar bloqueos
```

## Métricas a Trackear para Expectativas

| Métrica | Initial | Trackear | Ajuste |
|---------|---------|----------|--------|
| Research depth | 3 sources | Cada research | ±1 si deviation |
| Email summary | 3 bullets | Cada email check | ±1 si feedback |
| Reminder timing | 30 min | Cada reminder | ±10 min si ignored |
| Alert frequency | 5/min | Cada heartbeat | Reducir si "no molestar" |

## Formato de Insight para Consolidación

```markdown
## Aprendizajes Consolidados - YYYY-MM-DD

### Preferencias Descubiertas
- [timestamp] Alberto prefiere resúmenes de 3 bullets vs párrafos
- [timestamp] No le gusta ser interrumpido durante Deep Work

### Patrones de Uso
- [timestamp] Calendar reminders a 30min son ignorados
- [timestamp] Weather alerts solo efectivos si lluvia > 60%

### Decisiones Tomadas
- [timestamp] Usar Claude Code Loop pattern para autonomía
- [timestamp] HEARTBEAT.md como fuente de verdad
```

## Ventajas del Sistema

1. **MEMORY.md estable** - Crece lento, solo insights importantes
2. **Daily logs detallados** - Pero se prunean automáticamente
3. **Contexto sesiones** - Limpio, últimos mensajes
4. **Expectativas adaptativas** - Aprende sin intervención
5. **No depende de contexto** - Todo persisitido en archivos

## TODO: Implementación

- [ ] Modificar HEARTBEAT.md con memory maintenance
- [ ] Crear script `sil-memory-maintenance.py`
- [ ] Configurar heartbeat counter
- [ ] Probar con 1 semana de datos
