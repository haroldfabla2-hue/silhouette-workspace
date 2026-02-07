# 🛡️ Sil Supervisor v3.0

Sistema de supervisión externo, robusto e inteligente para OpenClaw.

## Arquitectura

```
┌─────────────────────────────────────────────────┐
│           SUPERVISOR v3.0 (Systemd Service)      │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐    ┌──────────────┐           │
│  │   SNAPSHOTS  │    │   HEALTH     │           │
│  │   Manager   │    │   Monitor    │           │
│  └──────┬──────┘    └──────┬──────┘           │
│         │                   │                   │
│         └─────────┬───────────┘                   │
│                   ▼                             │
│         ┌─────────────────┐                     │
│         │     AI BRAIN   │  MiniMax           │
│         │   (Opcional)   │                     │
│         └────────┬────────┘                     │
│                  │                               │
│    ┌────────────┴────────────┐                  │
│    ▼                         ▼                  │
│  AUTO-RESTORE          LEARNING                │
│                                                    │
└─────────────────────────────────────────────────┘
```

## Características

- ✅ **Externo**: Corre como servicio systemd, independiente de Sil
- ✅ **Robusto**: Si Sil se rompe, el supervisor la puede reparar
- ✅ **Inteligente**: Usa IA (MiniMax) para analizar errores
- ✅ **Snapshots**: Guarda los últimos 5 snapshots
- ✅ **Auto-Restauración**: Reverte a snapshot funcional si algo falla
- ✅ **Alertas**: Notifica por Telegram y WhatsApp
- ✅ **Aprendizaje**: Genera lecciones para que Sil nunca más falle igual

## Archivos

| Archivo | Propósito |
|---------|----------|
| `sil-supervisor.py` | Script principal del supervisor |
| `sil-supervisor.service` | Servicio systemd |
| `/root/.openclaw/snapshots/` | Snapshots de configs |
| `/root/.openclaw/logs/supervisor.log` | Logs del supervisor |

## Instalación

```bash
# 1. Instalar servicio
cp /root/.openclaw/supervisor/sil-supervisor.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable sil-supervisor.service
systemctl --user start sil-supervisor.service

# 2. Verificar estado
systemctl --user status sil-supervisor.service

# 3. Ver logs
journalctl --user -u sil-supervisor.service -f
```

## Uso

```bash
# Verificar salud
python3 /root/.openclaw/supervisor/sil-supervisor.py check

# Estado del supervisor
python3 /root/.openclaw/supervisor/sil-supervisor.py status

# Guardar snapshot manualmente
python3 /root/.openclaw/supervisor/sil-supervisor.py snapshot openclaw.json

# Restaurar snapshot
python3 /root/.openclaw/supervisor/sil-supervisor.py restore openclaw.json

# Ver snapshots disponibles
ls -la /root/.openclaw/snapshots/
```

## Configuración

Editable en el script `sil-supervisor.py`:

```python
CONFIG = {
    "max_snapshots": 5,           # Cuántos snapshots guardar
    "check_interval": 300,         # Segundos entre checks
    "post_change_wait": 30,       # Segundos después de cambio
    "alert_channels": ["telegram", "whatsapp"],  # Canales
    "critical_files": [
        "/root/.openclaw/openclaw.json",
        "/root/.openclaw/workspace/memory.db",
        "/root/.openclaw/workspace/data/contacts.db",
    ]
}
```

## Protocolo v3.0 con Supervisor

```
1. PLANIFICAR → Escribir el cambio
2. SNAPSHOT → python3 sil-supervisor.py snapshot openclaw.json
3. BACKUP → cp openclaw.json backup.json
4. VALIDAR → python3 -c "import json; json.load(open('config'))"
5. EJECUTAR → openclaw config set "path" "value"
6. ESPERAR → ⏳ 30 segundos (supervisando)
7. SUPERVISOR VERIFICA → Automaticamente
   ✅ Todo bien → Continuar
   ❌ Error → AUTO-RESPUESTA:
      ├── IA analiza error
      ├── Snapshot restaurado
      ├── Doctor --fix
      ├── Gateway restart
      └── Alertar a Alberto
8. APRENDIZAJE → Lección guardada en memory
```

## Flujo de Auto-Restauración

```
ERROR DETECTADO
       │
       ▼
┌──────────────────┐
│ AI ANALIZA ERROR │ ← MiniMax
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ GENERA LECCIÓN    │ → Para que Sil aprenda
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ REVERTIR SNAPSHOT │ ← Restaurar último funcional
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ DOCTOR --FIX     │ → Aplicar correcciones
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ GATEWAY RESTART  │ → Reiniciar
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  ALERTAR (T+W)   │ → Notificar a Alberto
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ INTEGRAR LECCIÓN │ → MEMORY.md + learning.db
└──────────────────┘
```

## Logs

```bash
# Ver logs en tiempo real
tail -f /root/.openclaw/logs/supervisor.log

# Ver últimos 100 líneas
tail -100 /root/.openclaw/logs/supervisor.log
```

## Eliminación

```bash
# Detener servicio
systemctl --user stop sil-supervisor.service
systemctl --user disable sil-supervisor.service

# Opcional: eliminar archivos
rm -rf /root/.openclaw/supervisor
rm -rf /root/.openclaw/snapshots
```

---

*Creado: 2026-02-06*
*Versión: 3.0.0*
