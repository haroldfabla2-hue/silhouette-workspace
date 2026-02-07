# TASKS.md - Auto-Researcher v1.0

*Última actualización: 2026-02-07 02:50*

---

## 🛡️ Flocky v4.0 - COMPLETADO ✅

| Tarea | Estado |
|-------|--------|
| Implementar supervisor externo | ✅ Completo |
| Sistema de snapshots | ✅ Funcionando |
| IA MiniMax integrada | ✅ Analizando errores |
| Auto-restore con verificación | ✅ Verificado |
| Test automatizado | ✅ Configurado |
| Cron diario (6 AM) | ✅ Listo |

---

## 🤖 Auto-Researcher v1.0 - EN PROGRESO

### ✅ FASE 1: Foundation - COMPLETA
| Componente | Estado | Notas |
|-----------|--------|-------|
| Estructura del skill | ✅ | `/skills/auto-researcher/` |
| SKILL.md | ✅ | Documentación completa |
| research.py | ✅ | Pipeline principal |
| research_core.py | ✅ | Funciones core |
| glm-wrapper.py | ✅ | Wrapper Z.AI GLM |
| image-prompts.md | ✅ | Prompts especializados |

### ✅ FASE 2: Image Generation (Z.AI GLM) - COMPLETA
| Componente | Estado | Herramienta |
|-----------|--------|-------------|
| Infographics | ✅ | glm-image.py |
| Slides | ✅ | glm-image.py |
| Drive Upload | ✅ | glm-workflow.py |

### ⏳ FASE 3: Google Workspace - USA EXISTENTE
| Componente | Estado | Herramienta |
|-----------|--------|-------------|
| Google Docs | ✅ USA gog | `gog docs create` |
| Google Sheets | ✅ USA gog | `gog sheets create` |
| Drive Images | ✅ USA GLM | `glm-workflow.py` |

### 🔜 FASE 4: PDF Generation - PENDIENTE
- [ ] Testear ReportLab
- [ ] Crear templates PDF

### 🔜 FASE 5: Automation - PENDIENTE
- [ ] Cron para reports automáticos
- [ ] Templates por tipo

---

## 📁 Archivos Creados

```
auto-researcher/
├── SKILL.md                    # Documentación principal
├── scripts/
│   ├── research.py            # Pipeline principal
│   └── research_core.py       # Funciones core
├── references/
│   └── image-prompts.md       # Prompts para imágenes
└── assets/
    └── (templates, logos, etc.)
```

---

## 📋 Comandos de Uso

```bash
# Quick research + PDF
python3 scripts/research.py --query "AI trends 2024" --type brief --pdf

# Full analysis
python3 scripts/research.py --query "competitor analysis" --type analysis --all

# Daily brief
python3 scripts/research.py --query "news today" --type brief --pdf --images 2
```

---

## 🛠️ Dependencias

| Componente | Estado | Ubicación |
|-----------|--------|-----------|
| **web_search** | ✅ Built-in | Brave API |
| **web_fetch** | ✅ Built-in | OpenClaw tool |
| **MiniMax** | ✅ Integrada | Flocky |
| **openai-image-gen** | ✅ Ready | /usr/lib/node_modules/ |
| **gog** | ✅ Ready | Google Workspace |
| **ReportLab** | ✅ Instalado | Python library |

---

## 🎯 Próximos Pasos

1. **Probar script** con un query simple
2. **Integrar APIs** que faltan (gog, image-gen)
3. **Testear PDF** generation
4. **Crear templates** para diferentes tipos

---

## 📊 Dependencias del Sistema

| Skill/API | Estado | Uso |
|-----------|--------|-----|
| **openai-whisper-api** | ✅ Ready | STT (OpenAI API) |
| **google-tts** | ✅ Ready | TTS (Google Cloud) |
| **gog** | ✅ Ready | Google Workspace |
| **openai-image-gen** | ✅ Ready | Generación de imágenes |
| **web_search** | ✅ Ready | Brave Search |
| **web_fetch** | ✅ Ready | Extracción web |
| **MiniMax** | ✅ Ready | IA Analysis |
| **ReportLab** | ✅ Ready | PDF Generation |

---

*Para continuar: Probar FASE 1 ( Foundation) *
