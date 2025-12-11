# DevAgent Roadmap

## 🎯 Vision

DevAgent es un asistente de desarrollo AI reutilizable que aprende de cada interacción, mejorando continuamente su capacidad para ejecutar tareas de código. Diseñado para integrarse con cualquier proyecto y usar los créditos de Google AI Studio de manera eficiente.

---

## 📅 Phases

### Phase 0: Foundation ✅ (Completed)
> Core functionality working

- [x] CLI tool instalable via pip
- [x] Integración con Gemini API
- [x] Detección automática de contexto del proyecto
- [x] Knowledge base (rules, patterns, personas)
- [x] Operaciones de archivos (crear, modificar, eliminar)
- [x] Integración con Git (branch, commit)
- [x] Comando `devagent run` para ejecutar prompts
- [x] Comando `devagent context` para ver contexto
- [x] Comando `devagent rules` para listar reglas
- [x] Comando `devagent --dry` para preview
- [x] Script para listar modelos disponibles
- [x] Soporte para múltiples modelos (shortcuts: pro, flash, flash-lite)

---

### Phase 1: Usability & Documentation 🚧 (In Progress)
> Clarify existing features and improve user experience.

**Goal:** Ensure users understand how to use DevAgent effectively, especially regarding API keys and model selection.

- [x] Clarify in `README.md` that `GEMINI_API_KEY` uses AI Studio credits.
- [x] Improve `README.md` and CLI help text for the `--model` selection option.
- [ ] Add `devagent status` command to show current configuration (API key status, default model).
- [ ] Improve error handling and user feedback for common configuration issues.

**Deliverables:**
- Clearer documentation for core features.
- An easy way for users to verify their configuration.

---

### Phase 1.5: Enhanced History & Feedback 🎯 (Next)
> Learn from every execution

**Goal:** Guardar historial completo y permitir feedback para aprendizaje futuro.

#### 1.1 Enhanced History Storage
- [x] Guardar prompt original completo en `~/.devagent/projects/{project}/prompts/`
- [x] Guardar respuesta completa de Gemini en `~/.devagent/projects/{project}/responses/`
- [ ] Registrar tiempo de ejecución y tokens usados
- [ ] Guardar diff de archivos modificados (Pospuesto)
- [ ] Comando `devagent history --detailed` (Pospuesto)

#### 1.2 Feedback System
- [ ] Comando `devagent feedback good` - marcar última ejecución como exitosa
- [ ] Comando `devagent feedback bad --reason "..."` - marcar como fallida con razón
- [ ] Guardar feedback en `~/.devagent/projects/{project}/feedback.json`
- [ ] Mostrar resumen de feedback en `devagent history`

#### 1.3 Project Learnings
- [ ] Archivo `learnings.md` por proyecto con lecciones aprendidas
- [ ] Comando `devagent learnings` para ver/editar
- [ ] Auto-agregar learnings basados en feedback patterns

**Deliverables:**
- Historial completo con prompts y respuestas
- Sistema de feedback funcional
- Base para aprendizaje automático

---

### Phase 2: Auto-Learning & Patterns
> Improve automatically based on feedback

**Goal:** El agente mejora sus respuestas basándose en feedback histórico.

#### 2.1 Error Pattern Detection
- [ ] Detectar errores comunes en respuestas marcadas como "bad"
- [ ] Guardar en `~/.devagent/global/common_errors.json`
- [ ] Agregar advertencias al prompt cuando se detecten patrones similares
- [ ] Comando `devagent errors` para ver errores frecuentes

#### 2.2 Successful Patterns
- [ ] Identificar patrones en ejecuciones "good"
- [ ] Guardar en `~/.devagent/global/successful_patterns.json`
- [ ] Sugerir patterns similares para nuevas tareas

#### 2.3 Smart Prompt Enhancement
- [ ] Inyectar learnings relevantes al prompt automáticamente
- [ ] Agregar "Don't do X" basado en errores previos
- [ ] Agregar "Remember to Y" basado en éxitos previos

**Deliverables:**
- Detección automática de errores comunes
- Prompts mejorados basados en historial
- Knowledge base que crece con el uso

---

### Phase 3: Model Intelligence
> Use the right model for each task

**Goal:** Selección inteligente de modelo basada en tipo de tarea y presupuesto.

#### 3.1 Model Performance Tracking
- [ ] Registrar qué modelo se usó para cada tarea
- [ ] Correlacionar modelo con feedback (good/bad)
- [ ] Guardar en `~/.devagent/global/model_performance.json`

