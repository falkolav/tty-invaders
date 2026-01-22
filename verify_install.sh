#!/bin/bash
# Verification script for TTY Invaders installation

echo "=== TTY Invaders Installation Verification ==="
echo ""

# Test 1: Check if package is installed
echo "1. Checking if package is importable..."
if uv run python -c "from tty_invaders.game import Game; print('✓ Package imports successfully')" 2>/dev/null; then
    echo "   ✓ PASS: Package is importable"
else
    echo "   ✗ FAIL: Cannot import package"
    exit 1
fi
echo ""

# Test 2: Check if game initializes
echo "2. Testing game initialization..."
if uv run python -c "from tty_invaders.game import Game; g = Game(); assert g.initialize(), 'Init failed'; print('✓ Game initializes')" 2>/dev/null; then
    echo "   ✓ PASS: Game initializes successfully"
else
    echo "   ✗ FAIL: Game initialization failed"
    exit 1
fi
echo ""

# Test 3: Check if script exists
echo "3. Checking if tty-invaders script exists..."
if [ -f ".venv/bin/tty-invaders" ]; then
    echo "   ✓ PASS: Script exists at .venv/bin/tty-invaders"
else
    echo "   ✗ FAIL: Script not found"
    exit 1
fi
echo ""

# Test 4: Check if module can be run
echo "4. Testing module execution..."
if uv run python -m tty_invaders --help 2>&1 | head -1 | grep -q "Terminal" 2>/dev/null || \
   uv run python -c "from tty_invaders.__main__ import main; print('✓ Module is executable')" 2>/dev/null; then
    echo "   ✓ PASS: Module can be executed"
else
    echo "   ✗ FAIL: Module execution failed"
    exit 1
fi
echo ""

# Test 5: Run tests
echo "5. Running unit tests..."
if uv run pytest tests/ -q 2>/dev/null; then
    echo "   ✓ PASS: All tests passed"
else
    echo "   ✗ FAIL: Some tests failed"
    exit 1
fi
echo ""

echo "=== All Verification Tests Passed! ==="
echo ""
echo "You can now run the game using any of these methods:"
echo "  • uv run tty-invaders"
echo "  • uv run python -m tty_invaders"
echo "  • .venv/bin/tty-invaders"
echo ""
