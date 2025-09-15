# Download all required installers for offline installation
Write-Host "Downloading all required installers..." -ForegroundColor Green

# Create installers directory
$installersDir = ".\installers"
if (!(Test-Path $installersDir)) {
    New-Item -ItemType Directory -Path $installersDir
}

# Download URLs (latest stable versions)
$downloads = @{
    "Git-2.43.0-64-bit.exe" = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    "python-3.11.7-amd64.exe" = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    "VSCodeUserSetup-x64-1.84.2.exe" = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
}

# Download each installer
foreach ($file in $downloads.Keys) {
    $url = $downloads[$file]
    $outputPath = Join-Path $installersDir $file
    
    if (Test-Path $outputPath) {
        Write-Host "✓ $file already exists" -ForegroundColor Yellow
    } else {
        Write-Host "Downloading $file..." -ForegroundColor Cyan
        try {
            Invoke-WebRequest -Uri $url -OutFile $outputPath -UseBasicParsing
            Write-Host "✓ $file downloaded successfully" -ForegroundColor Green
        } catch {
            Write-Host "✗ Failed to download $file" -ForegroundColor Red
            Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host "`nAll installers ready! Run INSTALL.bat to install everything." -ForegroundColor Green
