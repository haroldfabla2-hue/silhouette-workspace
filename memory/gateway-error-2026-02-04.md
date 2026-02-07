# 2026-02-04 - Error de Gateway WebSocket y Solución

## Resumen

Error al intentar acceder a la UI de OpenClaw desde el navegador. Se resolvió configurando Tailscale Serve en puerto 8443.

## Problemas Encontrados

### 1. Error 1006 WebSocket
- **Síntoma:** "disconnected (1006): no reason"
- **Causa:** Caddy sin soporte WebSocket

### 2. Error 404 Not Found (Tailscale)
- **Síntoma:** "Not Found" al acceder a la URL de Tailscale
- **Causa:** Conflicto de puertos (Caddy usaba 443, Tailscale también quería 443)

### 3. Pairing Required
- **Síntoma:** "disconnected (1008): pairing required"
- **Causa:** Nuevo dispositivo requería aprobación

## Solución Paso a Paso

### Paso 1: Instalar Tailscale
```bash
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/focal.noarmor.gpg | sudo gpg --dearmor -o /usr/share/keyrings/tailscale-archive-keyring.gpg
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/focal.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
apt-get update && apt-get install -y tailscale
```

### Paso 2: Autenticar con Auth Key
```bash
tailscale up --auth-key=TpHejYAp8N11CNTRL
```

### Paso 3: Configurar Gateway con allowTailscale
```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "CJCCZP9xYVF0DNF+lT6KmXOXLvlAmDj33boiKZipZoo=",
      "allowTailscale": true
    }
  }
}
```

### Paso 4: Configurar Tailscale Serve en puerto 8443
```bash
tailscale serve reset
tailscale serve --bg --https=8443 127.0.0.1:18789
```

### Paso 5: Aprobar dispositivo
```bash
openclaw devices list
openclaw devices approve <requestId>
```

## Lecciones Aprendidas

1. **Caddy y Tailscale Serve no pueden compartir el puerto 443**
   - Solución: Usar puerto 8443 para Tailscale Serve

2. **Gateway debe quedarse en loopback por seguridad**
   - Tailscale Serve hace el proxy inverso desde el servidor mismo

3. **Device pairing es obligatorio para nuevos dispositivos**
   - even from the same Tailnet
   - Aprobación requerida para cada browser/nuevo dispositivo

4. **allowTailscale debe estar habilitado**
   - Permite autenticación via identidad Tailscale

## URLs de Acceso

- **Producción (Tailscale):** https://silhouetteserver.tail77b896.ts.net:8443/openclaw/
- **Local (servidor):** http://localhost:18789/openclaw/

## Token de Acceso

```
CJCCZP9xYVF0DNF+lT6KmXOXLvlAmDj33boiKZipZoo=
```

## Verificación

```bash
# Verificar serve
tailscale serve status

# Verificar gateway
ps aux | grep openclaw-gateway

# Ver dispositivos
openclaw devices list
```

## Archivos Modificados

- `/root/.openclaw/openclaw.json` - Gateway config
- `/etc/caddy/Caddyfile` - Caddy config (WebSocket headers)
- `/var/lib/tailscale/certs/` - Certificados TLS de Tailscale

## Estado Final

✅ Gateway funcionando en loopback
✅ Tailscale Serve en puerto 8443
✅ Caddy funcionando en puerto 443
✅ Dispositivo aprobado
✅ UI accesible desde laptop
