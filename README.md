# E-KYC System Using Computer Vision

An automated **Electronic Know-Your-Customer (E-KYC)** system designed to verify user identities securely. This project combines **Optical Character Recognition (OCR)** for document text extraction and **Biometric Facial Recognition** with **Liveness Detection** to prevent identity fraud.

---

## 🌟 Key Features

1. **ID Document Upload & Preview**: Supports uploading ID documents (Aadhaar Card, PAN Card, Drivers License, or Passports) with instant preview.
2. **AI-Powered OCR Extraction**: Automatically extracts user details like **Name**, **ID Number**, and **Date of Birth (DOB)** from the uploaded ID card using EasyOCR.
3. **Interactive Biometric Liveness Detection**: Employs client-side face landmark tracking. The user must perform a liveness proof (blinking twice) to ensure they are a real person and not a photo/video spoof.
4. **Facial Comparison & Matching**: Extracts the profile picture from the uploaded ID card and compares it with the live-captured face using deep representation vectors (face recognition) to check if they match.
5. **Clearance Registration**: Automatically saves successfully verified user credentials into a local SQLite database for KYC records.

---

## 🛠️ Technology Stack

* **Backend Framework**: Python (Flask)
* **Database**: SQLite (SQLAlchemy ORM)
* **Computer Vision & Deep Learning**:
  * **Face Detection & Landmarks**: MediaPipe (Client-side)
  * **Face Recognition**: `face_recognition` (wraps `dlib` ResNet)
  * **Optical Character Recognition (OCR)**: `EasyOCR` (PyTorch-based)
  * **Image Processing**: OpenCV, Pillow
* **Frontend**: HTML5, Vanilla CSS, Tailwind CSS, Javascript (ES Modules)

---

## 📂 Project Folder Structure

```text
Ekyc_system_using_computer_vision/
│
├── app.py                      # Main Flask application entry point
├── config.py                   # Configuration settings
├── ekyc.db                     # SQLite database file (generated automatically)
├── requirements.txt            # Python library dependencies
├── package.json                # npm configuration for Tailwind CSS compiling
│
├── database/                   # Database models and session setup
│   ├── database.py             # SQLite engine setup and database initializer
│   └── models.py               # SQLAlchemy schema definition for Registered Users
│
├── routes/                     # Flask Routing Blueprints
│   ├── __init__.py             # Route registrations
│   ├── home.py                 # Landing page route
│   └── verification.py         # Verification API and view endpoints
│
├── services/                   # Backend Computer Vision Core Services
│   ├── face/                   # Face Recognition sub-module
│   │   ├── detector.py         # Detects and crops faces in images
│   │   ├── matcher.py          # Matches live face vs. ID face (vector distance)
│   │   └── face_service.py     # Main coordinator for face verification
│   │
│   ├── ocr/                    # OCR Extraction sub-module
│   │   ├── ocr_engine.py       # Invokes EasyOCR engine
│   │   ├── preprocessor.py     # Image binarization/rotation checks for better text accuracy
│   │   └── ocr_service.py      # Main coordinator for document OCR extraction
│   │
│   ├── upload/                 # Helper services for temporary file handling
│   └── verification/           # KYC workflow state coordinator
│
├── templates/                  # Jinja2 HTML Layout Templates
│   ├── base.html               # Main base template containing shared layout and backgrounds
│   ├── index.html              # Landing page dashboard
│   └── verification.html       # Step-by-step KYC verification page
│
├── static/                     # Frontend Static Assets
│   ├── css/
│   │   └── output.css          # Tailwind compiled stylesheet
│   └── js/
│       ├── verification.js     # Orchestrates face scanning, liveness loops, and backend submit
│       ├── camera/             # Camera start/stop helpers
│       ├── mediapipe/          # MediaPipe landmarker and Eye-Aspect-Ratio blink detector
│       └── upload/             # Drag-and-drop ID upload controller
│
├── uploads/                    # Stores uploaded document files & captured biometric faces
└── tests/                      # Testing suites
```

---

## 💻 Installation & Setup Guide

Follow these steps to set up and run the project locally on your machine.

### Prerequisites

Ensure you have the following installed:
* [Python 3.10 or 3.11](https://www.python.org/downloads/) (Recommended versions for compatibility with `dlib`)
* [Node.js & npm](https://nodejs.org/en) (For Tailwind compilation)
* **Windows Users only**: [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with the **"Desktop development with C++"** workload selected. This is **strictly required** to compile the C++ `dlib` library during dependency installation.

---

### Step-by-step Setup

#### 1. Clone the Project Repository
```bash
git clone https://github.com/manojhp24/e-KYC_using_computer_vision.git
cd e-KYC_using_computer_vision
```

#### 2. Set Up a Python Virtual Environment
Creating a virtual environment ensures that the python dependencies do not conflict with other system libraries.
```bash
# Create the environment
python -m venv .venv

# Activate the environment:
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

#### 3. Install Python Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
*(Note: Installing `dlib` may take a few minutes as it compiles libraries locally. Make sure your Visual Studio compiler is installed if on Windows.)*

#### 4. Install Node.js Packages & Build CSS
Tailwind CSS styles are configured via npm. Build the stylesheet by running:
```bash
# Install npm dependencies
npm install

# Start CSS compiler watcher in a separate terminal:
npm run watch
```

#### 5. Launch the Application
Run the Flask server:
```bash
flask run
```
By default, the server will start running at: **`http://127.0.0.1:5000/`**

---

## 🚀 How to Use

1. Open your browser and navigate to `http://127.0.0.1:5000/`.
2. Click **Start Identity Verification** to open the verification flow.
3. **Step 1: ID Upload**:
   * Click the ID Card Document container or drag-and-drop a photo of your ID Card.
   * You should see a preview of the document.
4. **Step 2: Biometric Liveness check**:
   * Allow browser camera permissions when prompted.
   * Position your face inside the scanner frame.
   * Look directly at the camera and blink **two times** clearly.
   * Once successfully checked, the liveness engine will lock, crop your face, and start verifying.
5. **Step 3: Verification Results**:
   * A loading window will appear while the backend processes OCR and matches faces.
   * If matched, the **Verification Result Card** will appear showing your extracted details (Name, DOB, ID Number) and confirmation badge.
