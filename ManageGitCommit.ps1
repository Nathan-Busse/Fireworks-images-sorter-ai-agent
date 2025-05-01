# |------------------------------------------DO NOT IGNORE---------------------------------------------------|
# |  Make sure that you are using POWERSHELL 7.0 or higher.                                                  |
# |  This script must run with Administrator privileges to execute properly.                                 |
# |  It will auto-relaunch as Administrator if needed, and set its working directory correctly.              |
# |----------------------------------------------------------------------------------------------------------|

# This script handles Git operations by:
# - Automatically restarting with Administrator privileges if required.
# - Automatically changing the working directory to the script's location.
# - Configuring Git to support long paths globally.
# - Automating Git staging, commit, and push operations.

# ---------------------------------------------------CHANGELOG------------------------------------------------------
# v1.0.0 - Initial script created for Git operations (commit/push).
# v1.1.0 - Added automatic relaunch as Administrator using Start-Process with -Verb RunAs.
# v1.2.0 - Improved handling of working directories with $PSScriptRoot.
# v1.3.0 - Enhanced compatibility for running outside of VS Code.
# v1.4.0 - Introduced countdown timer before exiting for user confirmation.
# ---------------------------------------------------BEGIN---------------------------------------------------------

# Step 0: Auto-relaunch with Administrator privileges if not already elevated.
function Test-Admin {
    $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Admin)) {
    Write-Host "Script is not running as Administrator. Relaunching as Administrator..."
    try {
        Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
        Write-Host "Waiting 10 seconds before exiting to allow the relaunch process to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        exit
    } catch {
        Write-Error "Failed to relaunch as Administrator. Please manually run this script with Administrator privileges."
        Start-Sleep -Seconds 10
        exit
    }
}

# Step 1: Automatically change the working directory to the script's location (repo root assumed).
try {
    Set-Location -Path $PSScriptRoot
    Write-Host "Changed directory to the script's location: $PSScriptRoot"
} catch {
    Write-Error "Failed to change directory to the script's location. Check if the script path is accessible."
    Start-Sleep -Seconds 10
    exit
}

# Step 2: Configure Git's long path support globally.
try {
    Write-Host "Enabling Git's long path support globally..."
    git config --global core.longpaths true
    Write-Host "Git global long path support enabled successfully." -ForegroundColor Green
} catch {
    Write-Error "Failed to enable Git's long path support globally. Please ensure Git is installed."
    Start-Sleep -Seconds 10
    exit
}

# Step 3: Automate Git commit and push operations.
try {
    $commitMsg = Read-Host "Enter your commit message"
    if ([string]::IsNullOrWhiteSpace($commitMsg)) {
        Write-Error "Commit message cannot be empty. Exiting..."
        Start-Sleep -Seconds 10
        exit
    }

    Write-Host "Staging all changes..."
    git add .
    Write-Host "Committing changes..."
    git commit -m "$commitMsg"
    Write-Host "Pushing changes to the remote repository..."
    git push

    Write-Host "`nGit operations complete. Your changes are now live!" -ForegroundColor Green
} catch {
    Write-Error "Failed during Git commit/push operations. Please check your repository settings."
    Start-Sleep -Seconds 10
    exit
}

# Step 4: Countdown before exiting to ensure user sees final messages.
Write-Host "`nExiting script in:" -ForegroundColor Yellow
For ($i = 10; $i -ge 1; $i--) {
    Write-Host "$i seconds remaining..." -ForegroundColor Cyan
    Start-Sleep -Seconds 1
}
Write-Host "Goodbye! Script has completed." -ForegroundColor Green
exit
# --------------------------------------------------------END--------------------------------------------------------