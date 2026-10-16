import os
import sys
import subprocess
from pathlib import Path

# Nama environment yang disepakati bersama tim
VENV_NAME = "proyek-gaming"
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"


def get_venv_python(venv_dir: Path) -> Path:
    """Mengambil path executable python di dalam virtual environment."""
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def find_existing_venv() -> Path | None:
    """Mencari apakah venv proyek-gaming sudah ada di root proyek atau di Conda."""
    # 1. Cek local venv di dalam folder proyek
    local_venv = ROOT_DIR / VENV_NAME
    if local_venv.exists() and get_venv_python(local_venv).exists():
        return local_venv

    # 2. Cek apakah ada Conda env bernama 'proyek-gaming'
    user_home = Path.home()
    conda_paths = [
        user_home / "miniconda3" / "envs" / VENV_NAME,
        user_home / "anaconda3" / "envs" / VENV_NAME,
        Path("C:/ProgramData/miniconda3/envs") / VENV_NAME,
        Path("C:/ProgramData/anaconda3/envs") / VENV_NAME,
    ]
    for cp in conda_paths:
        py_exe = cp / "python.exe"
        if py_exe.exists():
            return cp

    return None


def setup_venv():
    """Membuat venv dan menginstal seluruh dependensi dari requirements.txt."""
    print("=" * 50)
    print("  SETUP VIRTUAL ENVIRONMENT PROYEK GAMING")
    print("=" * 50)

    # 1. Cek apakah environment sudah ada
    existing_env = find_existing_venv()
    if existing_env:
        print(f"[INFO] Virtual environment '{VENV_NAME}' ditemukan di:")
        print(f"       -> {existing_env}")
        target_python = get_venv_python(existing_env)
        if not target_python.exists():
            # Conda python path di Windows berada langsung di root env
            target_python = existing_env / "python.exe"
    else:
        # Buat virtual environment standar (venv) di root proyek
        target_env = ROOT_DIR / VENV_NAME
        print(f"[INFO] Membuat virtual environment baru '{VENV_NAME}' di root proyek...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(target_env)], check=True)
            print(f"[SUCCESS] Virtual environment '{VENV_NAME}' berhasil dibuat.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Gagal membuat virtual environment: {e}")
            sys.exit(1)

        target_python = get_venv_python(target_env)

    # 2. Update pip & pasang requirements.txt
    if not REQUIREMENTS_FILE.exists():
        print(f"[WARNING] File {REQUIREMENTS_FILE.name} tidak ditemukan.")
        return

    print("\n[INFO] Menginstal / memverifikasi dependensi dari requirements.txt...")
    try:
        subprocess.run(
            [str(target_python), "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
        )
        subprocess.run(
            [str(target_python), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
            check=True,
        )
        print("\n" + "=" * 50)
        print("  SETUP SELESAI & DEPENDENSI TERPASANG!")
        print("=" * 50)
        print(f"Python Executable: {target_python}")
        print(f"Referensi Dependensi: {REQUIREMENTS_FILE.name}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Gagal menginstal dependensi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_venv()
