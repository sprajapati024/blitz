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
    (project_dir / 'src' / 'main.py').write_text('original content')
    
    # Create checkpoint
    cp = CheckpointManager(project_dir)
    checkpoint = cp.create_checkpoint(name="baseline", description="", phase='coding')
    
    # Modify project
    (project_dir / 'src' / 'modified.py').write_text('# changed')
    
    # Execute rewind
    handler = InterruptHandler(project_dir, cp)
    result = handler.execute_option(
        option_id='rewind',
        context={'checkpoint_id': checkpoint.id}
    )
    
    print('Execute rewind result:')
    print(json.dumps(result, indent=2))
    print()
    print(f"Keys: {result.keys()}")
