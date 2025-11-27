#!/usr/bin/env python
"""
Script to test Celery and Redis connectivity
Run this inside the Django container: docker exec -it django_app python test_celery_redis.py
"""

import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')
sys.path.insert(0, '/app')
django.setup()

from django.conf import settings
import redis


def test_redis_connection():
    """Test direct Redis connection"""
    print("\n=== Testing Direct Redis Connection ===")
    try:
        # Extract host and port from REDIS_URL
        redis_url = settings.CACHES['default']['LOCATION']
        print(f"Redis URL: {redis_url}")

        # Connect to Redis
        r = redis.from_url(redis_url)

        # Test ping
        if r.ping():
            print("✓ Redis connection successful!")

        # Test set/get
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        if value == b'test_value':
            print("✓ Redis read/write successful!")
            r.delete('test_key')

        # Get info
        info = r.info()
        print(f"✓ Redis version: {info['redis_version']}")
        print(f"✓ Connected clients: {info['connected_clients']}")

        return True
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        return False


def test_celery_connection():
    """Test Celery broker connection"""
    print("\n=== Testing Celery Broker Connection ===")
    try:
        from config.celery import app

        print(f"Broker URL: {app.conf.broker_url}")
        print(f"Result Backend: {app.conf.result_backend}")

        # Inspect Celery
        inspect = app.control.inspect()

        # Check active workers
        active_workers = inspect.active()
        if active_workers:
            print(f"✓ Active Celery workers found: {list(active_workers.keys())}")
        else:
            print("⚠ No active Celery workers found (this is expected if worker isn't running)")

        # Test broker connection
        conn = app.connection()
        conn.connect()
        if conn.connected:
            print("✓ Celery broker connection successful!")
            conn.release()
            return True
        else:
            print("✗ Celery broker connection failed")
            return False

    except Exception as e:
        print(f"✗ Celery connection failed: {e}")
        return False


def test_celery_task():
    """Test a simple Celery task"""
    print("\n=== Testing Celery Task Execution ===")
    try:
        from assistant.tasks import check_profanity

        # Send a test task
        result = check_profanity.delay("test text")
        print(f"✓ Task sent successfully! Task ID: {result.id}")
        time.sleep(1)
        print(f"  Task state: {result.state}")

        # Note: Task won't complete without a worker running
        if result.state == 'PENDING':
            print("  ⚠ Task is pending (worker needed to process)")

        return True
    except Exception as e:
        print(f"✗ Task execution failed: {e}")
        return False


def main():
    print("=" * 60)
    print("Celery & Redis Connection Test")
    print("=" * 60)

    redis_ok = test_redis_connection()
    celery_ok = test_celery_connection()
    task_ok = test_celery_task()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Redis Connection: {'✓ PASS' if redis_ok else '✗ FAIL'}")
    print(f"  Celery Connection: {'✓ PASS' if celery_ok else '✗ FAIL'}")
    print(f"  Task Dispatch: {'✓ PASS' if task_ok else '✗ FAIL'}")
    print("=" * 60)

    if redis_ok and celery_ok:
        print("\n✓ All connections working! Start celery worker to process tasks.")
    else:
        print("\n✗ Some connections failed. Check configuration.")


if __name__ == '__main__':
    main()
