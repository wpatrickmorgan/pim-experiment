"""
Custom bench commands for Imperium PIM
"""

import click
import os
import sys
from pathlib import Path


@click.command('build-frontend')
@click.option('--frontend-path', default=None, help='Path to frontend repository')
def build_frontend(frontend_path=None):
    """Build and integrate the PIM frontend with Frappe"""
    
    # Get the current app directory
    app_dir = Path(__file__).parent.parent.absolute()
    
    # Import and run the build script
    build_script = app_dir / "build_frontend.py"
    
    if not build_script.exists():
        click.echo(f"❌ Build script not found: {build_script}")
        sys.exit(1)
    
    # Set frontend path if provided
    if frontend_path:
        os.environ['FRONTEND_PATH'] = frontend_path
    
    # Execute the build script
    click.echo("🚀 Building PIM Frontend...")
    
    try:
        # Import and execute the build script
        import subprocess
        result = subprocess.run([sys.executable, str(build_script)], cwd=app_dir)
        
        if result.returncode == 0:
            click.echo("✅ Frontend build completed successfully!")
            click.echo("💡 Run 'bench restart' to reload the changes")
        else:
            click.echo("❌ Frontend build failed!")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Error during build: {str(e)}")
        sys.exit(1)


commands = [
    build_frontend
]

