Write-Host ""
Write-Host "========================================="
Write-Host "     JalNetra Backend Setup"
Write-Host "========================================="
Write-Host ""

# Create folders
$folders = @(
"app",
"app/api",
"app/core",
"app/database",
"app/models",
"app/schemas",
"app/services",
"app/utils",
"logs"
)

foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created $folder"
    }
}

# Create __init__.py files
$initFiles = @(
"app/__init__.py",
"app/api/__init__.py",
"app/core/__init__.py",
"app/database/__init__.py",
"app/models/__init__.py",
"app/schemas/__init__.py",
"app/services/__init__.py",
"app/utils/__init__.py"
)

foreach ($file in $initFiles) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}

# Create empty files
$files = @(
"app/main.py",
"app/core/config.py",
"app/database/database.py",
".env",
".gitignore",
"requirements.txt",
"README.md"
)

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}

Write-Host ""
Write-Host "========================================="
Write-Host " Setup Completed Successfully!"
Write-Host "========================================="