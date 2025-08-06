#!/usr/bin/env python3
import os
import sys

def setup_environment():
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

if __name__ == "__main__":
    setup_environment()
    
    # Import and run the main application
    from main import main
    import asyncio
    
    # Run the async main function
    asyncio.run(main())
