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
    (project_dir / 'README.md').write_text('readme')
    
    cp = CheckpointManager(project_dir)
    checkpoint = cp.create_checkpoint(name='baseline', description='', phase='coding')
    
    # Add new file
    (project_dir / 'src' / 'added.py').write_text('# added')
    (project_dir / 'README.md').write_text('# MODIFIED')
    
    # Compare
    comparison = cp.compare_checkpoint(checkpoint.id)
    print('Comparison result:')
    print(json.dumps(comparison, indent=2))
