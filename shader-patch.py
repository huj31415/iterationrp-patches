import zipfile
import tempfile
import logging
import patch_ng
import sys
from pathlib import Path
import shutil

# To generate the patch file:
# git diff --no-index original_shader_folder patched_shader_folder > patch.diff

# Usage:
# python shader-patch.py input.zip patch.diff output.zip

# Thanks to u/Lavenderanus for fixing line ending errors on linux
def normalize_line_endings(directory):
    for ext in ("*.glsl", "*.comp", "*.frag", "*.properties"):
        for path in Path(directory).rglob(ext):
            content = path.read_bytes().replace(b"\r\n", b"\n")
            path.write_bytes(content)

def extract_zip(zip_path, directory):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(directory)


def create_zip(directory, zip_path):
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path in Path(directory).rglob("*"):
            if path.is_file():
                z.write(path, path.relative_to(directory))


def apply_patch(directory, patch_file):
    patch_set = patch_ng.fromfile(str(patch_file))
    if not patch_set:
        print("\033[0m\033[1;31mWARNING: Could not parse patch file.\033[0m")
        return

    success = patch_set.apply(root=str(directory), strip=1)

    if not success:
        print("\033[0m\033[1;31mWARNING: patch-ng reported errors while applying the patch.\033[0m")

def copy_folder_into_zip(extract_dir, source_folder, destination_folder):
    source_folder = Path(source_folder)
    dest = extract_dir / destination_folder

    dest.mkdir(parents=True, exist_ok=True)

    shutil.copytree(source_folder, dest, dirs_exist_ok=True)

def patch_zip(input_zip, patch_file, output_zip, tex_src, tex_dest):
    with tempfile.TemporaryDirectory() as tmp:

        tmp_dir = Path(tmp)

        extract_dir = tmp_dir / "shader"
        extract_dir.mkdir()

        print("Extracting zip...")
        extract_zip(input_zip, extract_dir)

        print("Normalizing line endings...")
        normalize_line_endings(extract_dir)
        
        print("Applying patch...\033[2m")
        apply_patch(extract_dir, patch_file)
        print("\033[0m")

        if tex_src.exists():
            print(f"Copying textures to {tex_dest}")
            copy_folder_into_zip(extract_dir, tex_src, tex_dest)
        else:
            print(f"\033[1;31mERROR: Texture source folder not found: {tex_src}.\nPatch will proceed without copying textures, please manually add them.\033[0m")

        print("Creating patched zip...")
        create_zip(extract_dir, output_zip)

        print(f"\033[1;32mFinished -> {output_zip}\033[0m")


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage:")
        print("python shader-patch.py input.zip patch.diff output.zip [verbosity: 0 (default), 1, 2]")
        sys.exit(1)

    input_zip = Path(sys.argv[1])
    patch_file = Path(sys.argv[2]).resolve()
    output_zip = Path(sys.argv[3])
    
    verbosity = sys.argv[4] if len(sys.argv) > 4 else "0"
    if (verbosity) not in ["0", "1", "2"]:
        print("Invalid verbosity level. Use 0 (default), 1, or 2.")
        sys.exit(1)
    verbosity_levels = {0:logging.WARNING, 1:logging.INFO, 2:logging.DEBUG}
    loglevel = verbosity_levels[int(verbosity)]

    logging.basicConfig(level=loglevel)
    logger = logging.getLogger("patch_ng")
    logger.setLevel(loglevel)

    TEXTURE_SRC = Path(__file__).parent / "texture"
    TEXTURE_DEST = "shaders/texture"

    if not patch_file.exists():
        print(f"\033[1;31mERROR: Patch file not found: {patch_file}\033[0m")
        sys.exit(1)

    patch_zip(input_zip, patch_file, output_zip, TEXTURE_SRC, TEXTURE_DEST)


if __name__ == "__main__":
    main()
