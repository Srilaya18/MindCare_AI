# Software Configuration Management Plan (SCMP)
**Project Title:** AI-Assisted Community-Centric Mental Health Counseling Platform

## 1. Introduction
This document outlines the Software Configuration Management (SCM) practices governing the development of the AI-Assisted Mental Health Counseling Platform. This system analyzes text based on emotional state to provide preliminary mental health support and community resources.

## 2. Configuration Items (CIs)
The following files and components constitute the primary Configuration Items (CIs):
1. **Source Code**:
   - `app.py`: Contains the Flask server, routing logic, and the TextBlob integration for Natural Language Processing (stress level classification).
   - `templates/index.html`: The user interface constructed with a responsive Bootstrap 5 grid, dynamic JavaScript state handling, and interactive design.
2. **Dependencies/Build Scripts**:
   - `requirements.txt`: Records the specific Python package versions (Flask, TextBlob, Werkzeug) to ensure environments are identical.
3. **Documentation**:
   - `SCM_Project_Report.md`: This comprehensive SCM document tracking system architecture, tools, and change history.

*(Note: Database Schema and external Test Case scripts are considered optional and deferred to future release cycles).*

## 3. SCM Tools Used & Enhancements
- **Version Control:** Git (Local tracking engine).
- **Hosting & Collaboration:** GitHub (Remote tracking platform).
- **Continuous Integration (CI/CD):** GitHub Actions. Automatically tests the codebase on every push to `main`, ensuring no broken code reaches production.
- **Containerization (Environment SCM):** Docker. A `Dockerfile` guarantees that the application runs in identical environments everywhere.
- **Dependency Management:** `pip` / `requirements.txt`.
- **Automated Testing & Linting:** `pytest` (Unit testing CI) and `flake8` (Code standard enforcement CI).

## 4. SCM Activities
### 4.1. Version Control
The project's codebase and artifacts have been initialized within a Git repository. Every logical change is encapsulated in a commit containing a descriptive message of the update.

### 4.2. Change Control Process
Changes follow a basic workflow:
1. **Identification**: Need for change is identified (e.g., parameter tuning in NLP).
2. **Implementation**: Modifications applied to local codebase.
3. **Commit**: Changes integrated into the main repository branch (`git commit`).
4. **Verification**: Application is instantiated and tested locally before committing to production.

### 4.3. Configuration Audits
Audits ensure that the delivered platform behaves identically across environments. By locking package dependencies within `requirements.txt`, structural drift is avoided.

### 4.4. Build and Release Management
Releasing the software involves mapping the local branch to the production environment, typically executed via:
```sh
pip install -r requirements.txt
python app.py
```

## 5. Results & Outcomes
As outlined in the core requirements, the user can input concerns, and the background NLP system calculates polarity. Based on defined thresholds:
- Polarity < -0.2 => HIGH Stress Classification
- Polarity < 0.2 => MEDIUM Stress Classification
- Else => LOW Stress Classification

Using an automated dependency manager and robust Git timeline, the project is structured with 100% reproducibility.

## 6. Conclusion
Implementing rigorous SCM practices allows this AI-assisted mental health application to scale efficiently. Maintaining tight version control reduces regression bugs significantly when updating advanced configurations like TextBlob parameters or altering front-end aesthetics.
