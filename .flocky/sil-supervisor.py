#!/usr/bin/env python3
"""
Sil External Supervisor v3.0 - Flocky
Sistema de supervisión externo, robusto e inteligente
Monitorea OpenClaw, guarda snapshots, auto-restaura, y enseña a Sil
"""

import os
import sys
import json
import shutil
import subprocess
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple

# ============================================
# CONFIGURACIÓN
# ============================================

CONFIG = {
    # Paths
    "openclaw_config": "/root/.openclaw/openclaw.json",
    "snapshots_dir": "/root/.openclaw/snapshots",
    "logs_dir": "/root/.openclaw/logs",
    "memory_db": "/root/.openclaw/workspace/memory.db",
    
    # Para Sil - Reportes de aprendizaje
    "learning_report": "/root/.openclaw/supervisor/learning_report.md",
    
    # Snapshots
    "max_snapshots": 5,
    
    # Checks
    "check_interval": 300,  # 5 minutos
    "post_change_wait": 30,  # 30 segundos después de cambio
    
    # API Keys
    "minimax_api_key": os.environ.get("MINIMAX_API_KEY", "sk-cp-bKOW_nJ_vF3pTb-D9ZWGDg9Cifm8DzvOQYpHYmUL3cgD89Yiv-ZtUjs2PL9Kn0-QPV_9733sS45dlsYC-gPAlNoeEFb-6PS10mmIqv-KKbw3nrDt85o-PtE"),
    
    # Channels para alertas (Sil usará estos para notify)
    "alert_channels": ["telegram", "whatsapp"],
    
    # Archivos críticos a supervisar
    "critical_files": [
        "/root/.openclaw/openclaw.json",
        "/root/.openclaw/workspace/memory.db",
        "/root/.openclaw/workspace/data/contacts.db",
    ]
}

# Logging
LOG_FILE = Path(CONFIG["logs_dir"]) / "supervisor.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# UTILIDADES
# ============================================

