# 🛡️ Magic File Scanner (Malware Detection Tool)

> A Python-based forensic tool that identifies file types by their raw hexadecimal signatures ("Magic Numbers"), detecting potential malware disguised with spoofed file extensions.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Security](https://img.shields.io/badge/Focus-Malware%20Analysis-red)
![CLI](https://img.shields.io/badge/Interface-CLI-green)

## 🧐 The Problem
One of the oldest tricks in the hacker playbook is **Extension Spoofing**. An attacker renames a malicious executable (`virus.exe`) to look like a harmless image (`vacation.jpg`) or a video (`movie.mp4`). Windows hides the extension by default, and users double-click the "image," infecting their machine.

## 💡 The Solution
**Magic File Scanner** ignores the file extension entirely. Instead, it reads the **File Header (Magic Bytes)**—the unique hexadecimal signature at the beginning of the file binary—to determine the *true* file type.

If a file claims to be a `.jpg` but has the hex signature of a Windows Executable (`4D 5A`), this tool triggers a **RED SECURITY ALERT**.

## ✨ Features
* **Hexadecimal Signature Analysis:** Reads raw binary headers to identify true file types.
* **Broad Format Support:**
    * **Images:** JPEG, PNG, GIF
    * **Documents:** PDF, ZIP, Office Docs (DOCX/XLSX)
    * **Executables:** Windows (EXE), Linux (ELF), Scripts (Shebang)
    * **Video:** MP4, MOV, MKV, WebM
* **Spoof Detection:** Automatically compares the detected "Real Type" vs. the "File Extension" to flag anomalies.
* **Dual-Engine Verification:** Uses Python's byte analysis + the system native `file` command (Linux/Mac/WSL) for double verification.

## 🚀 Installation & Usage

### Prerequisites
* Python 3.x
* (Optional) Linux, macOS, or WSL (Windows Subsystem for Linux) to use the secondary `file` command feature.

### Installation
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/magic-file-scanner.git](https://github.com/YOUR_USERNAME/magic-file-scanner.git)

# Navigate to directory
cd magic-file-scanner

Usage:

Run the script directly. It will launch an interactive dashboard.


SCREENSHOTS:

<img width="799" height="553" alt="Screenshot 2025-12-02 131252" src="https://github.com/user-attachments/assets/3074a2a1-1442-49f0-8636-60a0ebf8b79d" />


python magic_scanner.py


Follow the on-screen prompt to enter the path of the file you want to analyze.
