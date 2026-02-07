#!/usr/bin/env python3
"""
Flocky v4.0 - External Intelligent Watchdog
Sistema de supervisión externo, robusto e inteligente
NO depende de OpenClaw - Solo herramientas del sistema
"""

import os
import sys
import json
import shutil
import subprocess
import time
import logging
import signal
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple, List

# ============================================
# CONFIGURACIÓN (100% Externa)
# ============================================

class FlockyConfig:
    """Configuración de Flocky v4.0"""
    
    # Paths
    OPENCLAW_CONFIG = "/root/.openclaw/openclaw.json"
    SNAPSHOTS_DIR = "/root/.openclaw/supervisor/snapshots"
    ERRORS_DIR = "/root/.openclaw/supervisor/errors"
    HISTORY_DIR = "/root/.openclaw/supervisor/history"
    LOGS_DIR = "/root/.openclaw/logs"
    LEARNING_REPORT = "/root/.openclaw/supervisor/learning_report.md"
    PENDING_ALERT = "/root/.openclaw/supervisor/pending_alert.txt"
    WAKE_FLAG = "/root/.openclaw/supervisor/wake_sil.flag"
    STATUS_FILE = "/root/.openclaw/supervisor/status.json"
    
    # Snapshots
    MAX_SNAPSHOTS = 5
    
    # Timing
    CHECK_INTERVAL = 30  # 30 segundos (para pruebas, production: 300)
    POST_CHANGE_WAIT = 10  # 10 segundos después de cambio
    
    # AI (MiniMax)
    AI_ENDPOINT = "https://api.minimax.io/anthropic/v1/messages"
    AI_MODEL = "MiniMax-M2.1"
    AI_API_KEY = "sk-cp-bKOW_nJ_vF3pTb-D9ZWGDg9Cifm8DzvOQYpHYmUL3cgD89Yiv-ZtUjs2PL9Kn0-QPV_9733sS45dlsYC-gPAlNoeEFb-6PS10mmIqv-KKbw3nrDt85o-PtE"
    AI_TIMEOUT = 60
    AI_MAX_TOKENS = 1000
    
    # Services
    OPENCLAW_SERVICE = "openclaw-gateway.service"
    
    # Puertos
    GATEWAY_WS = "ws://127.0.0.1:18789"
    GATEWAY_HTTP = "http://127.0.0.1:18789"
    
    # Alertas
    ALERTS_DIR = "/root/.openclaw/supervisor/alerts"
    ALERT_FILE = "/root/.openclaw/supervisor/alerts/urgent_alert.json"
    
    # Tests
    TEST_MODE = False  # Activar contest para -- pruebas


# ============================================
# LOGGING
# ============================================

class FlockyLogger:
    """Logger de Flocky"""
    
    def __init__(self):
        self.log_file = Path(FlockyConfig.LOGS_DIR) / "flocky_v4.log"
        self.log_file.parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("flocky_v4")
    
    def info(self, msg: str):
        self.logger.info(msg)
    
    def error(self, msg: str):
        self.logger.error(msg)
    
    def warning(self, msg: str):
        self.logger.warning(msg)


# ============================================
# UTILIDADES DEL SISTEMA (100% Externo)
# ============================================

