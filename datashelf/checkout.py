import shutil
from pathlib import Path
from datashelf.load import load

def checkout(lookup_key: str, dest: str | Path) -> Path:
    src_path = load(lookup_key = lookup_key)
    
    dest_path: Path = Path(dest).resolve()
    
    if dest_path.suffix != ".parquet":
        raise TypeError(f"{dest} is invalid. Make sure file has .parquet suffix.")
    
    if dest_path.exists():
        raise FileExistsError(f"Destination already exists: {dest_path}")
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src_path), str(dest_path))

    print(f"Checked out artifact to {dest_path}")
    return dest_path
    