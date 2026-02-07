# CLAUDE CODE LOOP - Implementación para OpenClaw

## Resumen

**Objetivo:** Implementar un sistema de investigación autónoma inspirado en Claude Code Loop que aprovecha la arquitectura existente de OpenClaw.

**Pattern:** LEER → RESEARCH → VERIFICAR → DECIDIR → PERSISTIR → REPETIR

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│              CLAUDE CODE LOOP                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│   │  LEER  │ →  │RESEARCH │ →  │ VERIFY  │      │
│   │Context  │    │(Brave)  │    │Progress │      │
│   └─────────┘    └─────────┘    └────┬────┘      │
│          ↑                             │           │
│          │           ┌─────────────────┘           │
│          │           ↓                             │
│          │    ┌─────────┐                          │
│          │    │ DECIDE  │ → Exit?                  │
│          │    │ Continue│    → Help?              │
│          │    └────┬────┘                          │
│          │         ↓                               │
│          │    ┌─────────┐                          │
│          │    │PERSIST  │ → memory/YYYY-MM-DD.md   │
│          │    └────┬────┘                          │
│          │         ↓                               │
│          │    ┌─────────┐                          │
│          │    │ REPEAT  │ → LEER                    │
│          │    └─────────┘                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Componentes

### 1. HEARTBEAT.md ( ya existente )
Checklist que se ejecuta cada 30min. Ahora extendido con:
- Autonomous Research Loop
- Safety Guards
- Progress Tracking
- Exit Conditions

**Ubicación:** `/root/.openclaw/workspace/HEARTBEAT.md`

### 2. TASKS.md
Fuente de verdad para tasks de investigación autónoma.

**Formato:**
```markdown
### [ID-YYYY-MM-DD] Título

**Status:** pending | in_progress | blocked | done
**Priority:** high | medium | low
**Exit Conditions:**
- [ ] Condición 1
- [ ] Condición 2

**Research Queries:**
- [ ] query 1
- [ ] query 2

**Progress Log:**
- YYYY-MM-DD: Descripción del progreso
```

**Ubicación:** `/root/.openclaw/workspace/TASKS.md`

### 3. scripts/claude-code-loop.sh
Script de参考 (para documentación/development). No es necesario ejecutar - el loop ocurre via Heartbeat.

**Ubicación:** `/root/.openclaw/workspace/scripts/claude-code-loop.sh`

### 4. Memory Persistence
- `memory/YYYY-MM-DD.md` - Notas diarias
- `MEMORY.md` - Memorias a largo plazo

---

## Safety Guards

| Guard | Valor | Propósito |
|-------|-------|-----------|
| Max Retries | 3 | Previene loops infinitos |
| Max Queries | 3 por heartbeat | Rate limiting |
| Circuit Breaker | Archivo `.circuit_breaker` | Detiene execution si hay errores |
| Exit Conditions | Definidas por task | Evita scope creep |

---

## Cómo Usar

### 1. Crear una nueva Task

Editar `TASKS.md`:

```markdown
### RESEARCH-2026-02-06 Investigar alternativas a Notion

**Status:** pending
**Priority:** high
**Exit Conditions:**
- [ ] Encontrar 3 alternativas
- [ ] Comparar precios
- [ ] Guardar en memory/YYYY-MM-DD.md

**Research Queries:**
- [ ] "Notion alternatives 2026 open source"
- [ ] "alternative to Notion for personal knowledge management"
- [ ] "Obsidian vs Notion vs Coda comparison"
```

### 2. Heartbeat ejecuta automáticamente

Cada 30min, Heartbeat:
1. Lee HEARTBEAT.md → Lee TASKS.md
2. Ejecuta web_search para queries pendientes
3. Verifica progreso
4. Decide: continuar, pedir help, o terminar
5. Persiste resultados en memory/YYYY-MM-DD.md

### 3. Ver resultados

```bash
# Ver tasks pendientes
cat /root/.openclaw/workspace/TASKS.md

# Ver progreso de hoy
cat /root/.openclaw/workspace/memory/2026-02-06.md
```

---

## Fuentes de Inspiración

| Proyecto | Relevancia |
|----------|-----------|
| **Ralph-Claude-Code** | ⭐ Loop autónomo con exit detection |
| **Autonomous-Dev** | 8-Agent Pipeline (simplificado) |
| **Continuous-Claude** | Context persistence |
| **Claude-Flow** | Enterprise patterns |

---

## Diferencias con Claude Code

| Aspecto | Claude Code Original | Nuestra Implementación |
|---------|---------------------|----------------------|
| Ejecución | CLI contínua | Heartbeat (30min) |
| Contexto | En memoria | MEMORY.md + files |
| Safety | Ralph-built-in | Manual guards |
| Research | Antral API | Brave Search |

---

## Limitaciones

- No es un loop contínuo real (es batched via Heartbeat)
- No ejecuta código directamente (usa tools existentes)
- No hace PRs/commits automáticamente

---

## Próximos Pasos

1. [ ] Testear con primera task real
2. [ ] Refinar exit conditions
3. [ ] Añadir métricas de éxito
4. [ ] Iterar basado en feedback
