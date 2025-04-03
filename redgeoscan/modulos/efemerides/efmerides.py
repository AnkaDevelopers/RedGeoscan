import os
import time
import gzip
import shutil
from ftplib import FTP

FTP_SERVER = "lox.ucsd.edu"
BASE_FTP_PATH = "/pub/products/"

def connect_and_navigate(ftp_server: str, ftp_path: str) -> FTP:
    ftp = FTP(ftp_server)
    ftp.login()
    ftp.cwd(ftp_path)
    return ftp

def wait_for_files(ftp: FTP, max_attempts: int = 10, wait_seconds: int = 5) -> list:
    for _ in range(max_attempts):
        files = ftp.nlst()
        if files:
            return files
        time.sleep(wait_seconds)
    return []

def buscar_archivos(files: list) -> list:
    return [f for f in files if (
        (f.startswith("COD0OPSFIN_") or f.startswith("COD0OPSRAP_")) and f.endswith("ORB.SP3.gz")
        or f.startswith("igr")
        or f.startswith("igs")
    )]

def descargar_archivo(ftp: FTP, filename: str, destino: str) -> str:
    os.makedirs(destino, exist_ok=True)
    local_file_path = os.path.join(destino, filename)
    with open(local_file_path, "wb") as local_file:
        ftp.retrbinary(f"RETR {filename}", local_file.write)
    return local_file_path

def descomprimir_gz(file_path: str) -> str:
    extracted_file_path = file_path[:-3]
    with gzip.open(file_path, "rb") as f_in:
        with open(extracted_file_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)
    return extracted_file_path

def descargar_efemeride_para_semana(gps_week: str, destino: str) -> bool | None:
    ftp_path = f"{BASE_FTP_PATH}{gps_week}/"
    try:
        ftp = connect_and_navigate(FTP_SERVER, ftp_path)
        files = wait_for_files(ftp)
        if not files:
            ftp.quit()
            return None

        archivos_encontrados = buscar_archivos(files)
        if archivos_encontrados:
            for archivo in archivos_encontrados:
                local_file = descargar_archivo(ftp, archivo, destino)
                descomprimir_gz(local_file)
            ftp.quit()
            return True

        ftp.quit()
        return None

    except Exception as e:
        print(f"Error en la descarga: {e}")
        return None
