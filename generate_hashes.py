import hashlib
import json
from pathlib import Path

def calculate_file_hash(file_path):
    """একটি ফাইলের SHA256 hash calculate করে"""
    path = Path(file_path)
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()

def generate_hashes():
    """সবগুলো ফাইলের hash generate করে"""
    files_to_check = [
        'email_router.py',
        'gui_app.py', 
        'license_manager.py'
    ]
    
    hashes = {}
    
    for file in files_to_check:
        hash_value = calculate_file_hash(file)
        if hash_value:
            hashes[file] = hash_value
            print(f"✅ {file}: {hash_value}")
        else:
            print(f"❌ {file}: File not found!")
    
    return hashes

def generate_php_code(hashes):
    """PHP array code generate করে"""
    php_code = """function load_code_hashes(): array {
    return ["""
    
    for file, hash_val in hashes.items():
        php_code += f"\n        '{file}' => '{hash_val}',"
    
    php_code += "\n    ];\n}"
    return php_code

if __name__ == "__main__":
    print("🔍 Calculating file hashes...\n")
    
    hashes = generate_hashes()
    
    print("\n📝 PHP Code:\n")
    php_code = generate_php_code(hashes)
    print(php_code)
    
    # ফাইলে save করার option
    save_to_file = input("\n💾 Save to hashes_output.php? (y/n): ")
    if save_to_file.lower() == 'y':
        with open('hashes_output.php', 'w') as f:
            f.write("<?php\n\n")
            f.write(php_code)
            f.write("\n\n?>")
        print("✅ Saved to hashes_output.php")