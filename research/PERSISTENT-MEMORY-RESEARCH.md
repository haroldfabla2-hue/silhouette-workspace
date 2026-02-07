# 📋 Investigación: Sistema de Memoria Persistente para Sil

**Fecha:** 2026-02-05
**Investigador:** Sil (auto-investigación)
**Objetivo:** Sistema de memoria que nunca pierda contexto

---

## 🎯 Resumen Ejecutivo

### Lo que ya existe:
- `MEMORY.md` - Memoria semántica (texto plano, 20KB)
- `memory/YYYY-MM-DD.md` - Logs diarios
- `memory_search` - Herramienta de búsqueda
- Cron job de memory consolidation

### Lo que falta:
- Base de datos estructurada (SQLite)
- Tablas especializadas
- Búsqueda semántica real
- Tags y organización
- Persistencia cross-session completa

---

## 🔬 Investigación de opciones

### Opción 1: Claude-Flow Memory System (12 tablas SQLite)

**Fuente:** https://github.com/ruvnet/claude-flow/wiki/Memory-System

**Esquema de 12 tablas:**
```
.swarm/memory.db
├── memory_store (key-value con namespaces)
├── sessions (gestión cross-session)
├── agents (registro de agentes)
├── tasks (tracking de tareas)
├── agent_memory (memoria por agente)
├── shared_state (estado compartido)
├── events (log de eventos)
├── patterns (patrones aprendidos)
├── performance_metrics (métricas)
├── workflow_state (persistencia de workflows)
├── swarm_topology (topología de red)
└── consensus_state (consenso distribuido)
```

**Ventajas:**
- ✅ SQLite (ya tenemos Python/sqlite3)
- ✅ 12 tablas especializadas
- ✅ ACID compliant
- ✅ Escalable (millones de registros)
- ✅ WAL mode para concurrencia

**Desventajas:**
- ❌ Complex overkill para un solo agente
- ❌ Diseñado para swarms multi-agente

---

### Opción 2: SQLite + MEMORY.md híbrido

**Inspirado en:** claude-mem (thedotmack/claude-mem)

**Arquitectura:**
```
~/.openclaw/
├── memory.db (SQLite estructurado)
│   ├── conversations (transcripts)
│   ├── facts (hechos curados)
│   ├── tags (etiquetas)
│   └── metadata (fechas, sesiones)
├── memory/
│   └── YYYY-MM-DD.md (logs diarios)
└── MEMORY.md (memoria semántica, backup)
```

**Ventajas:**
- ✅ Integra con lo que ya existe
- ✅ Backup en texto plano (MEMORY.md)
- ✅ Búsqueda estructurada + semántica
- ✅ Simple de implementar
- ✅ Sin dependencias externas

---

### Opción 3: ChromaDB/Weaviate (Vector Database)

**Ventajas:**
- ✅ Búsqueda semántica real con embeddings
- ✅ Popular en ecosistemas AI

**Desventajas:**
- ❌ Dependencia externa
- ❌ Overkill para nuestro caso
- ❌ Más complejo de mantener

---

## 🎓 Recomendación: Opción 2 (Híbrido SQLite + MEMORY.md)

**Razón:** Integra con lo que ya existe, más simple, sin dependencias.

---

## 📐 Diseño del Sistema Propuesto

### Estructura de la base de datos

```sql
-- Tabla principal: conversaciones
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    channel TEXT, -- telegram, whatsapp, etc.
    user TEXT,
    message TEXT,
    response TEXT,
    tags TEXT, -- JSON array de tags
    metadata TEXT, -- JSON para datos adicionales
    embedding BLOB -- futuro: para búsqueda semántica
);

-- Tabla: hechos curados (de MEMORY.md)
CREATE TABLE curated_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    category TEXT, -- user, system, project, preference
    source TEXT, -- de dónde vino
    confidence REAL DEFAULT 1.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME
);

-- Tabla: tags
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT,
    usage_count INTEGER DEFAULT 0,
    last_used DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: sesiones
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    start_time DATETIME,
    end_time DATETIME,
    channel TEXT,
    model TEXT,
    context_summary TEXT,
    FOREIGN KEY(id) REFERENCES conversations(session_key)
);

-- Tabla: patrones aprendidos
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger TEXT NOT NULL,
    behavior TEXT NOT NULL,
    success_rate REAL DEFAULT 0.0,
    usage_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used DATETIME
);
```

### Flujo de datos

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT                                │
│  (mensajes, commands, archivos)                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              CONVERSATION MANAGER                        │
│  1. Guardar conversación completa                        │
│  2. Extraer tags                                        │
│  3. Identificar hechos nuevos                           │
│  4. Actualizar patrones                                  │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌───────────────────┐   ┌───────────────────┐
│   SQLite DB       │   │   MEMORY.md       │
│ (búsqueda rápida) │   │ (backup semántico)│
│ • conversations   │   │ • hechos curados  │
│ • facts           │   │ • preferencias    │
│ • tags            │   │ • contexto        │
└───────────────────┘   └───────────────────┘
```

### APIs del sistema

```python
class MemorySystem:
    async def save_conversation(session_key, message, response, tags=None)
    async def search_conversations(query, tags=None, limit=10)
    async def get_fact(key)
    async def set_fact(key, value, category="general")
    async def get_session_context(session_key)
    async def learn_pattern(trigger, behavior, success)
    async def consolidate_from_memory()  # De MEMORY.md a SQLite
    async def export_to_memory()  # De SQLite a MEMORY.md
```

---

## 🔗 Integración con OpenClaw

### Archivos existentes a integrar:
| Archivo | Rol | Acción |
|---------|-----|--------|
| `MEMORY.md` | Memoria semántica | Mantener, usar como backup |
| `memory/YYYY-MM-DD.md` | Logs diarios | Mantener, indexar en SQLite |
| `sessions_list` | Lista de sesiones | Integrar con tabla sessions |
| `memory_search` | Búsqueda existente | Mejorar con SQLite |

### Cron jobs a agregar:
```
• Auto-consolidation: SQLite ↔ MEMORY.md (cada 4h)
• Cleanup: Eliminar conversaciones antiguas (>30 días)
• Backup: Exportar a JSON (diario)
```

---

## 📋 Plan de implementación

### Fase 1: Base (Día 1)
- [ ] Crear SQLite database schema
- [ ] Implementar clase MemorySystem
- [ ] Integrar conversaciones existentes
- [ ] Script de migración MEMORY.md → SQLite

### Fase 2: Búsqueda (Día 2)
- [ ] Implementar búsqueda por tags
- [ ] Búsqueda por fecha
- [ ] Búsqueda por sesión

### Fase 3: Patrones (Día 3)
- [ ] Tracking de patrones
- [ ] Métricas de éxito
- [ ] Sugerencias basadas en patrones

### Fase 4: Integración (Día 4)
- [ ] Integrar con OpenClaw tools
- [ ] Auto-cargar contexto al inicio
- [ ] Actualizar memory_search

---

## 🔧 Requerimientos

### Dependencies
```json
{
  "python": ">=3.10",
  "sqlite3": "built-in",
  "json": "built-in"
}
```

### Sin dependencias externas (para simplificar)

---

## 📖 Referencias

1. Claude-Flow Memory System: https://github.com/ruvnet/claude-flow/wiki/Memory-System
2. Claude-Mem (triple redundancy): https://deepwiki.com/thedotmack/claude-mem/1-overview
3. Memory MCP Server: https://www.pulsemcp.com/servers/whenmoon-memory

---

*Investigación completada: 2026-02-05*
*Próximo paso: Implementar Fase 1*
