#!/usr/bin/env python3
"""Test script for Stage 1: Configuration and Dependency Injection."""
import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.infrastructure.config import get_settings
from src.infrastructure.dependencies import get_container


async def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing configuration loading...")
    
    try:
        settings = get_settings()
        print(f"✅ App Name: {settings.app_name}")
        print(f"✅ Environment: {settings.environment}")
        print(f"✅ Debug: {settings.debug}")
        print(f"✅ Database URL: {settings.database_url}")
        print(f"✅ Redis URL: {settings.redis_url}")
        print(f"✅ API Host:Port: {settings.api_host}:{settings.api_port}")
        
        # Check required fields
        assert settings.secret_key, "SECRET_KEY is required"
        assert settings.database_name, "DATABASE_NAME is required"
        assert settings.database_user, "DATABASE_USER is required"
        assert settings.database_password, "DATABASE_PASSWORD is required"
        assert settings.telegram_bot_token, "TELEGRAM_BOT_TOKEN is required"
        
        print("✅ Configuration loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


async def test_dependency_injection():
    """Test dependency injection container."""
    print("\n🏗️ Testing dependency injection...")
    
    try:
        container = get_container()
        print(f"✅ Container created: {type(container).__name__}")
        
        # Test settings access
        settings = container.settings
        print(f"✅ Settings accessible: {settings.app_name}")
        
        # Test database factory
        db_factory = container.get_database_factory()
        print(f"✅ Database factory created: {type(db_factory).__name__}")
        
        print("✅ Dependency injection working!")
        return True
        
    except Exception as e:
        print(f"❌ DI Container error: {e}")
        return False


async def test_database_connection():
    """Test database connection (will fail if PostgreSQL is not running)."""
    print("\n🗄️ Testing database connection...")
    
    try:
        container = get_container()
        db_factory = container.get_database_factory()
        
        # Try to create engine (this doesn't actually connect yet)
        engine = db_factory.create_engine()
        print(f"✅ Database engine created: {engine}")
        
        # Try to create a connection (this will actually connect)
        try:
            connection = await db_factory.create_connection()
            print("✅ Database connection successful!")
            await connection.close()
            await db_factory.close()
            return True
        except Exception as conn_e:
            print(f"⚠️ Database connection failed (expected if PostgreSQL not running): {conn_e}")
            await db_factory.close()
            return False
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False


async def test_unit_of_work():
    """Test Unit of Work pattern (will fail if database not available)."""
    print("\n🔄 Testing Unit of Work...")
    
    try:
        container = get_container()
        
        # Test UoW context manager
        try:
            async with container.get_uow() as uow:
                print(f"✅ UoW created: {type(uow).__name__}")
                print(f"✅ User repository accessible: {type(uow.users).__name__}")
                print("✅ Unit of Work working!")
                return True
        except Exception as uow_e:
            print(f"⚠️ UoW failed (expected if database not running): {uow_e}")
            return False
            
    except Exception as e:
        print(f"❌ UoW setup error: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Testing Stage 1: Configuration and Dependency Injection\n")
    
    tests = [
        ("Configuration", test_configuration),
        ("Dependency Injection", test_dependency_injection),
        ("Database Connection", test_database_connection),
        ("Unit of Work", test_unit_of_work),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = await test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS:")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed >= 2:  # Config and DI should always pass
        print("\n🎉 Stage 1 is working! (Database tests may fail without PostgreSQL)")
        print("\n📝 Next steps:")
        print("1. Start PostgreSQL and Redis to test database connections")
        print("2. Update TELEGRAM_BOT_TOKEN in .env with real token")
        print("3. Run: python test_stage1.py")
        return True
    else:
        print("\n💥 Stage 1 has critical issues that need fixing!")
        return False


if __name__ == "__main__":
    asyncio.run(main()) 