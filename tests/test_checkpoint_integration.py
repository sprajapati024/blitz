#!/usr/bin/env python3
"""
Integration tests for Smart Interruptions (Phase 2B)

These tests verify that checkpointing actually works:
- Files are actually saved and restored
- State persists correctly
- Interruptions are handled properly
"""

import sys
import tempfile
import shutil
from pathlib import Path
import json

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.checkpoint_manager import CheckpointManager, InterruptHandler


class TestCheckpointManager:
    """Test the checkpoint manager end-to-end"""
    
    def setup_test_project(self, tmpdir: Path) -> Path:
        """Create a realistic test project structure"""
        project_dir = tmpdir / "test_trading_bot"
        project_dir.mkdir()
        
        # Create realistic file structure
        (project_dir / "src").mkdir()
        (project_dir / "tests").mkdir()
        (project_dir / "docs").mkdir()
        
        # Main module
        (project_dir / "src" / "main.py").write_text('''
import asyncio
from data import PriceFetcher
from trading import PaperTrader

async def main():
    fetcher = PriceFetcher()
    trader = PaperTrader()
    
    # Main loop
    while True:
        prices = await fetcher.get_prices()
        trader.evaluate(prices)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
''')
        
        # Data module
        (project_dir / "src" / "data.py").write_text('''
import requests
from typing import Dict, Any

class PriceFetcher:
    """Fetches stock prices from Yahoo Finance"""
    
    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
    
    def __init__(self):
        self.session = requests.Session()
    
    async def get_prices(self, symbols: list) -> Dict[str, float]:
        """Fetch current prices for symbols"""
        prices = {}
        for symbol in symbols:
            data = self._fetch(symbol)
            prices[symbol] = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return prices
    
    def _fetch(self, symbol: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{symbol}"
        resp = self.session.get(url)
        return resp.json()
''')
        
        # Trading module
        (project_dir / "src" / "trading.py").write_text('''
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Position:
    symbol: str
    shares: float
    entry_price: float
    entry_time: datetime

class PaperTrader:
    """Paper trading engine - simulates trades without real money"""
    
    def __init__(self, initial_balance: float = 50000.0):
        self.balance = initial_balance
        self.positions: Dict[str, Position] = {}
        self.history: List[dict] = []
    
    def buy(self, symbol: str, shares: float, price: float):
        cost = shares * price
        if cost > self.balance:
            raise ValueError(f"Insufficient funds: ${cost:.2f} needed, ${self.balance:.2f} available")
        
        self.balance -= cost
        self.positions[symbol] = Position(symbol, shares, price, datetime.now())
        self._log_trade("BUY", symbol, shares, price)
    
    def sell(self, symbol: str, price: float):
        if symbol not in self.positions:
            raise ValueError(f"No position in {symbol}")
        
        position = self.positions[symbol]
        proceeds = position.shares * price
        pnl = proceeds - (position.shares * position.entry_price)
        
        self.balance += proceeds
        del self.positions[symbol]
        self._log_trade("SELL", symbol, position.shares, price, pnl=pnl)
    
    def evaluate(self, prices: Dict[str, float]):
        """Evaluate current positions against market prices"""
        for symbol, price in prices.items():
            if symbol in self.positions:
                self._check_stop_loss(symbol, price)
    
    def _check_stop_loss(self, symbol: str, current_price: float):
        """Check if stop loss triggered"""
        position = self.positions[symbol]
        drop_pct = (position.entry_price - current_price) / position.entry_price
        
        if drop_pct > 0.05:  # 5% stop loss
            self.sell(symbol, current_price)
    
    def _log_trade(self, action: str, symbol: str, shares: float, price: float, pnl: float = None):
        entry = {
            "time": datetime.now().isoformat(),
            "action": action,
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "total": shares * price
        }
        if pnl is not None:
            entry["pnl"] = pnl
        self.history.append(entry)
''')
        
        # Tests
        (project_dir / "tests" / "test_trading.py").write_text('''
import pytest
from trading import PaperTrader

def test_buy_creates_position():
    trader = PaperTrader(initial_balance=10000)
    trader.buy("AAPL", 10, 150.0)
    
    assert "AAPL" in trader.positions
    assert trader.positions["AAPL"].shares == 10
    assert trader.balance == 8500.0

def test_sell_realizes_pnl():
    trader = PaperTrader(initial_balance=10000)
    trader.buy("AAPL", 10, 150.0)
    trader.sell("AAPL", 160.0)
    
    assert "AAPL" not in trader.positions
    assert trader.balance == 10100.0  # $100 profit

def test_insufficient_funds():
    trader = PaperTrader(initial_balance=100)
    with pytest.raises(ValueError):
        trader.buy("AAPL", 10, 150.0)
''')
        
        # Docs
        (project_dir / "README.md").write_text('''# Trading Bot

Paper trading bot for stock evaluation.

## Features
- Real-time price fetching
- Paper trading (no real money)
- Stop-loss automation
- Trade history

## Setup
```bash
pip install -r requirements.txt
python src/main.py
```
''')
        
        (project_dir / "ARCHITECTURE.md").write_text('''# Architecture

## Components
1. PriceFetcher - Gets market data
2. PaperTrader - Executes virtual trades
3. Position - Tracks holdings

## Data Flow
Prices -> Evaluate -> Trade -> Log
''')
        
        return project_dir
    
    def test_create_checkpoint_saves_files(self):
        """Verify checkpoint actually saves project files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = self.setup_test_project(Path(tmpdir))
            
            # Initialize checkpoint manager
            cp = CheckpointManager(project_dir)
            
            # Create checkpoint
            checkpoint = cp.create_checkpoint(
                name="initial_state",
                description="Before major refactor",
                agent_status={'coder': 'running'},
                current_tasks=['Refactor data layer'],
                completed_tasks=['Setup project'],
                phase='coding'
            )
            
            # Verify checkpoint directory exists
            checkpoint_dir = project_dir / ".blitz" / "checkpoints" / checkpoint.id
            assert checkpoint_dir.exists(), "Checkpoint directory not created"
            
            # Verify files were copied
            assert (checkpoint_dir / "src" / "main.py").exists(), "main.py not saved"
            assert (checkpoint_dir / "src" / "data.py").exists(), "data.py not saved"
            assert (checkpoint_dir / "src" / "trading.py").exists(), "trading.py not saved"
            assert (checkpoint_dir / "tests" / "test_trading.py").exists(), "tests not saved"
            assert (checkpoint_dir / "README.md").exists(), "README not saved"
            assert (checkpoint_dir / "ARCHITECTURE.md").exists(), "ARCHITECTURE not saved"
            
            # Verify state file
            state_file = checkpoint_dir / "_state.json"
            assert state_file.exists(), "State file not saved"
            
            state = json.loads(state_file.read_text())
            assert state['agent_status']['coder'] == 'running'
            assert 'Refactor data layer' in state['current_tasks']
            
            print("✅ Test passed: Checkpoint saves all files correctly")
            return True
    
    def test_restore_checkpoint_actually_restores(self):
        """Verify restore actually puts files back"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = self.setup_test_project(Path(tmpdir))
            cp = CheckpointManager(project_dir)
            
            # Create checkpoint
            checkpoint = cp.create_checkpoint(
                name="before_changes",
                description="Original state",
                phase='coding'
            )
            
            # Modify project files
            (project_dir / "src" / "new_feature.py").write_text("# NEW CODE\n")
            (project_dir / "src" / "main.py").write_text("# COMPLETELY CHANGED\n")
            
            # Restore checkpoint
            result = cp.restore_checkpoint(checkpoint.id)
            
            assert result['success'], f"Restore failed: {result.get('error')}"
            assert result['restored'], "Restore not marked as completed"
            
            # Verify files restored
            main_content = (project_dir / "src" / "main.py").read_text()
            assert 'asyncio' in main_content, "main.py not restored correctly"
            assert 'PriceFetcher' in main_content, "main.py content wrong"
            
            # Verify new file removed
            assert not (project_dir / "src" / "new_feature.py").exists(), "New file not removed"
            
            print("✅ Test passed: Restore actually restores files")
            return True
    
    def test_compare_shows_what_would_change(self):
        """Verify dry-run compare shows accurate diff"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = self.setup_test_project(Path(tmpdir))
            cp = CheckpointManager(project_dir)
            
            # Create checkpoint
            checkpoint = cp.create_checkpoint(name="baseline", description="", phase='coding')
            
            # Add new file (would be REMOVED on restore)
            (project_dir / "src" / "added.py").write_text("# added\n")
            
            # Modify existing (would be REVERTED on restore)
            (project_dir / "README.md").write_text("# MODIFIED\n")
            
            # Delete a file (would be RESTORED)
            (project_dir / "src" / "data.py").unlink()
            
            # Compare
            comparison = cp.compare_checkpoint(checkpoint.id)
            
            assert comparison['success'], "Compare failed"
            # We deleted a file, so there's something to restore
            assert comparison['changes']['files_to_restore'] > 0, "Should show files to restore"
            # We added a file, so there's something to remove
            assert comparison['changes']['files_to_remove'] > 0, "Should show files to remove"
            # We modified a file
            assert comparison['changes']['files_to_modify'] > 0, "Should show files to modify"
            
            # Verify specific files mentioned (path format is relative like 'src/added.py')
            assert any('added.py' in f for f in comparison['would_lose_files']), "Added file not in diff"
            
            print("✅ Test passed: Compare shows accurate diff")
            return True
    
    def test_list_checkpoints_returns_valid_checkpoints(self):
        """Verify checkpoint listing works"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = self.setup_test_project(Path(tmpdir))
            cp = CheckpointManager(project_dir)
            
            # Create multiple checkpoints
            cp1 = cp.create_checkpoint(name="first", description="", phase='coding')
            cp2 = cp.create_checkpoint(name="second", description="", phase='coding')
            cp3 = cp.create_checkpoint(name="third", description="", phase='testing')
            
            # List checkpoints
            checkpoints = cp.list_checkpoints()
            
            assert len(checkpoints) == 3, f"Expected 3 checkpoints, got {len(checkpoints)}"
            
            # Verify order (newest first)
            assert checkpoints[0].id == cp3.id, "Wrong order - newest should be first"
            assert checkpoints[1].id == cp2.id
            assert checkpoints[2].id == cp1.id
            
            print("✅ Test passed: Checkpoints listed correctly")
            return True
    
    def test_checkpoint_registry_persists(self):
        """Verify checkpoint registry survives across manager instances"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = self.setup_test_project(Path(tmpdir))
            
            # First manager instance
            cp1 = CheckpointManager(project_dir)
            checkpoint = cp1.create_checkpoint(name="test", description="", phase='coding')
            
            # Second manager instance (simulates restart)
            cp2 = CheckpointManager(project_dir)
            checkpoints = cp2.list_checkpoints()
            
            assert len(checkpoints) == 1, "Checkpoint not persisted"
            assert checkpoints[0].id == checkpoint.id, "Wrong checkpoint"
            
            # Verify can restore from second instance
            result = cp2.restore_checkpoint(checkpoint.id, dry_run=True)
            assert result['success'], "Can't restore from new instance"
            
            print("✅ Test passed: Registry persists across instances")
            return True


class TestInterruptHandler:
    """Test the interrupt handler"""
    
    def setup_test_project(self, tmpdir: Path) -> Path:
        """Create minimal test project"""
        project_dir = tmpdir / "test_project"
        project_dir.mkdir()
        (project_dir / "src").mkdir()
        (project_dir / "src" / "main.py").write_text("print('hello')\n")
        return project_dir
    
    def test_handle_interrupt_creates_checkpoint(self):
        """Verify interrupt handler creates checkpoint"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = self.setup_test_project(Path(tmpdir))
            
            handler = InterruptHandler(project_dir)
            
            result = handler.handle_interrupt(
                user_request="Use PostgreSQL instead of SQLite",
                current_phase="coding",
                current_task="Setting up database",
                agent_status={'coder': 'running'},
                completed_tasks=['Project structure', 'Dependencies']
            )
            
            # Should have created checkpoint
            assert 'interruption_checkpoint' in result
            checkpoint_id = result['interruption_checkpoint']['id']
            
            # Verify checkpoint exists
            cp_manager = CheckpointManager(project_dir)
            checkpoints = cp_manager.list_checkpoints()
            assert any(cp.id == checkpoint_id for cp in checkpoints), "Checkpoint not created"
            
            # Should have at least 2 options (continue_then_change and start_fresh are always there)
            assert len(result['options']) >= 2, f"Should have options, got {len(result['options'])}"
            
            # Should have the expected option IDs
            option_ids = [opt['id'] for opt in result['options']]
            assert 'continue_then_change' in option_ids, "Missing continue_then_change option"
            assert 'start_fresh' in option_ids, "Missing start_fresh option"
            
            print("✅ Test passed: Interrupt handler creates checkpoint")
            return True
    
    def test_execute_option_rewind(self):
        """Verify execute_option actually rewinds"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = self.setup_test_project(Path(tmpdir))
            
            # Create checkpoint
            cp = CheckpointManager(project_dir)
            checkpoint = cp.create_checkpoint(name="baseline", description="", phase='coding')
            
            # Modify project
            (project_dir / "src" / "modified.py").write_text("# changed\n")
            
            # Execute rewind
            handler = InterruptHandler(project_dir, cp)
            result = handler.execute_option(
                option_id='rewind',
                context={'checkpoint_id': checkpoint.id}
            )
            
            assert result['action'] == 'rewind', f"Wrong action: {result.get('action')}"
            assert result['restore_result']['restored'], "Not marked as restored"
            
            # Verify files restored
            assert not (project_dir / "src" / "modified.py").exists(), "Modified file not removed"
            
            print("✅ Test passed: Rewind option actually works")
            return True


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("INTEGRATION TESTS: Smart Interruptions (Phase 2B)")
    print("="*60 + "\n")
    
    test_checkpoint = TestCheckpointManager()
    test_interrupt = TestInterruptHandler()
    
    tests = [
        ("Create checkpoint saves files", test_checkpoint.test_create_checkpoint_saves_files),
        ("Restore actually restores", test_checkpoint.test_restore_checkpoint_actually_restores),
        ("Compare shows diff", test_checkpoint.test_compare_shows_what_would_change),
        ("List checkpoints", test_checkpoint.test_list_checkpoints_returns_valid_checkpoints),
        ("Registry persists", test_checkpoint.test_checkpoint_registry_persists),
        ("Handle interrupt creates checkpoint", test_interrupt.test_handle_interrupt_creates_checkpoint),
        ("Execute rewind works", test_interrupt.test_execute_option_rewind),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {name}")
            print(f"   Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
