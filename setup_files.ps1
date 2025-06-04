@'
# Create all necessary files for FINKI Forum

Write-Host "Creating file structure..." -ForegroundColor Green

# Create empty __init__.py files
"" | Out-File -FilePath "forum\management\__init__.py" -Encoding UTF8
"" | Out-File -FilePath "forum\management\commands\__init__.py" -Encoding UTF8
"" | Out-File -FilePath "forum\templatetags\__init__.py" -Encoding UTF8

# Create Python files with basic content
@"
# Add your forms here
from django import forms
"@ | Out-File -FilePath "accounts\forms.py" -Encoding UTF8

@"
# Add your forms here
from django import forms
"@ | Out-File -FilePath "forum\forms.py" -Encoding UTF8

@"
# Context processors
def forum_context(request):
    return {}
"@ | Out-File -FilePath "forum\context_processors.py" -Encoding UTF8

@"
# Template tags
from django import template
register = template.Library()
"@ | Out-File -FilePath "forum\templatetags\forum_extras.py" -Encoding UTF8

@"
# Management command
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'Create sample data'
    def handle(self, *args, **options):
        self.stdout.write('Sample data created')
"@ | Out-File -FilePath "forum\management\commands\create_sample_data.py" -Encoding UTF8

# Create CSS file
@"
/* FINKI Forum Styles */
body {
    background-color: #f8f9fa;
}
"@ | Out-File -FilePath "static\css\styles.css" -Encoding UTF8

# Create JS file
@"
// FINKI Forum JavaScript
console.log('FINKI Forum loaded');
"@ | Out-File -FilePath "static\js\main.js" -Encoding UTF8

Write-Host "Files created successfully!" -ForegroundColor Green
'@ | Out-File -FilePath setup_files.ps1 -Encoding UTF8

# Run the script
powershell -ExecutionPolicy Bypass -File setup_files.ps1