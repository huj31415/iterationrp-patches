import zipfile
import tempfile
import subprocess
import sys
from pathlib import Path

# To generate the patch file:
# git diff --no-index original_shader_folder patched_shader_folder > patch.diff

# Usage:
# python patch_shader.py input.zip patch.diff output.zip

def extract_zip(zip_path, directory):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(directory)


def create_zip(directory, zip_path):
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path in Path(directory).rglob("*"):
            if path.is_file():
                z.write(path, path.relative_to(directory))


def apply_patch(directory, patch_file):
    result = subprocess.run(
        ["patch", "-p2", "-i", str(patch_file)],
        cwd=directory,
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("WARNING: patch command reported errors")
        print(result.stderr)


def patch_zip(input_zip, patch_file, output_zip):
    with tempfile.TemporaryDirectory() as tmp:

        tmp_dir = Path(tmp)

        extract_dir = tmp_dir / "shader"
        extract_dir.mkdir()

        print("Extracting zip...")
        extract_zip(input_zip, extract_dir)

        print("Applying patch...")
        apply_patch(extract_dir, patch_file)

        print("Creating patched zip...")
        create_zip(extract_dir, output_zip)

        print(f"Finished -> {output_zip}")


def main():
    if len(sys.argv) != 4:
        print("Usage:")
        print("python patch_shader.py input.zip patch.diff output.zip")
        sys.exit(1)

    input_zip = Path(sys.argv[1])
    patch_file = Path(sys.argv[2]).resolve()
    output_zip = Path(sys.argv[3])
    
    if not patch_file.exists():
        print(f"ERROR: Patch file not found: {patch_file}")
        sys.exit(1)

    patch_zip(input_zip, patch_file, output_zip)


if __name__ == "__main__":
    main()