#### 3.2 Smart Model Selection
- [ ] Analizar tipo de tarea (simple fix vs complex feature)
- [ ] Sugerir modelo basado en complejidad y budget
- [ ] Flag `--auto-model` para selección automática
- [ ] Estimar costo antes de ejecutar

#### 3.3 Model Comparison
- [ ] Comando `devagent compare prompt.md --models flash,pro`
- [ ] Ejecutar mismo prompt con múltiples modelos
- [ ] Mostrar diff de respuestas
- [ ] Útil para evaluar nuevos modelos

**Deliverables:**
- Tracking de performance por modelo
- Selección inteligente de modelo
- Herramienta de comparación

---

### Phase 4: Advanced Features
> Power user capabilities

#### 4.1 Replay & Iterate
- [ ] Comando `devagent replay {task-id}` - re-ejecutar prompt anterior
- [ ] Comando `devagent retry --improve` - reintentar con ajustes automáticos
- [ ] Guardar versiones de archivos para rollback

#### 4.2 Template System
- [ ] Guardar prompts exitosos como templates
- [ ] Comando `devagent template save {name}`
- [ ] Comando `devagent template use {name} --vars key=value`
- [ ] Biblioteca de templates compartidos

#### 4.3 Multi-File Context
- [ ] Leer archivos existentes para mejor contexto
- [ ] Flag `--include src/types/*.ts` para agregar archivos al prompt
- [ ] Auto-detectar archivos relacionados

#### 4.4 Interactive Mode
- [ ] Comando `devagent chat` para modo conversacional
- [ ] Mantener contexto entre mensajes
- [ ] Útil para tareas iterativas

**Deliverables:**
- Sistema de replay y retry
- Templates reutilizables
- Mejor manejo de contexto

---

### Phase 5: Collaboration & Sharing
> Share knowledge across projects

#### 5.1 Export/Import Learnings
- [ ] Exportar learnings de un proyecto
- [ ] Importar learnings a otro proyecto
- [ ] Útil para proyectos similares

#### 5.2 Rule Generation
- [ ] Generar nuevas rules basadas en patterns exitosos
- [ ] Comando `devagent rules generate`
- [ ] Revisar y aprobar antes de agregar

#### 5.3 Statistics & Insights
- [ ] Dashboard de uso (tokens, costos, success rate)
- [ ] Comando `devagent stats`
- [ ] Exportar reportes

**Deliverables:**
- Learnings portables entre proyectos
- Generación automática de rules
- Analytics de uso

---

## 🏗️ Technical Debt & Improvements

### Code Quality
- [ ] Agregar tests unitarios
- [ ] Agregar tests de integración
- [ ] Type hints completos
- [ ] Documentación de API

### Error Handling
- [ ] Mejor manejo de errores de API
- [ ] Retry automático con backoff
- [ ] Logging estructurado

### Performance
- [ ] Cache de contexto de proyecto
- [ ] Lazy loading de knowledge base
- [ ] Async API calls

---

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Task success rate | > 80% |
| Average retry needed | < 1.5 |
| Time saved per task | > 50% vs manual |
| Cost per task | < $0.10 average |

---

## 🗓️ Timeline (Estimated)

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 0: Foundation | 1 day | ✅ Complete |
| Phase 1: Usability & Doc... | 1 day | 🚧 In Progress |
| Phase 1.5: History & Feed... | 2-3 days | 🎯 Next |
| Phase 2: Auto-Learning | 1 week | Planned |
| Phase 3: Model Intelligence | 1 week | Planned |
| Phase 4: Advanced Features | 2 weeks | Future |
| Phase 5: Collaboration | 2 weeks | Future |

---

## 💡 Ideas Backlog

Ideas para considerar en el futuro:

- [ ] Web UI para visualizar historial
- [ ] Integración con VS Code extension
- [ ] Webhook para notificaciones
- [ ] Soporte para otros LLMs (Claude API, OpenAI)
- [ ] Plugin system para extensiones
- [ ] Modo offline con modelos locales (Gemma, Llama)
- [ ] Integración con CI/CD
- [ ] Colaboración multi-usuario

---

## 📝 Notes

- Priorizar funcionalidad sobre perfección
- Cada phase debe ser usable de forma independiente
- Mantener backwards compatibility
- Documentar decisiones importantes

---

*Last updated: December 6, 2024*
