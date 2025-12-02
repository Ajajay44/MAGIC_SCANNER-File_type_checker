import os
import sys
import binascii
import subprocess
import shutil

# --- CONFIGURATION: The Magic Database ---
MAGIC_NUMBERS = {
    # Images
    "FFD8FF": "JPEG Image",            # Common prefix for both JFIF (E0) and Exif (E1)
    "89504E47": "PNG Image",
    "47494638": "GIF Image",
    "424D": "BMP Bitmap",
    "49492A00": "TIFF Image (Little Endian)",
    "4D4D002A": "TIFF Image (Big Endian)",
    
    # Audio/Video
    "494433": "MP3 Audio",
    "2E524D46": "RealMedia",
    "57415645": "WAV Audio",          # Often appears after 'RIFF' header
    
    # Documents & Archives
    "25504446": "PDF Document",
    "504B0304": "ZIP Archive / Office Doc (docx/xlsx)", 
    "1F8B": "GZIP Compressed File",
    "425A": "BZIP Compressed File",
    "75737461": "TAR Archive",        # 'usta' - often at offset 257, but checking prefix helps
    
    # Executables
    "4D5A": "Windows Executable (EXE/DLL)",
    "7F454C46": "Linux Executable (ELF)",
    "CAFEBABE": "Java Class File",     # Classic signature
    #video files
    "0000001866747970": "MP4 Video",       # Common (Canon, etc)
    "0000002066747970": "MP4 Video",       # Common (Isom)
    "0000001466747970": "MP4 / MOV Video", # QuickTime / Apple
    "1A45DFA3"        : "MKV / WebM Video"         # Matroska Video (Bonus!)
}

# --- VISUALS ---
class Colors:
    CYAN = '\033[96m'
    ORANGE = '\033[33m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def show_banner():
    """Displays the Tool Name in ASCII Art"""
    banner = f"""{Colors.CYAN}
    ███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗ 
    ████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝ 
    ██╔████╔██║███████║██║  ███╗██║██║      
    ██║╚██╔╝██║██╔══██║██║   ██║██║██║      
    ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗ 
    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝ 
             {Colors.ORANGE}v1.1 - File Type & Magic Number Scanner{Colors.RESET}
    """
    print(banner)

def get_hex_signature(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read(32) 
            return binascii.hexlify(content).decode('utf-8').lower()
    except Exception:
        return None

def run_system_file_command(file_path):
    if not shutil.which("file"):
        return "Command 'file' not found (Are you on Windows?)"
    try:
        result = subprocess.check_output(['file', file_path], stderr=subprocess.STDOUT)
        return result.decode('utf-8').strip()
    except Exception as e:
        return f"Error: {e}"

def analyze():
    # 1. Clear screen and show banner
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()
    
    # 2. Input
    file_path = input(f"{Colors.BOLD}Enter file path to analyze: {Colors.RESET}").strip()
    print() 

    if not os.path.isfile(file_path):
        print(f"{Colors.RED}[!] Error: File not found.{Colors.RESET}")
        input("\nPress Enter to try again...")
        return

    # 3. Magic Number Analysis
    print(f"{Colors.CYAN}--- Magic Number Analysis ---{Colors.RESET}")
    
    raw_hex = get_hex_signature(file_path)
    print(f"Raw hex: {Colors.BLUE}{raw_hex}{Colors.RESET}")

    detected = "Unknown / Text File"
    upper_hex = raw_hex.upper()
    
    for magic, name in MAGIC_NUMBERS.items():
        if upper_hex.startswith(magic):
            detected = name
            break
            
    print(f"Detected: {Colors.GREEN}{detected}{Colors.RESET}")
    print()

    # 4. Extension info
    ext = os.path.splitext(file_path)[1].lower()
    print(f"File extension: {Colors.ORANGE}{ext}{Colors.RESET}")
    print()

    # 5. File Command Output
    print(f"{Colors.CYAN}--- System File Command ---{Colors.RESET}")
    sys_output = run_system_file_command(file_path)
    print(f"{sys_output}")
    print()

    # 6. Conclusion & Alert Logic
    print(f"{Colors.CYAN}--- Final Verdict ---{Colors.RESET}")
    
    # Logic to determine if there is a mismatch
    mismatch = False
    
    # If we didn't identify the magic number, we can't be sure (so no alert)
    if "Unknown" in detected:
        print(f"{Colors.ORANGE}[?] Signature unknown. Cannot verify integrity.{Colors.RESET}")
        
    else:
        # Check specific known types
        # Case A: Executables
        if "Executable" in detected:
            if ext not in ['.exe', '.dll', '.bin', '.elf', '.o', '.msi']:
                mismatch = True
        
        # Case B: Images
        elif "JPEG" in detected and ext not in ['.jpg', '.jpeg']: mismatch = True
        elif "PNG" in detected and ext != '.png': mismatch = True
        elif "GIF" in detected and ext != '.gif': mismatch = True
        
        # Case C: PDF
        elif "PDF" in detected and ext != '.pdf': mismatch = True
        
        # Case D: ZIP / Office (Note: DOCX/XLSX are technically ZIPs, so this is valid)
        elif "ZIP" in detected:
            if ext not in ['.zip', '.docx', '.xlsx', '.pptx', '.jar', '.apk']:
                mismatch = True

        # --- TRIGGER THE ALERT ---
        if mismatch:
            print(f"{Colors.RED}{Colors.BOLD}[!!!] SECURITY ALERT: EXTENSION MISMATCH! [!!!]{Colors.RESET}")
            print(f"{Colors.RED} >> The file header says it is: {detected}")
            print(f" >> But the extension is:       {ext}{Colors.RESET}")
            print(f"{Colors.RED} >> This is a common malware hiding tactic.{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}[OK] Verified: File signature matches the extension.{Colors.RESET}")

    print("-" * 50)
    input("Press Enter to continue ...")

if __name__ == "__main__":
    while True:
        analyze()