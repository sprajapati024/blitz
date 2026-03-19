#!/usr/bin/env python3
import tempfile
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).parent))

from core.checkpoint_manager import CheckpointManager, InterruptHandler

with tempfile.TemporaryDirectory() as tmpdir:
    project_dir = Path(tmpdir) / 'test'
    project_dir.mkdir()
    (project_dir / 'src').mkdir()
    (project_dir / 'src' / 'main.py').write_text('hello')
    
    handler = InterruptHandler(project_dir)
    
    result = handler.handle_interrupt(
        user_request="Use PostgreSQL instead of SQLite",
        current_phase="coding",
        current_task="Setting up database",
        agent_status={'coder': 'running'},
        completed_tasks=['Project structure', 'Dependencies']
    )
    
    print('Handle interrupt result:')
    print(f"Options count: {len(result['options'])}")
    for opt in result['options']:
        print(f"  - {opt['id']}: {opt['title']}")
