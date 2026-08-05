

# claudops

> Plantilla de flujo de trabajo universal para Claude Code — clónala, ejecuta `/setup`, y comienza a desarrollar

**Autor:** [@alexandrbasis](https://x.com/alexandrbasis) | [@MishkaKey](https://x.com/MishkaKey)

[![Live Site](https://img.shields.io/badge/Live_Site-claudops-0d9488?style=flat-square)](https://alexandrbasis.com/claudops/workflows/)

<a href="https://alexandrbasis.com/claudops/workflows/">
  <img src="docs/workflow-overview.png" alt="Claudops AI Development Pipeline — 7 stages from feature discovery to deployment" width="100%">
</a>

---

Una carpeta `.claude/` probada en producción que puedes insertar en **cualquier** base de código. Incluye agentes, habilidades (skills), hooks y un asistente de configuración que ajusta automáticamente todo para que coincida con tu pila tecnológica.

Funciona con cualquier lenguaje, framework y arquitectura: TypeScript, Python, Go, Ruby, Java y más.

## Filosofía

Este es un **pipeline con humano en el bucle**, no un agente completamente autónomo. Cada etapa es iniciada por ti y cada salida es validada por ti. La IA propone; tú apruebas, ajustas o rechazas. Nada se despliega sin tu aprobación explícita.

- **Tú inicias** cada etapa: `/nf` para descubrimiento, `/ct` para planificación, `/si` para implementación, `/sr` para revisión
- **Tú validas** entre etapas: revisa el documento de descubrimiento antes de planificar, revisa el plan antes de programar
- **Tú controlas los puntos de control**: las verificaciones de calidad se ejecutan automáticamente, pero la fusión (merge) siempre es tu decisión
- **Los agentes asisten, no reemplazan**: 17 agentes se encargan del trabajo tedioso (linting, pruebas, verificaciones de arquitectura), tú tomas las decisiones

El resultado: velocidad de la IA con criterio humano. Contexto completo en cada paso, sin automatización de caja negra.

## Características destacadas

- **Asistente `/setup`**: detecta automáticamente tu pila tecnológica, estructura del proyecto y comandos, luego configura todas las habilidades, agentes y hooks en un solo paso
- **`/update-setup`**: descarga los cambios del repositorio principal de claudops, muestra las diferencias y te permite seleccionar actualizaciones específicas mientras conserva tus personalizaciones locales
- **17 agentes especializados**: TDD, revisión de código, validación de tareas e investigación
- **31 habilidades (skills)**: ciclo de vida completo de desarrollo, monitoreo del servidor de desarrollo y asistentes multi-IA (Gemini CLI, Codex CLI, Cursor CLI)
- **Composabilidad Skills ↔ Agentes**: los agentes precargan habilidades de convenciones compartidas mediante el frontmatter `skills:`
- **Revisión de planes multi-IA**: verificación opcional de planes con Gemini (ver `review-plan-gemini.sh`)
- **Hooks**: lint al escribir, sincronización, validación, protecciones y métricas
- **Integración con Linear**: gestión de proyectos desde tu terminal (habilidad `cc-linear`)

---

## Contenido

### Agentes (17)

**Automatización** (`.claude/agents/automation-agents/`)
| Agente | Propósito |
|-------|---------|
| `automated-quality-gate` | Ejecuta lint, verificación de tipos y pruebas antes de la revisión |
| `developer-agent` | Agente universal para elementos de trabajo acotados |
| `integration-test-runner` | Ejecución de pruebas E2E e integración |
| `senior-architecture-reviewer` | Revisa el enfoque, la arquitectura y el cumplimiento de TDD |

**Revisión de código** (`.claude/agents/code-review-agents/`)
| Agente | Enfoque |
|-------|-------|
| `code-quality-reviewer` | SOLID, mantenibilidad, olores a código |
| `documentation-accuracy-reviewer` | Completitud y precisión de la documentación |
| `performance-reviewer` | Consultas N+1, caché y optimización |
| `security-code-reviewer` | OWASP Top 10, inyección y problemas de autenticación |
| `spec-compliance-reviewer` | Alineación con especificaciones y requisitos |
| `test-coverage-reviewer` | Brechas de cobertura y calidad de pruebas |

**Validadores de tareas** (`.claude/agents/tasks-validators-agents/`)
| Agente | Propósito |
|-------|---------|
| `plan-reviewer` | Validación de planes técnicos |
| `task-splitter` | Evalúa si una tarea necesita desglose |
| `task-decomposer` | Estructura de fases para tareas divididas |

**Flujo de trabajo** (`.claude/agents/wf-agents/`)
| Agente | Propósito |
|-------|---------|
| `changelog-generator` | Genera registro de cambios desde la documentación de tareas |
| `create-pr-agent` | Automatización de PR con integración de Linear |
| `docs-updater` | Sincronización de documentación |

**Ayudantes** (`.claude/agents/helpful-agents/`)
| Agente | Propósito |
|-------|---------|
| `comprehensive-researcher` | Tareas de investigación profunda |

---

### Habilidades (Skills) (31)

Consulta [`.claude/skills/README.md`](.claude/skills/README.md) para el índice completo. Resumen:

| Área | Ejemplos |
|------|----------|
| Configuración y convenciones | `setup`, `update-setup`, `coding-conventions`, `review-conventions` |
| Flujo principal | `ct`, `si`, `si-quick`, `sr`, `prc`, `ph`, `nf`, `product`, `vp`, `blueprint` |
| Descubrimiento y diseño | `brainstorm`, `design-exploration`, `analyze`, `grill-me`, `rip` |
| Calidad y depuración | `dev-server`, `code-analysis`, `dbg`, `fci` |
| Multi-IA | `gemini-cli`, `codex-cli`, `cursor-cli` |
| Integraciones y metadatos | `cc-linear`, `deep-research`, `parallelization`, `sbs`, `update-docs` |

---

### Composabilidad Skills ↔ Agentes

Los agentes de revisión y el agente de desarrollo precargan habilidades de convenciones compartidas mediante el frontmatter `skills:`, sin duplicación por agente:

```yaml
# In agent frontmatter
skills:
  - review-conventions   # preloaded into all 7 review agents
  - coding-conventions   # preloaded into developer-agent
```

El asistente `/setup` llena estas habilidades de convenciones con la pila tecnológica de tu proyecto, las reglas de arquitectura y los comandos. Cada agente las hereda automáticamente.

---

### Revisión de planes multi-IA

Flujo opcional cuando Gemini CLI está configurado: consulta `.claude/scripts/review-plan-gemini.sh` y la configuración de hooks en `.claude/settings.json`.

**Lo que Gemini puede verificar:** seguridad, arquitectura, rendimiento, casos extremos y capacidad de prueba.

---

### Hooks

Hooks en Python/shell bajo `.claude/hooks/`: lint al escribir, sincronización de agentes, verificaciones pre-commit, protecciones bash/archivo, seguimiento de costos, etc. Detalles: [`.claude/hooks/README.md`](.claude/hooks/README.md).

---

## Estructura del repositorio

```
.claude/
├── agents/           # Specialized subagents
├── docs/
│   ├── templates/    # PRD, JTBD, decomposition, review templates
│   └── references/
├── hooks/            # Claude Code hooks (see hooks/README.md)
├── scripts/          # e.g. review-plan-gemini.sh, linear-api.sh
├── skills/           # Slash-command skills (see skills/README.md)
└── settings.json     # Hook and project settings (copy & customize)

workflow-visualization.html   # Interactive workflow map (open in browser)
```

---

## Inicio rápido

### 1. Clonar en tu proyecto
```bash
git clone https://github.com/alexandrbasis/claudops.git
cp -r claudops/.claude your-project/
cd your-project
```

### 2. Ejecutar el asistente de configuración
```
/setup
```

El asistente hará lo siguiente:
1. **Escaneará tu base de código** con 3 agentes en paralelo (pila tecnológica, estructura del proyecto, comandos)
2. **Confirmará** contigo los valores detectados (framework, ORM, comandos de prueba/lint/construcción, arquitectura)
3. **Completará** todas las variables `{{PLACEHOLDER}}` directamente en cada archivo de habilidad, agente y hook

Tras la configuración, cada archivo tendrá tus valores reales integrados: sin resolución en tiempo de ejecución, sin indirección de configuración.

### 3. Mantenerlo actualizado
```
/update-setup
```

Descarga los últimos cambios del repositorio principal de claudops, muestra qué hay de nuevo o modificado y te permite seleccionar qué aplicar. Tus habilidades y hooks locales personalizados nunca se modifican.

### 4. Comenzar a usar los flujos de trabajo
```
/ct    — create a technical decomposition
/si    — start implementation from a task
/sr    — run multi-agent code review
```

### Seleccionar habilidades individuales
```bash
cp -r claudops/.claude/skills/si your-project/.claude/skills/
cp claudops/.claude/scripts/review-plan-gemini.sh your-project/.claude/scripts/
```

### Como referencia
Estudia los patrones y adáptalos a tus propios flujos de trabajo.

---

## Flujos de trabajo clave

### Pipeline TDD
```
/ct → /si → automated-quality-gate → senior-architecture-reviewer
```

### Revisión de código multi-agente
```
code-quality + security + performance + test-coverage + documentation
```

### Flujo orientado a tareas
```
/ct → /si → /sr → /prc → merge
```

### Multi-IA
- Gemini CLI: revisión de planes, investigación basada en web
- Codex / Cursor CLI: revisión de segunda opinión (ver plantilla `cross-ai-protocol`)

---

## Requisitos previos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado
- Git + GitHub CLI (`gh`)
- Opcional: Gemini CLI (`npm i -g @google/gemini-cli`)
- Opcional: Acceso a la API de Linear

---

## Seguridad y privacidad

**No incluidos (sensibles):** `settings.local.json`, claves API, credenciales MCP, archivos de registro

**Seguros para compartir:** Agentes, habilidades, scripts de hooks y plantillas en este repositorio (excluye las sobrescrituras locales)

---

## Contribuir

¿Encontraste un patrón mejor? ¿Tienes sugerencias?
- Abre un issue con tu idea
- Comparte tus propios flujos de trabajo
- Contribuye con mejoras mediante PR

---

## Licencia

MIT — Ver [LICENSE](LICENSE)
