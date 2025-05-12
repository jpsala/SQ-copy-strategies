# Tasks

This document is the single source of truth for all task tracking in the project.

---

## Backlog
(List all tasks that are planned but not yet started.)

## In Progress
(List all tasks currently being worked on.)

## Completed
(List all completed tasks.)

## Active Enhancements
- Copy strategies - In Progress

## Enhancement Details
### Copy strategies Enhancement

**Status**: In Progress
**Priority**: High
**Estimated Effort**: Medium

### Description
Develop a Python GUI application that copies files from the 'spp' folder (if they also exist in 'real-tick') to the 'final' folder. The app must allow the user to select the three folders, provide a simple interface, and be packaged as a single executable for Windows 10/11 with no dependencies required for the end user.

### Requirements
- User can select any folder to act as 'real-tick', 'spp', and 'final'
- Only files present in both 'spp' and 'real-tick' are copied to 'final', from the folder selected as 'real-tick'
- Simple, intuitive GUI for folder selection and operation
- Options has to be saved and restored on next run
- Runs on Windows 10/11 as a single .exe (no Python or dependencies required for user)
- No external dependencies required at runtime
- Create an python environment and use it to build the app

### Subtasks
- [x] Review Python GUI options for no-dependency packaging (e.g., Tkinter)
- [x] Design simple GUI for folder selection and copy action
- [ ] Implement logic to compare and copy files from 'spp' to 'final' if also in 'real-tick'
- [ ] Add error handling and user feedback
- [ ] Test on Windows 10 and 11
- [x] Package app as a single .exe (e.g., using PyInstaller)
- [x] Verify no dependencies required for end user
- [x] GUI with folder selection and Start Copy button
- [ ] Implement storing and restoring folder selections (options) on app start/exit
- [ ] Prepare minimal user instructions

### Dependencies
- Python 3.x (for development)
- Tkinter (standard library)
- PyInstaller (for packaging)

### Notes
- The app must be extremely simple to use
- No installation or configuration required for the end user
- All logic must be compatible with Windows file paths

## Completed Enhancements

## Planned Features

### Modernized GUI & Live Preview Enhancement

**Status**: Complete
**Priority**: High
**Estimated Effort**: High

#### Description
Upgrade the application with a modern, user-friendly GUI and add a dynamic preview feature that shows which files will be copied whenever any folder location is changed. The preview updates in real time as the user selects different folders.

#### Complexity
Level: 3 (Intermediate Feature)
Type: Enhancement

#### Requirements
- [x] Modern, visually appealing GUI (beyond default Tkinter look)
- [x] Dynamic preview of files to be copied, updating on any folder change
- [x] All previous requirements for folder selection, copy logic, and packaging still apply
- [x] Must remain a single-file Windows executable with no runtime dependencies

#### Components Affected
- GUI (main window, folder selection, preview area)
- File comparison logic (triggered on folder change)
- State management (to track folder selections and preview state)

#### Design Decisions
- Architecture:
  - [x] Evaluate advanced Tkinter (ttk, customtkinter) or alternative (PySimpleGUI, PyQt, etc.)
  - [x] Ensure compatibility with PyInstaller for single-file build
- UI/UX:
  - [x] Design a modern layout with clear folder selectors and a preview pane
  - [x] Add icons, better spacing, and visual feedback
- Algorithms:
  - [x] Efficiently scan and compare folders on change without UI freezing

#### Implementation Strategy
1. Research and select GUI toolkit/approach
2. Prototype modernized GUI layout
3. Implement folder selection and preview update logic
4. Integrate preview area into main window
5. Optimize file comparison for responsiveness
6. Ensure all features work with PyInstaller packaging
7. User testing and feedback

#### Testing Strategy
- [x] Unit tests for file comparison logic
- [x] Manual tests for GUI responsiveness and preview accuracy
- [x] Integration test: end-to-end folder selection and preview
- [x] User acceptance test on Windows 10/11

#### Documentation Plan
- [x] Update user instructions for new GUI and preview
- [x] Document design decisions and toolkit selection

#### Creative Phases Required
- [x] 🎨 UI/UX Design
- [x] 🏗️ Architecture Design (if new toolkit chosen)
- [x] ⚙️ Algorithm Design (if new preview logic is complex)

#### Dependencies
- Python 3.x (for development)
- Tkinter/ttk or alternative GUI library (must be compatible with single-file build)
- PyInstaller (for packaging)

#### Challenges & Mitigations
- Modern look in Tkinter is limited: consider ttk, customtkinter, or PySimpleGUI
- Real-time preview may slow UI: use threading or async updates
- Packaging with PyInstaller: test early with chosen GUI library
- Maintain no-runtime-dependency requirement: avoid libraries that require external installs

#### Completion Note
This session delivered a robust, user-friendly, persistent, and accurate file copy tool with a modern GUI and live preview, meeting all requirements and user experience goals.

## Completed Enhancements

## Planned Features

### Modernized GUI & Live Preview Enhancement

**Status**: Planning
**Priority**: High
**Estimated Effort**: High

#### Description
Upgrade the application with a modern, user-friendly GUI and add a dynamic preview feature that shows which files will be copied whenever any folder location is changed. The preview updates in real time as the user selects different folders.

#### Complexity
Level: 3 (Intermediate Feature)
Type: Enhancement

#### Requirements
- [ ] Modern, visually appealing GUI (beyond default Tkinter look)
- [ ] Dynamic preview of files to be copied, updating on any folder change
- [ ] All previous requirements for folder selection, copy logic, and packaging still apply
- [ ] Must remain a single-file Windows executable with no runtime dependencies

#### Components Affected
- GUI (main window, folder selection, preview area)
- File comparison logic (triggered on folder change)
- State management (to track folder selections and preview state)

#### Design Decisions
- Architecture:
  - [ ] Evaluate advanced Tkinter (ttk, customtkinter) or alternative (PySimpleGUI, PyQt, etc.)
  - [ ] Ensure compatibility with PyInstaller for single-file build
- UI/UX:
  - [ ] Design a modern layout with clear folder selectors and a preview pane
  - [ ] Add icons, better spacing, and visual feedback
- Algorithms:
  - [ ] Efficiently scan and compare folders on change without UI freezing

#### Implementation Strategy
1. Research and select GUI toolkit/approach
2. Prototype modernized GUI layout
3. Implement folder selection and preview update logic
4. Integrate preview area into main window
5. Optimize file comparison for responsiveness
6. Ensure all features work with PyInstaller packaging
7. User testing and feedback

#### Testing Strategy
- [ ] Unit tests for file comparison logic
- [ ] Manual tests for GUI responsiveness and preview accuracy
- [ ] Integration test: end-to-end folder selection and preview
- [ ] User acceptance test on Windows 10/11

#### Documentation Plan
- [ ] Update user instructions for new GUI and preview
- [ ] Document design decisions and toolkit selection

#### Creative Phases Required
- [x] 🎨 UI/UX Design
- [ ] 🏗️ Architecture Design (if new toolkit chosen)
- [ ] ⚙️ Algorithm Design (if new preview logic is complex)

#### Dependencies
- Python 3.x (for development)
- Tkinter/ttk or alternative GUI library (must be compatible with single-file build)
- PyInstaller (for packaging)

#### Challenges & Mitigations
- Modern look in Tkinter is limited: consider ttk, customtkinter, or PySimpleGUI
- Real-time preview may slow UI: use threading or async updates
- Packaging with PyInstaller: test early with chosen GUI library
- Maintain no-runtime-dependency requirement: avoid libraries that require external installs 