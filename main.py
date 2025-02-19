from elftools.elf.elffile import ELFFile
from pathlib import Path
import sqlite3
import datetime

SHF_ALLOC_FLAG = 0x2 # Indicates that the ELF section is loadable

def get_section_sizes(elf_path: Path) -> dict:
    with open(elf_path, "rb") as f:
        elf = ELFFile(f)
        section_sizes = {}
        for section in elf.iter_sections():
            # Only include sections that are named and loadable
            if section.name and (section["sh_flags"] & SHF_ALLOC_FLAG):
                section_sizes[section.name] = section["sh_size"]
    return section_sizes

def update_database(section_sizes: dict) -> None:
    conn = sqlite3.connect("elf_sections.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elf_sections (
            timestamp TEXT,
            section_name TEXT,
            size INTEGER,
            PRIMARY KEY (timestamp, section_name)
        )
    ''')
    timestamp = datetime.datetime.now().isoformat()
    for section_name, size in section_sizes.items():
        cursor.execute('''
            INSERT INTO elf_sections (timestamp, section_name, size)
            VALUES (?, ?, ?)
        ''', (timestamp, section_name, size))
    conn.commit()
    conn.close()

def main():
    elf_file = Path("../dummy-c-project/c_project2.elf")
    section_sizes = get_section_sizes(elf_file)
    update_database(section_sizes)

if __name__ == "__main__":
    main()
