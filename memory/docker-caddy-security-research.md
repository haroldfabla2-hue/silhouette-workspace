# Investigación: Docker & Caddy - Mejores Prácticas de Seguridad

**Fecha:** 2026-02-04
**Autor:** Sil (Asistente de Alberto Farah)

---

## DOCKER - Mejores Prácticas de Seguridad

### 1. Rootless vs Rootful

| Aspecto | Rootful (default) | Rootless |
|--------|-------------------|----------|
| Daemon | Corre como root | Corre como usuario normal |
| Contenedores | Acceso root real | UID/GID mapeados |
| Riesgo | Mayor si hay breach | Mitigado |
| Complejidad | Simple | Más complejo |

**Recomendación:** Para servidor de producción personal, **Rootful es aceptable** si:
- Solo Alberto tiene acceso sudo
- No hay servicios públicos que permitan upload de imágenes
- Se configura firewall correctamente

### 2. Aislamiento de Contenedores

Docker usa:
- **Namespaces** - Aísla procesos, red, filesystem
- **Control Groups (cgroups)** - Limita recursos (CPU, memoria, I/O)
- **Capabilities** - Permisos granulares (no root total por defecto)

### 3. Configuración de Seguridad

```json
// /etc/docker/daemon.json recomendado
{
  "icc": false,           // Inter-container communication off
  "no-new-privileges": true,
  "seccomp-profile": "/etc/docker/seccomp-profile.json",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 4. Buenas Prácticas para Contenedores

| Práctica | Por qué |
|----------|---------|
| `--user 1000:1000` | No correr como root dentro |
| `--read-only` | Filesystem de solo lectura |
| `--cap-drop ALL` | Eliminar capabilities innecesarias |
| `--network none` | Red isolada si no necesita |
| Imágenes oficiales | Menor superficie de ataque |
| Etiquetar imágenes | Versiones específicas (no `:latest`) |
| Scan de vulnerabilidades | Trivy, Clair, Snyk |

### 5. Protección del Daemon Docker

- **Solo usuarios de confianza** pueden controlar el daemon
- **No exponer API REST** sobre TCP sin TLS
- Usar **socket Unix** local por defecto
- Si API remota necesaria: HTTPS + certificados + VPN

### 6. Firewall con Docker

⚠️ **Docker bypassea ufw/firewalld**
- Docker manipula iptables directamente
- Crear reglas en la cadena **DOCKER-USER**
- O usar `--iptables=false` y manejar todo manualmente

---

## CADDY - Mejores Prácticas de Seguridad

### 1. Instalación

**Recomendado:** Instalar desde repositorio oficial Debian/Ubuntu
```bash
# Repositorio oficial
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install caddy
```

### 2. Configuración Básica Segura

```Caddyfile
# sil.albertofarah.com

sil.albertofarah.com {
    # Redirigir HTTP a HTTPS
    encode zstd gzip

    # Reverse proxy a contenedor Docker
    reverse_proxy localhost:8080 {
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }

    # Headers de seguridad
    header {
        X-Frame-Options "SAMEORIGIN"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
        Referrer-Policy "strict-origin-when-cross-origin"
        Content-Security-Policy "default-src 'self'"
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
    }

    # Rate limiting (opcional)
    rate-limit {
        zone {
            name static_files
            size 100
            expire 1s
        }
    }
}
```

### 3. HTTPS Automático

Caddy获取 certificados Let's Encrypt automáticamente:
- Requiere **email válido** (configurado al instalar)
- Dominio debe resolver a este servidor
- Puerto 80/443 accesibles públicamente

### 4. Configuración de Email para ACME

```bash
# En /etc/caddy/Caddyfile
{
    email admin@albertofarah.com
}
```

### 5. Hardening Adicional

| Header | Propósito |
|--------|-----------|
| X-Frame-Options | Previene clickjacking |
| X-Content-Type-Options | Previene MIME sniffing |
| X-XSS-Protection | Protección XSS legacy |
| Referrer-Policy | Controla información de referer |
| CSP | Content Security Policy |
| HSTS | Fuerza HTTPS |

### 6. Rate Limiting

Caddy tiene rate limiting básico integrado o usar módulo externo para más control.

---

## ARQUITECTURA PROPUESTA

```
Internet
    │
    │ Puerto 80, 443
    ▼
┌─────────────────┐
│     Caddy       │  ← Reverse proxy + HTTPS
│   (systemd)     │    - sil.albertofarah.com
└────────┬────────┘
         │ localhost:8080
         ▼
┌─────────────────┐
│  Docker Proxy   │  ← Red propia de Docker
│   Network       │    - Contenedores aislados
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────┐
│ App 1 │  │ App 2│
└──────┘  └──────┘
```

---

## LISTA DE VERIFICACIÓN PRE-INSTALACIÓN

### Servidor Base
- [ ] Ubuntu 24.04 LTS actualizado
- [ ] Firewall ufw configurado (solo SSH abierto inicialmente)
- [ ] Usuario sudo creado para operaciones
- [ ] SSH key-based authentication
- [ ] Fail2ban instalado

### Docker
- [ ] Instalar desde repositorio oficial Docker
- [ ] Configurar daemon.json con opciones seguras
- [ ] Crear usuario docker-admin (opcional)
- [ ] Configurar log rotation
- [ ] Definir política de imágenes confiables

### Caddy
- [ ] Instalar desde repositorio oficial
- [ ] Configurar email para Let's Encrypt
- [ ] Crear Caddyfile para sil.albertofarah.com
- [ ] Configurar dominio DNS para apuntar al servidor
- [ ] Probar HTTPS

### Redes
- [ ] Abrir puertos 80 y 443 en firewall
- [ ] Verificar que dominio resuelve correctamente
- [ ] Configurar DNS con registros A/AAAA

---

## FUENTES CONSULTADAS

- Docker Security Documentation: https://docs.docker.com/engine/security/
- Docker Rootless Mode: https://docs.docker.com/engine/security/rootless/
- Caddy Documentation: https://caddyserver.com/docs/
- Docker Daemon Security: https://docs.docker.com/engine/security/protect-access/