class SystemUtils:
    """Utilidades del sistema - SIN dependencias de OpenClaw"""
    
    @staticmethod
    def run_command(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
        """Ejecutar comando del sistema"""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)
    
    @staticmethod
    def cp(src: str, dst: str) -> bool:
        """Copiar archivo"""
        try:
            shutil.copy2(src, dst)
            return True
        except Exception:
            return False
    
    @staticmethod
    def systemctl(action: str, service: str) -> Tuple[bool, str]:
        """Controlar servicio systemd"""
        code, stdout, stderr = SystemUtils.run_command(
            ["systemctl", "--user", action, service],
            timeout=30
        )
        return code == 0, stderr or stdout
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """Verificar si archivo existe"""
        return Path(path).exists()
    
    @staticmethod
    def read_file(path: str) -> Optional[str]:
        """Leer archivo"""
        try:
            with open(path) as f:
                return f.read()
        except Exception:
            return None
    
    @staticmethod
    def write_file(path: str, content: str) -> bool:
        """Escribir archivo"""
        try:
            Path(path).parent.mkdir(exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_file(path: str) -> bool:
        """Eliminar archivo"""
        try:
            Path(path).unlink()
            return True
        except Exception:
            return False
    
    @staticmethod
    def timestamp() -> str:
        """Timestamp formateado"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def curl_get(url: str, timeout: int = 5) -> Tuple[bool, str]:
        """HTTP GET request"""
        code, stdout, stderr = SystemUtils.run_command(
            ["curl", "-s", "-m", str(timeout), url],
            timeout=10
        )
        return code == 0, stdout[:500] if stdout else ""


# ============================================
# SNAPSHOT MANAGER
# ============================================

class SnapshotManager:
    """Gestor de snapshots - solo cp del sistema"""
    
    def __init__(self, logger: FlockyLogger):
        self.logger = logger
        self.snapshots_dir = Path(FlockyConfig.SNAPSHOTS_DIR)
        self.errors_dir = Path(FlockyConfig.ERRORS_DIR)
        self.snapshots_dir.mkdir(exist_ok=True)
        self.errors_dir.mkdir(exist_ok=True)
    
    def save_snapshot(self, name: str, filepath: str) -> Optional[str]:
        """Guardar snapshot - solo cp"""
        try:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            dest = self.snapshots_dir / f"{name}.{ts}.json"
            
            if SystemUtils.cp(filepath, str(dest)):
                self.logger.info(f"✅ Snapshot: {dest.name}")
                
                # Auto-rotate: mantener solo MAX_SNAPSHOTS
                snapshots = sorted(self.snapshots_dir.glob(f"{name}.*.json"))
                for old in snapshots[:-FlockyConfig.MAX_SNAPSHOTS]:
                    old.unlink()
                    self.logger.info(f"🗑️ Eliminado: {old.name}")
                
                return str(dest)
            return None
        except Exception as e:
            self.logger.error(f"❌ Error guardando snapshot: {e}")
            return None
    
    def get_latest_snapshot(self, name: str) -> Optional[Path]:
        """Obtener snapshot más reciente"""
        snapshots = sorted(self.snapshots_dir.glob(f"{name}.*.json"))
        return snapshots[-1] if snapshots else None
    
    def list_snapshots(self, name: str) -> List[Path]:
        """Listar todos los snapshots"""
        return sorted(self.snapshots_dir.glob(f"{name}.*.json"))
    
    def save_error_context(self, error_type: str, content: str) -> str:
        """Guardar contexto del error"""
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"error_{error_type}_{ts}.json"
        filepath = self.errors_dir / filename
        
        SystemUtils.write_file(str(filepath), content)
        self.logger.info(f"📁 Error guardado: {filename}")
        return str(filepath)


# ============================================
# AI BRAIN (MINIMAX)
# ============================================

class AIBrain:
    """Inteligencia de Flocky - MiniMax API"""
    
    def __init__(self, logger: FlockyLogger):
        self.logger = logger
        self.endpoint = FlockyConfig.AI_ENDPOINT
        self.model = FlockyConfig.AI_MODEL
        self.api_key = FlockyConfig.AI_API_KEY
    
    def analyze_error(self, error: str, context: str, logs: str) -> Dict:
        """Analizar error con MiniMax"""
        
        prompt = f"""
Analiza este error de OpenClaw:

ERROR:
{error}

CONTEXTO:
{context}

LOGS RELEVANTES:
{logs[-1000:]}

Genera un análisis JSON con:
1. "root_cause": Frase corta (max 10 palabras)
2. "explanation": Explicación clara (2-3 oraciones)
3. "solution": Lista de pasos específicos para resolver
4. "lesson_for_sil": Lección breve (max 50 palabras) que Sil debe aprender
5. "prevention": Cómo prevenir este error en el futuro

Responde SOLO JSON sin markdown ni texto adicional.
"""
        
        if not self.api_key or self.api_key.startswith("sk-cp-"):
            return self._fallback_analysis(error, context)
        
        try:
            import requests
            
            response = requests.post(
                self.endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": FlockyConfig.AI_MAX_TOKENS
                },
                timeout=FlockyConfig.AI_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("content", "")
                
                # Extraer JSON de la respuesta
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
                
                return json.loads(json_str)
            
            self.logger.error(f"❌ AI API error: {response.status_code}")
            return self._fallback_analysis(error, context)
            
        except Exception as e:
            self.logger.error(f"❌ Error en AI: {e}")
            return self._fallback_analysis(error, context)
    
    def _fallback_analysis(self, error: str, context: str) -> Dict:
        """Análisis sin IA"""
        return {
            "root_cause": "Error de sistema",
            "explanation": f"Error detectado: {error[:100]}",
            "solution": "1. Revisar logs\n2. Restaurar snapshot\n3. Reiniciar servicio",
            "lesson_for_sil": "Los errores deben ser analizados con IA para generar lecciones específicas.",
            "prevention": "Implementar validación antes de aplicar cambios."
        }


# ============================================
# HEALTH CHECKER
# ============================================

class HealthChecker:
    """Verificador de salud - herramientas del sistema"""
    
    def __init__(self, logger: FlockyLogger):
        self.logger = logger
    
    def check_config_valid(self) -> Tuple[bool, str]:
        """Verificar que el config sea JSON válido"""
        try:
            with open(FlockyConfig.OPENCLAW_CONFIG) as f:
                json.load(f)
            return True, "Config válido"
        except json.JSONDecodeError as e:
            return False, f"JSON inválido: {e}"
        except Exception as e:
            return False, str(e)
    
    def check_gateway_status(self) -> Tuple[bool, str]:
        """Verificar estado del gateway"""
        # Verificar si el servicio está corriendo
        success, output = SystemUtils.systemctl("status", FlockyConfig.OPENCLAW_SERVICE)
        
        if success and "active (running)" in output:
            return True, "Gateway activo"
        
        # Verificar puerto
        alive, _ = SystemUtils.curl_get(FlockyConfig.GATEWAY_HTTP)
        if alive:
            return True, "Gateway responde"
        
        return False, "Gateway no responde"
    
    def check_gateway_health(self) -> Tuple[bool, str, str]:
        """Verificación completa"""
        # Intentar openclaw doctor si existe
        code, stdout, stderr = SystemUtils.run_command(
            ["openclaw", "doctor"],
            timeout=30
        )
        
        if code == 0 and "Doctor complete" in stdout:
            return True, stdout, stderr
        
        return False, stdout, stderr


# ============================================
# FLOCKY v4.0 CORE
# ============================================

class Flocky:
    """Flocky v4.0 - Watchdog Externo Inteligente"""
    
    # Estados
    STATE_IDLE = "IDLE"
    STATE_ERROR = "ERROR_DETECTED"
    STATE_AI = "AI_ANALYZING"
    STATE_RESTORE = "RESTORING"
    STATE_RESTART = "RESTARTING"
    STATE_WAKEUP = "WAKE_UP"
    STATE_DONE = "DONE"
    
    def __init__(self):
        self.logger = FlockyLogger()
        self.snapshots = SnapshotManager(self.logger)
        self.ai = AIBrain(self.logger)
        self.health = HealthChecker(self.logger)
        
        self.state = self.STATE_IDLE
        self.running = True
        self.error_count = 0
        self.total_errors = 0
        
        # Configurar señal de salida
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)
    
    def _shutdown(self, signum, frame):
        """Manejar cierre"""
        self.logger.info("🛑 Flocky cerrando...")
        self.running = False
    
    def save_status(self):
        """Guardar estado actual"""
        status = {
            "state": self.state,
            "error_count": self.error_count,
            "total_errors": self.total_errors,
            "timestamp": SystemUtils.timestamp(),
            "snapshots_count": len(self.snapshots.list_snapshots("openclaw.json"))
        }
        
        SystemUtils.write_file(
            FlockyConfig.STATUS_FILE,
            json.dumps(status, indent=2)
        )
    
    def _validate_json(self, filepath: str) -> bool:
        """Validar que un archivo JSON es válido"""
        try:
            with open(filepath) as f:
                json.load(f)
            return True
        except Exception:
            return False
    
    def _restore_config_with_verification(self) -> bool:
        """Restaurar config con verificación y reintentos
        
        Returns:
            bool: True si la restauración fue exitosa y verificada
        """
        snapshots = self.snapshots.list_snapshots("openclaw.json")
        
        if not snapshots:
            self.logger.error("❌ No hay snapshots disponibles")
            return False
        
        max_retries = 3
        snapshot_index = len(snapshots) - 1  # Empezar por el más reciente
        
        while snapshot_index >= 0 and snapshot_index >= len(snapshots) - max_retries:
            snapshot = snapshots[snapshot_index]
            
            for retry in range(max_retries):
                self.logger.info(f"🔄 Intento {retry + 1}/{max_retries}: {snapshot.name}")
                
                # 1. Copiar snapshot
                cp_result = SystemUtils.cp(str(snapshot), FlockyConfig.OPENCLAW_CONFIG)
                
                if not cp_result:
                    self.logger.error(f"❌ Error copiando: {snapshot.name}")
                    time.sleep(2 ** retry)  # Delay exponencial
                    continue
                
                # 2. Verificar que el JSON es válido
                if self._validate_json(FlockyConfig.OPENCLAW_CONFIG):
                    self.logger.info(f"✅ Restaurado y verificado: {snapshot.name}")
                    return True
                else:
                    self.logger.error(f"❌ Snapshot corrupto: {snapshot.name}")
            
            # Si el snapshot más reciente falla, intentar el anterior
            snapshot_index -= 1
        
        self.logger.error("❌ No se pudo restaurar ningún snapshot válido")
        return False
    
    def _restart_gateway_with_verification(self) -> bool:
        """Reiniciar gateway con verificación
        
        Returns:
            bool: True si el gateway está funcionando
        """
        max_retries = 3
        
        for retry in range(max_retries):
            self.logger.info(f"🔄 Reiniciando gateway (intento {retry + 1}/{max_retries})...")
            
            # 1. Detener servicio
            SystemUtils.systemctl("stop", FlockyConfig.OPENCLAW_SERVICE)
            time.sleep(2)
            
            # 2. Iniciar servicio
            success, _ = SystemUtils.systemctl("start", FlockyConfig.OPENCLAW_SERVICE)
            
            if not success:
                self.logger.error(f"❌ Error reiniciando (intento {retry + 1})")
                time.sleep(2 ** retry)  # Delay exponencial
                continue
            
            # 3. Verificar que está activo
            time.sleep(3)
            is_active, _ = self.health.check_gateway_status()
            
            if is_active:
                self.logger.info("✅ Gateway activo")
                return True
            else:
                self.logger.error(f"❌ Gateway no responde (intento {retry + 1})")
        
        self.logger.error("❌ No se pudo reiniciar el gateway")
        return False
    
    def _verify_system_health(self) -> bool:
        """Verificación completa de salud del sistema
        
        Returns:
            bool: True si todo está saludable
        """
        # 1. Verificar config
        config_ok, _ = self.health.check_config_valid()
        if not config_ok:
            self.logger.error("❌ Config inválido")
            return False
        
        # 2. Verificar gateway
        gateway_ok, _ = self.health.check_gateway_status()
        if not gateway_ok:
            self.logger.error("❌ Gateway no responde")
            return False
        
        return True
    
    def _write_learning_report(self, error_info: Dict, actions: List[str]) -> bool:
        """Escribir reporte de aprendizaje para Sil"""
        
        report = f"""## 🛡️ REPORTE DE FLOCKY - ERROR DETECTADO

**Fecha:** {SystemUtils.timestamp()}

### ❌ Error
**Causa Raíz:** {error_info.get('root_cause', 'Unknown')}

### 📝 Análisis IA
{error_info.get('explanation', 'N/A')}

### ✅ Acciones Tomadas
{chr(10).join([f'{i+1}. {action}' for i, action in enumerate(actions)])}

### 🎓 Lección para Sil
{error_info.get('lesson_for_sil', 'No disponible')}

### 📋 Prevention
{error_info.get('prevention', 'N/A')}

### 🔧 Solution
{error_info.get('solution', 'N/A')}

---
*Generado por Flocky v4.0*
"""
        
        return SystemUtils.write_file(FlockyConfig.LEARNING_REPORT, report)
    
    def _write_pending_alert(self, error_info: Dict, actions: List[str]) -> bool:
        """Escribir alerta pendiente"""
        
        alert = f"""🛡️ FLOCKY v4.0 - ERROR DETECTADO

❌ Error: {error_info.get('root_cause', 'Unknown')}

📝 Análisis: {error_info.get('explanation', 'N/A')[:200]}...

✅ Solución Aplicada:
- Snapshot restaurado: {actions[0]}
- Gateway reiniciado: {'✅' if actions[1] else '❌'}

🎓 Lección: {error_info.get('lesson_for_sil', 'N/A')}

⏰ {SystemUtils.timestamp()}
"""
        
        return SystemUtils.write_file(FlockyConfig.PENDING_ALERT, alert)
    
    def _write_wake_flag(self) -> bool:
        """Escribir flag para despertar a Sil"""
        
        flag = f"""{{
  "timestamp": "{SystemUtils.timestamp()}",
  "error_detected": true,
  "state": "{self.state}",
  "error_count": {self.error_count}
}}
"""
        
        return SystemUtils.write_file(FlockyConfig.WAKE_FLAG, flag)
    
    def _handle_error(self, error_msg: str, context: str):
        """Manejar un error detectado"""
        self.state = self.STATE_ERROR
        self.error_count += 1
        self.total_errors += 1
        
        self.logger.error(f"❌ {error_msg}")
        
        # 1. Guardar contexto del error
        self.snapshots.save_error_context(
            "config_invalid",
            json.dumps({
                "error": error_msg,
                "context": context,
                "timestamp": SystemUtils.timestamp()
            })
        )
        
        # 2. Análisis con IA
        self.state = self.STATE_AI
        ai_result = self.ai.analyze_error(error_msg, context, "")
        
        self.logger.info(f"🤖 IA: {ai_result.get('root_cause', 'Unknown')}")
        
        # 3. Restaurar snapshot con verificación
        self.state = self.STATE_RESTORE
        restore_success = self._restore_config_with_verification()
        
        # 4. Reiniciar gateway con verificación
        self.state = self.STATE_RESTART
        restart_success = self._restart_gateway_with_verification()
        
        actions = [
            self.snapshots.get_latest_snapshot("openclaw.json").name if restore_success else "FAILED",
            restart_success
        ]
        
        # 5. Verificación final del sistema
        if restore_success and restart_success:
            system_healthy = self._verify_system_health()
            if not system_healthy:
                self.logger.error("❌ Sistema no saludable después de restauración")
        
        # 6. Escribir reportes para Sil
        self.state = self.STATE_WAKEUP
        self._write_learning_report(ai_result, actions)
        self._write_pending_alert(ai_result, actions)
        self._write_wake_flag()
        self._write_direct_alert(ai_result, actions)  # Alerta directa
        
        self.logger.info("📝 Reportes escritos para Sil")
        
        # 6. Cambiar a DONE y volver a IDLE
        self.state = self.STATE_DONE
        self.logger.info("✅ Error manejado, volviendo a IDLE")
        
        self.state = self.STATE_IDLE
        self.error_count = 0
    
    def _write_direct_alert(self, error_info: Dict, actions: List[str]) -> bool:
        """Escribir alerta directa para Alberto (sin depender de Sil)
        
        Returns:
            bool: True si se escribió la alerta
        """
        # Crear directorio de alertas
        Path(FlockyConfig.ALERTS_DIR).mkdir(exist_ok=True)
        
        alert = {
            "timestamp": SystemUtils.timestamp(),
            "type": "URGENT",
            "error": error_info.get('root_cause', 'Unknown'),
            "explanation": error_info.get('explanation', 'N/A'),
            "lesson": error_info.get('lesson_for_sil', 'N/A'),
            "solution_applied": actions,
            "status": "RESOLVED" if actions[0] != "FAILED" else "FAILED",
            "generated_by": "flocky_v4",
            "requires_attention": False
        }
        
        alert_path = FlockyConfig.ALERT_FILE
        success = SystemUtils.write_file(alert_path, json.dumps(alert, indent=2))
        
        if success:
            self.logger.info(f"📨 Alerta directa escrita: {alert_path}")
        
        return success
    
    def run_self_test(self) -> Dict:
        """Ejecutar test automatizado del sistema
        
        Returns:
            Dict: Resultados del test
        """
        self.logger.info("🧪 Ejecutando test automatizado...")
        
        results = {
            "timestamp": SystemUtils.timestamp(),
            "passed": True,
            "tests": []
        }
        
        # Test 1: Verificar snapshots
        snapshots = self.snapshots.list_snapshots("openclaw.json")
        test1 = {
            "name": "Snapshots disponibles",
            "passed": len(snapshots) >= 1,
            "details": f"{len(snapshots)} snapshots"
        }
        results["tests"].append(test1)
        if not test1["passed"]:
            results["passed"] = False
        
        # Test 2: Verificar que al menos un snapshot es válido
        test2 = {"name": "Snapshot válido", "passed": False, "details": ""}
        for snap in snapshots[:3]:  # Revisar los 3 más recientes
            if self._validate_json(str(snap)):
                test2["passed"] = True
                test2["details"] = f"{snap.name} es válido"
                break
        if not test2["passed"]:
            test2["details"] = "Ningún snapshot es válido"
            results["passed"] = False
        results["tests"].append(test2)
        
        # Test 3: Verificar config actual
        config_valid = self._validate_json(FlockyConfig.OPENCLAW_CONFIG)
        test3 = {
            "name": "Config actual válido",
            "passed": config_valid,
            "details": "OK" if config_valid else "Config corrupto"
        }
        results["tests"].append(test3)
        if not test3["passed"]:
            results["passed"] = False
        
        # Test 4: Verificar gateway
        gateway_ok, _ = self.health.check_gateway_status()
        test4 = {
            "name": "Gateway respondiendo",
            "passed": gateway_ok,
            "details": "OK" if gateway_ok else "Gateway down"
        }
        results["tests"].append(test4)
        if not test4["passed"]:
            results["passed"] = False
        
        # Guardar resultados
        test_results_file = f"/root/.openclaw/supervisor/test_results_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        SystemUtils.write_file(test_results_file, json.dumps(results, indent=2))
        
        self.logger.info(f"🧪 Test completado: {'✅' if results['passed'] else '❌'}")
        
        return results
    
    def run(self):
        """Loop principal de Flocky"""
        self.logger.info("="*60)
        self.logger.info("🛡️ FLOCKY v4.0 INICIADO")
        self.logger.info("="*60)
        self.logger.info(f"🔧 Check interval: {FlockyConfig.CHECK_INTERVAL}s")
        self.logger.info(f"📁 Snapshots: {FlockyConfig.MAX_SNAPSHOTS}")
        self.logger.info(f"🧠 AI: MiniMax ({self.ai.model})")
        
        last_snapshot_time = None
        
        while self.running:
            try:
                # 1. Verificar salud
                self.logger.info("🔍 Health check...")
                
                # Verificar config
                config_ok, config_msg = self.health.check_config_valid()
                
                if not config_ok:
                    self._handle_error(config_msg, "Validación de config falló")
                    time.sleep(FlockyConfig.CHECK_INTERVAL)
                    continue
                
                # Verificar gateway
                gateway_ok, gateway_msg = self.health.check_gateway_status()
                
                if not gateway_ok:
                    self._handle_error(gateway_msg, "Gateway no responde")
                    time.sleep(FlockyConfig.CHECK_INTERVAL)
                    continue
                
                # 2. Todo bien - modo IDLE
                if self.state == self.STATE_IDLE:
                    self.logger.info(f"✅ Saludable - {SystemUtils.timestamp()}")
                    
                    # Guardar snapshot periódico (cada 6 horas)
                    now = datetime.now()
                    if last_snapshot_time and (now - last_snapshot_time).total_seconds() > 21600:
                        self.snapshots.save_snapshot(
                            "openclaw.json",
                            FlockyConfig.OPENCLAW_CONFIG
                        )
                        last_snapshot_time = now
                    elif not last_snapshot_time:
                        last_snapshot_time = now
                
                self.save_status()
                
                # Dormir hasta próximo check
                time.sleep(FlockyConfig.CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Flocky detenido")
                break
            except Exception as e:
                self.logger.error(f"❌ Error en loop: {e}")
                time.sleep(60)
        
        self.logger.info("👋 Flocky cerrado")


# ============================================
# COMANDOS
# ============================================

def cmd_status():
    """Ver estado de Flocky"""
    if SystemUtils.file_exists(FlockyConfig.STATUS_FILE):
        status = json.loads(SystemUtils.read_file(FlockyConfig.STATUS_FILE) or "{}")
        print(f"🛡️ FLOCKY v4.0 - STATUS")
        print(f"   State: {status.get('state', 'Unknown')}")
        print(f"   Last check: {status.get('last_check', 'N/A')}")
        print(f"   Errors: {status.get('error_count', 0)}")
        print(f"   Snapshots: {status.get('snapshots_count', 0)}")
    else:
        print("❌ Flocky no ha corrido aún")

def cmd_check():
    """Verificar salud manualmente"""
    health = HealthChecker(FlockyLogger())
    
    config_ok, config_msg = health.check_config_valid()
    gateway_ok, gateway_msg = health.check_gateway_status()
    
    print(f"🛡️ FLOCKY v4.0 - CHECK")
    print(f"   Config: {'✅' if config_ok else '❌'}")
    print(f"   Gateway: {'✅' if gateway_ok else '❌'}")

def cmd_snapshot():
    """Guardar snapshot manualmente"""
    snapshots = SnapshotManager(FlockyLogger())
    result = snapshots.save_snapshot("openclaw.json", FlockyConfig.OPENCLAW_CONFIG)
    print(f"✅ {result}" if result else "❌ Error")

def cmd_restore(index: int = -1):
    """Restaurar snapshot"""
    snapshots = SnapshotManager(FlockyLogger())
    snapshot_list = snapshots.list_snapshots("openclaw.json")
    
    if not snapshot_list:
        print("❌ No hay snapshots")
        return
    
    snapshot = snapshot_list[index] if index >= 0 else snapshot_list[-1]
    
    if SystemUtils.cp(str(snapshot), FlockyConfig.OPENCLAW_CONFIG):
        print(f"✅ Restaurado: {snapshot.name}")
    else:
        print("❌ Error restaurando")

def cmd_wakeup():
    """Simular wake up para Sil"""
    print("🛡️ FLOCKY v4.0 - WAKE UP")
    print("   Escribiendo flags para Sil...")
    
    SystemUtils.write_file(FlockyConfig.WAKE_FLAG, '{"test": true}')
    SystemUtils.write_file(FlockyConfig.LEARNING_REPORT, "## Test Report\n\nTest")
    SystemUtils.write_file(FlockyConfig.PENDING_ALERT, "Test Alert")
    
    print("✅ Flags escritos")
    print(f"   - {FlockyConfig.WAKE_FLAG}")
    print(f"   - {FlockyConfig.LEARNING_REPORT}")
    print(f"   - {FlockyConfig.PENDING_ALERT}")

def cmd_test_ai():
    """Probar IA"""
    ai = AIBrain(FlockyLogger())
    result = ai.analyze_error(
        "Config JSON inválido",
        "Cambio de apiKey",
        ""
    )
    
    print("🧠 AI TEST")
    print(f"   Root Cause: {result.get('root_cause', 'N/A')}")
    print(f"   Lesson: {result.get('lesson_for_sil', 'N/A')}")

def cmd_test():
    """Ejecutar test automatizado del sistema"""
    flocky = Flocky()
    results = flocky.run_self_test()
    
    print("🧪 FLOCKY v4.0 - SELF TEST")
    print()
    
    for test in results["tests"]:
        status = "✅" if test["passed"] else "❌"
        print(f"   {status} {test['name']}")
        print(f"      {test['details']}")
    
    print()
    print(f"RESULTADO: {'✅ PASÓ' if results['passed'] else '❌ FALLÓ'}")


# ============================================
# MAIN
# ============================================

def main():
    """Entry point"""
    
    if len(sys.argv) < 2:
        # Modo daemon
        flocky = Flocky()
        flocky.run()
    else:
        cmd = sys.argv[1]
        
        if cmd == "status":
            cmd_status()
        elif cmd == "check":
            cmd_check()
        elif cmd == "snapshot":
            cmd_snapshot()
        elif cmd == "restore":
            idx = int(sys.argv[2]) if len(sys.argv) > 2 else -1
            cmd_restore(idx)
        elif cmd == "wakeup":
            cmd_wakeup()
        elif cmd == "test-ai":
            cmd_test_ai()
        elif cmd == "test":
            cmd_test()
        else:
            print("Comandos de Flocky v4.0:")
            print("  status       - Ver estado")
            print("  check        - Verificar salud")
            print("  snapshot     - Guardar snapshot")
            print("  restore [n] - Restaurar snapshot (n=índice, -1=reciente)")
            print("  wakeup      - Escribir flags para Sil")
            print("  test-ai     - Probar IA")
            print("  test        - Test automatizado del sistema")
            print("")
            print("Sin argumentos: Modo daemon")


if __name__ == "__main__":
    main()
