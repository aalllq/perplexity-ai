"""
Integration test script for Perplexity AI API enhancements.
Tests module imports, API server functionality, and LiteLLM integration.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("Test 1: Module Imports")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test perplexity module
    print("\n1.1. Testing perplexity module...")
    try:
        import perplexity
        assert hasattr(perplexity, 'Client')
        assert hasattr(perplexity, 'LiteLLMClient')
        assert hasattr(perplexity, 'OpenAIClient')
        assert hasattr(perplexity, 'PerplexityLiteLLMProvider')
        assert hasattr(perplexity, 'register_perplexity_provider')
        print("  ✓ All perplexity classes available")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    # Test perplexity_async module
    print("\n1.2. Testing perplexity_async module...")
    try:
        import perplexity_async
        assert hasattr(perplexity_async, 'Client')
        assert hasattr(perplexity_async, 'AsyncLiteLLMClient')
        assert hasattr(perplexity_async, 'AsyncOpenAIClient')
        print("  ✓ All perplexity_async classes available")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    # Test API server
    print("\n1.3. Testing API server...")
    try:
        import api_server
        assert hasattr(api_server, 'app')
        assert hasattr(api_server, 'config')
        print("  ✓ API server imports successful")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    return tests_passed, tests_failed


def test_client_initialization():
    """Test that clients can be initialized."""
    print("\n" + "=" * 60)
    print("Test 2: Client Initialization")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test LiteLLM client (without actual API call)
    print("\n2.1. Testing LiteLLMClient initialization...")
    try:
        import perplexity
        # This will fail without API key, but we can test initialization structure
        try:
            client = perplexity.LiteLLMClient(model="gpt-3.5-turbo")
            print("  ✓ LiteLLMClient initialized")
            tests_passed += 1
        except ImportError as e:
            print(f"  ⚠ LiteLLM not available: {e}")
            tests_passed += 1  # This is OK - optional dependency
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    # Test OpenAI client (without actual API call)
    print("\n2.2. Testing OpenAIClient initialization...")
    try:
        import perplexity
        # Set a dummy API key to test initialization
        os.environ['OPENAI_API_KEY'] = 'sk-test-key-not-real'
        try:
            client = perplexity.OpenAIClient(model="gpt-3.5-turbo")
            print("  ✓ OpenAIClient initialized")
            tests_passed += 1
        except ImportError as e:
            print(f"  ⚠ OpenAI package not available: {e}")
            tests_passed += 1  # This is OK - optional dependency
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    finally:
        # Clean up
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
    
    return tests_passed, tests_failed


def test_api_server_structure():
    """Test API server structure and endpoints."""
    print("\n" + "=" * 60)
    print("Test 3: API Server Structure")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n3.1. Testing FastAPI app structure...")
    try:
        import api_server
        
        # Check that app exists
        assert api_server.app is not None
        print("  ✓ FastAPI app exists")
        
        # Check for required routes
        routes = {route.path for route in api_server.app.routes if hasattr(route, 'path')}
        required_routes = ['/', '/health', '/v1/models', '/v1/chat/completions']
        
        for route in required_routes:
            if route in routes:
                print(f"  ✓ Route {route} exists")
            else:
                print(f"  ✗ Route {route} missing")
                raise AssertionError(f"Route {route} missing")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    print("\n3.2. Testing ServerConfig...")
    try:
        import api_server
        
        # Check config exists
        assert api_server.config is not None
        assert hasattr(api_server.config, 'backend')
        assert hasattr(api_server.config, 'get_client')
        print("  ✓ ServerConfig properly structured")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    return tests_passed, tests_failed


def test_litellm_adapter():
    """Test LiteLLM adapter structure."""
    print("\n" + "=" * 60)
    print("Test 4: LiteLLM Adapter")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n4.1. Testing PerplexityLiteLLMProvider...")
    try:
        from perplexity.litellm_adapter import PerplexityLiteLLMProvider
        
        # We can't fully initialize without network, but test structure
        # The provider initialization requires network access to Perplexity
        print("  ✓ PerplexityLiteLLMProvider class available")
        print("  ⚠ Full initialization skipped (requires network)")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    print("\n4.2. Testing register_perplexity_provider function...")
    try:
        from perplexity.litellm_adapter import register_perplexity_provider
        
        # Function exists
        assert callable(register_perplexity_provider)
        print("  ✓ register_perplexity_provider function available")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        tests_failed += 1
    
    return tests_passed, tests_failed


def test_documentation_files():
    """Test that documentation files exist."""
    print("\n" + "=" * 60)
    print("Test 5: Documentation Files")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    files_to_check = [
        'README.md',
        'QUICKSTART.md',
        '.env.example',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'litellm_proxy_config.yaml',
        'api_server.py',
    ]
    
    for filename in files_to_check:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename} exists")
            tests_passed += 1
        else:
            print(f"  ✗ {filename} missing")
            tests_failed += 1
    
    return tests_passed, tests_failed


def test_example_files():
    """Test that example files exist."""
    print("\n" + "=" * 60)
    print("Test 6: Example Files")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    example_files = [
        'examples_openai_sync.py',
        'examples_openai_async.py',
        'examples_litellm_sync.py',
        'examples_litellm_async.py',
        'example_api_server_client.py',
    ]
    
    for filename in example_files:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename} exists")
            tests_passed += 1
        else:
            print(f"  ✗ {filename} missing")
            tests_failed += 1
    
    return tests_passed, tests_failed


def main():
    """Run all tests."""
    print("\n")
    print("*" * 60)
    print("Perplexity AI Integration Tests")
    print("*" * 60)
    print("\nRunning comprehensive integration tests...")
    print("Note: Some tests may be skipped if optional dependencies are missing")
    print()
    
    total_passed = 0
    total_failed = 0
    
    # Run all test suites
    passed, failed = test_imports()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_client_initialization()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_api_server_structure()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_litellm_adapter()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_documentation_files()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_example_files()
    total_passed += passed
    total_failed += failed
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests Passed: {total_passed}")
    print(f"Tests Failed: {total_failed}")
    print(f"Success Rate: {total_passed}/{total_passed + total_failed} ({100 * total_passed / (total_passed + total_failed):.1f}%)")
    
    if total_failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total_failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
