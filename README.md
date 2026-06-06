# AeroShield Twin - National Hackathon Project

**AI-Powered Cybersecurity Digital Twin for Aircraft Systems**

An advanced cybersecurity platform that detects, classifies, and mitigates cyber threats to aircraft systems using artificial intelligence and digital twin visualization.

## 🎯 Project Overview

AeroShield Twin is a comprehensive solution for monitoring and protecting software-defined aircraft systems from cyber threats. It uses:

- **AI Anomaly Detection** - Isolation Forest algorithm to detect abnormal aircraft behavior
- **Rule-Based Threat Classification** - Identifies threat types (GPS Spoofing, Sensor Anomalies, etc.)
- **Digital Twin Visualization** - Real-time visualization of aircraft subsystem health
- **Impact Prediction Engine** - Estimates operational consequences of threats
- **Mitigation Recommendations** - Suggests and applies protective actions
- **Incident Reporting** - Generates comprehensive incident reports

## ✨ Core Features

### 1. **Digital Twin Visualization**
- Real-time display of 5 aircraft subsystems (Navigation, Flight Control, Communication, Engine, Sensors)
- Color-coded health status (Green/Yellow/Red)
- Individual risk scores and impact levels
- Overall aircraft health assessment

### 2. **AI-Powered Threat Detection**
- Isolation Forest anomaly detection model
- Trained on normal aircraft operational patterns
- Real-time anomaly scoring and confidence metrics

### 3. **Threat Classification Engine**
- Rule-based classification system
- Identifies 5 threat categories: GPS Spoofing, Sensor Anomalies, Communication Anomalies, Network Intrusion, Unknown

### 4. **Attack Simulation**
- Simulate GPS Spoofing, Sensor Anomalies, and Network Intrusions
- Adjustable severity levels

### 5. **Impact Prediction**
- Predicts operational consequences of threats
- Estimates affected subsystems and risk progression

### 6. **Mitigation Recommendation Engine**
- Threat-specific mitigation actions
- Risk reduction calculations

### 7. **Incident Timeline**
- 5-stage incident progression: Normal → Attack → Detection → Prediction → Mitigation → Resolution

### 8. **Report Generation**
- JSON incident reports with optional PDF export

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│      React Frontend (Vite + Tailwind)   │
│  - Digital Twin Visualization           │
│  - Real-time Threat Monitoring          │
│  - Attack Simulation Controls           │
│  - Incident Timeline                    │
└───────────────┬─────────────────────────┘
                │ REST API
                ▼
┌─────────────────────────────────────────┐
│    FastAPI Backend (Python)             │
│  - Data Stream Simulation               │
│  - Anomaly Detection (Isolation Forest) │
│  - Threat Classification (Rules)        │
│  - Impact Prediction & Mitigation       │
│  - Report Generation                    │
└─────────────────────────────────────────┘
```

## 📋 System Requirements

### Backend
- **Python 3.9+**
- **FastAPI 0.104+**
- **Scikit-Learn 1.3+**
- **Pandas 2.0+**
- **NumPy 1.24+**

### Frontend
- **Node.js 16+**
- **npm 8+**
- **React 18+**
- **Vite 5+**
- **Tailwind CSS 3+**

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Train the anomaly detection model (1-2 minutes)
python train_model.py

# Start the backend server
python run.py
```

Backend runs at `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### Frontend Setup (in another terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at `http://localhost:3000`

## 🎬 Demo Workflow

1. **Open Dashboard** - `http://localhost:3000`
2. **Monitor Normal State** - Aircraft starts healthy
3. **Trigger Attack** - Click "🛰️ GPS Spoofing" button
4. **Observe Detection** - AI detects anomalies automatically
5. **Review Recommendations** - Mitigation suggestions appear
6. **Apply Mitigation** - Click mitigation button
7. **Monitor Recovery** - Watch risk score decrease
8. **Generate Report** - Click "End Incident & Generate Report"

## 📁 Key Files

```
backend/
├── app/main.py                  # FastAPI app
├── app/config/
│   ├── threat_rules.json        # Threat classification
│   ├── mitigations.json         # Mitigation library
│   └── impact_rules.json        # Impact prediction
├── app/ml/
│   ├── anomaly_detector.py      # Isolation Forest
│   ├── threat_classifier.py     # Threat classification
│   └── model_trainer.py         # Training script
└── requirements.txt

frontend/
├── src/components/
│   ├── Dashboard.jsx            # Main layout
│   ├── DigitalTwin.jsx          # Aircraft visualization
│   ├── ThreatPanel.jsx          # Threat display
│   ├── ImpactPanel.jsx          # Risk analysis
│   ├── RecommendationPanel.jsx  # Mitigations
│   ├── ControlPanel.jsx         # Attack buttons
│   └── IncidentTimeline.jsx     # Timeline
└── package.json
```

## 🔌 API Endpoints

- `GET /systems` - Aircraft system status
- `GET /digital-twin` - Full digital twin state
- `GET /alerts` - Current anomaly alerts
- `POST /simulate/gps-spoof` - GPS spoofing simulation
- `POST /simulate/sensor-attack` - Sensor anomaly simulation
- `POST /simulate/network-attack` - Network intrusion simulation
- `POST /stop-attack` - Stop attack
- `GET /recommendations` - Mitigation recommendations
- `POST /apply-mitigation` - Apply mitigation action
- `POST /end-incident` - End incident & generate report
- `GET /report` - Get incident report
- `GET /incident-history` - Past incidents

## 🧠 Machine Learning

**Anomaly Detection**: Isolation Forest
- Training data: 2000 synthetic aircraft measurements
- Features: 10 (subsystem values + risk scores)
- Detection latency: < 1 second

**Threat Classification**: Rule-based
- Patterns → Threat types
- Confidence scoring

## 📊 Performance

| Component | Target |
|-----------|--------|
| Anomaly Detection | < 1s |
| Threat Classification | < 200ms |
| API Response | < 100ms |
| Update Frequency | 1.5s |

## 🛣️ Future Enhancements

- WebSocket for real-time updates
- Autoencoder anomaly detection
- Real GPS spoofing dataset integration
- 3D aircraft visualization
- Multi-aircraft monitoring
- Database integration

## 🎯 Quick Reference

```bash
# Start Backend
cd backend
python train_model.py  # First time only
python run.py

# Start Frontend (new terminal)
cd frontend
npm install  # First time only
npm run dev
```

**API Documentation**: `http://localhost:8000/docs`

---

**AeroShield Twin v1.0.0** - Built for National Hackathon 🚀