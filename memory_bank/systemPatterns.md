# System Patterns

This document outlines the architectural and design patterns used in the system.

---

## Architectural Patterns
- Modular design: separate GUI, file logic, and state management
- Event-driven updates: UI responds to folder selection changes to trigger live preview
- Single-file deployment: all logic and resources packaged for Windows with PyInstaller

## Design Patterns
- MVC (Model-View-Controller) pattern for GUI and logic separation
- Observer pattern for updating preview when folder selections change
- Use of threading or async for responsive UI during file scanning

## Rationale
- Modular and event-driven design ensures maintainability and responsiveness
- MVC and observer patterns help keep UI and logic decoupled, making enhancements easier
- Threading/async is considered to prevent UI freezing during file operations
- Toolkit selection is driven by the need for a modern look, ease of packaging, and no runtime dependencies 