import os

# Define the folder structure
structure = {
    "business-price-tracker": {
        "data": {
            "raw": {},
            "cleaned": {}
        },
        "reports": {},
        "src": {
            "__init__.py": "",
            "fetch_data.py": "",
            "clean_data.py": "",
            "generate_excel.py": "",
            "update_sheet.py": "",
            "generate_pdf.py": "",
            "send_email.py": "",
            "utils.py": "",
            "main.py": ""
        },
        "logs": {},
        ".env": "",
        "requirements.txt": "",
        "Dockerfile": "",
        "README.md": "",
        "scheduler.bat": "",
        "cron.sh": ""
    }
}

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Create empty file
            with open(path, "w") as f:
                f.write(content)

# Run the function
create_structure(".", structure)
print("Project structure created successfully!")
