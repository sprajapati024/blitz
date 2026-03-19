#!/usr/bin/env python3
import tempfile
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).parent))

from core.checkpoint_manager import CheckpointManager

with tempfile.TemporaryDirectory() as tmpdir:
    project_dir = Path(tmpdir) / 'test'
    project_dir.mkdir()
    (project_dir / 'src').mkdir()
    (project_dir / 'src' / 'main.py').write_text('hello')
    (project_dir / 'src' / 'data.py').write_text('data')
    (project_dir / 'README.md').write_text('readme')
    
    cp = CheckpointManager(project_dir)
    checkpoint = cp.create_checkpoint(name='baseline', description='', phase='coding')
    
    # Add new file (would be REMOVED on restore)
    (project_dir / 'src' / 'added.py').write_text('# added')
    
    # Modify existing (would be REVERTED on restore)
    (project_dir / 'README.md').write_text('# MODIFIED')
    
    # Delete a file (would be RESTORED)
    (project_dir / 'src' / 'data.py').unlink()
    
    # Compare
    comparison = cp.compare_checkpoint(checkpoint.id)
    print('Would lose files:')
    print(comparison['would_lose_files'])
    print()
    print(f"Looking for 'added.py' in: {comparison['would_lose_files']}")