def timestamp() -> str:
    """Timestamp formateado"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run_command(cmd: list, timeout: int = 30) -> Tuple[int, str, str]:
    """Ejecutar comando y retornar (code, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

# ============================================
# SNAPSHOTS
# ============================================

def save_snapshot(name: str, filepath: str) -> Optional[str]:
    """Guardar snapshot de un archivo"""
    try:
        snap_dir = Path(CONFIG["snapshots_dir"])
        snap_dir.mkdir(exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = snap_dir / f"{name}.{ts}.json"
        
        shutil.copy(filepath, dest)
        
        # Auto-rotate
        snapshots = sorted(snap_dir.glob(f"{name}.*.json"))
        for old in snapshots[:-CONFIG["max_snapshots"]]:
            old.unlink()
            logger.info(f"🗑️ Snapshot eliminado: {old.name}")
        
        logger.info(f"✅ Snapshot: {dest.name}")
        return str(dest)
    except Exception as e:
        logger.error(f"❌ Error snapshot: {e}")
        return None

def get_latest_snapshot(name: str) -> Optional[Path]:
    """Obtener snapshot más reciente"""
    snap_dir = Path(CONFIG["snapshots_dir"])
    snapshots = sorted(snap_dir.glob(f"{name}.*.json"))
    return snapshots[-1] if snapshots else None

# ============================================
# SALUD DE OPENCLAW
# ============================================

def check_openclaw_health() -> Tuple[bool, str, str]:
    """Verificar salud de OpenClaw"""
    code, stdout, stderr = run_command(["openclaw", "doctor"])
    if code == 0 and "Doctor complete" in stdout:
        return True, stdout, stderr
    return False, stdout, stderr

def check_config_valid() -> Tuple[bool, str]:
    """Verificar que el config sea válido"""
    try:
        with open(CONFIG["openclaw_config"]) as f:
            json.load(f)
        return True, "Config válido"
    except json.JSONDecodeError as e:
        return False, f"JSON inválido: {e}"
    except Exception as e:
        return False, str(e)

# ============================================
# ANÁLISIS IA (MINIMAX)
# ============================================

def analyze_with_ai(error_log: str, change_made: str) -> Dict:
    """Usar MiniMax para analizar el error"""
    
    if not CONFIG["minimax_api_key"]:
        return {
            "root_cause": "Unknown (no API key)",
            "explanation": "No se pudo analizar con IA",
            "solution": "Revisar logs manualmente",
            "lesson_for_sil": "Verificar que MINIMAX_API_KEY esté configurada"
        }
    
    prompt = f"""
Analiza este error de OpenClaw:

CONTEXTO:
- OpenClaw es un asistente AI personal
- Sil es la IA principal
- Flocky es el supervisor externo
- Hay un protocolo: snapshot → cambio → verificar

ERROR:
{error_log}

CAMBIO REALIZADO:
{change_made}

TAREA:
Genera un análisis JSON con:
1. "root_cause": Frase corta de la causa raíz
2. "explanation": Explicación clara
3. "solution": Solución específica
4. "lesson_for_sil": Lección breve (máx 50 palabras) que Sil debe integrar

Responde SOLO JSON sin markdown.
"""
    
    try:
        import requests
        
        response = requests.post(
            "https://api.minimax.io/anthropic/v1/messages",
            headers={
                "Authorization": f"Bearer {CONFIG['minimax_api_key']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "MiniMax-M2.1",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", "")
            
            # Extraer JSON de la respuesta
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
                return json.loads(json_str)
            except:
                return {
                    "root_cause": "Parse error",
                    "explanation": content[:300],
                    "solution": "Revisar respuesta de IA",
                    "lesson_for_sil": "La IA tuvo problemas generando JSON válido"
                }
    except Exception as e:
        logger.error(f"❌ Error IA: {e}")
    
    return {
        "root_cause": "Unknown",
        "explanation": f"Error: {str(e)}",
        "solution": "Revisar logs",
        "lesson_for_sil": "Verificar conexión con API de IA"
    }

# ============================================
# ESCRITURA DE REPORTE PARA SIL
# ============================================

def write_learning_report(error_info: Dict, actions: list) -> None:
    """Escribir reporte de aprendizaje para Sil"""
    
    report = f"""## 🛡️ REPORTE DE FLOCKY - ERROR DETECTADO

**Fecha:** {timestamp()}

### ❌ Error
**Causa Raíz:** {error_info.get('root_cause', 'Unknown')}

### 📝 Análisis
{error_info.get('explanation', 'N/A')}

### ✅ Solución Aplicada
1. Snapshot restaurado: {actions[0]}
2. Doctor --fix: {'✅' if actions[1] else '❌'}
3. Gateway restart: {'✅' if actions[2] else '❌'}

### 🎓 Lección para Sil
{error_info.get('lesson_for_sil', 'No disponible')}

### 📋 Para Integrar en MEMORY.md
- Error: {error_info.get('root_cause', 'Unknown')}
- Lección: {error_info.get('lesson_for_sil', 'N/A')}
- Solución: {error_info.get('solution', 'N/A')}

---
*Generado por Flocky v3.0*
"""
    
    try:
        with open(CONFIG["learning_report"], "w") as f:
            f.write(report)
        logger.info(f"📝 Reporte escrito para Sil: {CONFIG['learning_report']}")
    except Exception as e:
        logger.error(f"❌ Error escribiendo reporte: {e}")

# ============================================
# AUTO-RESTAURACIÓN
# ============================================

def restore_snapshot_func(snapshot_path: str, target_path: str) -> bool:
    """Restaurar snapshot"""
    try:
        shutil.copy(snapshot_path, target_path)
        logger.info(f"✅ Restaurado: {snapshot_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error restaurando: {e}")
        return False

def apply_fix() -> bool:
    """Aplicar openclaw doctor --fix"""
    code, stdout, stderr = run_command(["openclaw", "doctor", "--fix"])
    return code == 0

def restart_gateway() -> bool:
    """Reiniciar gateway"""
    code, stdout, stderr = run_command(["openclaw", "gateway", "restart"])
    time.sleep(5)
    return code == 0

# ============================================
# ALERTAS (Espera a que Sil las envíe)
# ============================================

def prepare_alert(error_info: Dict, snapshot_name: str, actions: list) -> str:
    """Preparar alerta para que Sil envíe"""
    
    return f"""🛡️ FLOCKY v3.0 - ERROR DETECTADO

❌ Error: {error_info.get('root_cause', 'Unknown')}

📝 Análisis: {error_info.get('explanation', 'N/A')[:200]}...

✅ Solución Aplicada:
- Snapshot restaurado: {snapshot_name}
- Doctor --fix: {'✅' if actions[1] else '❌'}
- Gateway restart: {'✅' if actions[2] else '❌'}

🎓 Lección: {error_info.get('lesson_for_sil', 'N/A')}

⏰ {timestamp()}

*Reporte listo para enviar a Alberto*"""

# ============================================
# CICLO PRINCIPAL
# ============================================

def supervisor_loop():
    """Loop principal del supervisor"""
    logger.info("="*60)
    logger.info("🛡️ FLOCKY v3.0 INICIADO")
    logger.info("="*60)
    
    while True:
        try:
            healthy, stdout, stderr = check_openclaw_health()
            config_ok, config_msg = check_config_valid()
            
            if not config_ok:
                logger.error(f"❌ Config inválido: {config_msg}")
                
                latest = get_latest_snapshot("openclaw.json")
                if latest:
                    logger.info(f"🔄 Restaurando: {latest.name}")
                    
                    # Análisis IA
                    error_info = analyze_with_ai(config_msg, "Cambio de configuración")
                    
                    # Restaurar
                    restored = restore_snapshot_func(str(latest), CONFIG["openclaw_config"])
                    fix_applied = apply_fix()
                    restarted = restart_gateway()
                    
                    actions = [latest.name, fix_applied, restarted]
                    
                    # ESCRIBIR REPORTE PARA SIL
                    write_learning_report(error_info, actions)
                    
                    # Preparar alerta
                    alert = prepare_alert(error_info, latest.name, actions)
                    with open("/root/.openclaw/supervisor/pending_alert.txt", "w") as f:
                        f.write(alert)
                    
                    logger.info("📝 Reporte escrito para Sil")
                
                time.sleep(60)
                continue
            
            if healthy:
                logger.info(f"✅ OpenClaw saludable - {timestamp()}")
            
            # Snapshot periódico (cada 6 horas)
            save_snapshot("openclaw.json", CONFIG["openclaw_config"])
            
            time.sleep(CONFIG["check_interval"])
            
        except KeyboardInterrupt:
            logger.info("🛑 Flocky detenido")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            time.sleep(60)

# ============================================
# COMANDOS
# ============================================

def cmd_snapshot(name: str) -> None:
    """Guardar snapshot"""
    filepath = CONFIG.get(name.replace(".", "_"))
    if filepath and Path(filepath).exists():
        result = save_snapshot(name, filepath)
        print(f"✅ {result}")
    else:
        for critical in CONFIG["critical_files"]:
            if name in critical:
                result = save_snapshot(Path(critical).name, critical)
                print(f"✅ {result}")
                return
        print(f"❌ Archivo no encontrado: {name}")

def cmd_check() -> None:
    """Verificar salud"""
    healthy, _, _ = check_openclaw_health()
    config_ok, _ = check_config_valid()
    
    print(f"🛡️ FLOCKY v3.0 - CHECK")
    print(f"   OpenClaw: {'✅' if healthy else '❌'}")
    print(f"   Config: {'✅' if config_ok else '❌'}")
    print(f"   Snapshots: {len(list(Path(CONFIG['snapshots_dir']).glob('openclaw.json.*.json')))}")
    print(f"   Timestamp: {timestamp()}")

def cmd_status() -> None:
    """Estado del supervisor"""
    print(f"🛡️ FLOCKY v3.0 - STATUS")
    print(f"   Snapshots dir: {CONFIG['snapshots_dir']}")
    print(f"   Max snapshots: {CONFIG['max_snapshots']}")
    print(f"   Check interval: {CONFIG['check_interval']}s")
    print(f"   API key: {'✅' if CONFIG['minimax_api_key'] else '❌'}")
    print(f"   Reporte para Sil: {CONFIG['learning_report']}")

def cmd_restore(name: str, index: int = -1) -> None:
    """Restaurar snapshot"""
    snapshots = sorted(Path(CONFIG["snapshots_dir"]).glob(f"{name}.*.json"))
    if not snapshots:
        print("❌ No hay snapshots")
        return
    
    snapshot = snapshots[index] if index >= 0 else snapshots[-1]
    filepath = CONFIG.get(name.replace(".", "_"))
    
    if restore_snapshot_func(str(snapshot), filepath):
        print(f"✅ Restaurado: {snapshot.name}")

def cmd_alert() -> None:
    """Obtener alerta pendiente"""
    alert_file = "/root/.openclaw/supervisor/pending_alert.txt"
    if Path(alert_file).exists():
        with open(alert_file) as f:
            print(f.read())
    else:
        print("✅ No hay alertas pendientes")

def cmd_test_ai() -> None:
    """Probar IA"""
    result = analyze_with_ai(
        "Config JSON inválido en línea 47",
        "Cambio de apiKey"
    )
    print("=== IA TEST ===")
    print(f"Root Cause: {result.get('root_cause', 'N/A')}")
    print(f"Lesson: {result.get('lesson_for_sil', 'N/A')}")

# ============================================
# MAIN
# ============================================

def main():
    """Entry point"""
    
    if len(sys.argv) < 2:
        supervisor_loop()
    else:
        cmd = sys.argv[1]
        
        if cmd == "snapshot":
            name = sys.argv[2] if len(sys.argv) > 2 else "openclaw.json"
            cmd_snapshot(name)
        
        elif cmd == "check":
            cmd_check()
        
        elif cmd == "status":
            cmd_status()
        
        elif cmd == "restore":
            name = sys.argv[2] if len(sys.argv) > 2 else "openclaw.json"
            idx = int(sys.argv[3]) if len(sys.argv) > 3 else -1
            cmd_restore(name, idx)
        
        elif cmd == "alert":
            cmd_alert()
        
        elif cmd == "test-ai":
            cmd_test_ai()
        
        else:
            print("Comandos:")
            print("  snapshot <archivo>  - Guardar snapshot")
            print("  check               - Verificar salud")
            print("  status             - Estado")
            print("  restore <archivo>  - Restaurar snapshot")
            print("  alert              - Ver alerta pendiente")
            print("  test-ai            - Probar IA")

if __name__ == "__main__":
    main()
