"""Global configuration settings for the AI Baby Brain system."""

# Server Configuration
WS_HOST: str = "localhost"
WS_PORT: int = 8765

# Model Settings
TRANSFORMER_MODEL: str = "gpt2-medium"  # Base language model
WHISPER_MODEL: str = "base"  # Voice recognition model
LEARNING_RATE: float = 2e-4
BATCH_SIZE: int = 4
WARMUP_STEPS: int = 100

# Memory Settings
REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0

# SQLite Database
DATABASE_PATH: str = "data/brain_state/baby_memory.db"

# Personality Parameters
INITIAL_CURIOSITY: float = 0.8  # 0-1 scale
EMOTIONAL_STABILITY: float = 0.7  # 0-1 scale
LEARNING_EAGERNESS: float = 0.9  # 0-1 scale

# Training Parameters
MAX_SEQUENCE_LENGTH: int = 512
SAVE_INTERVAL: int = 1000  # Steps between saving brain state

# Voice Interface
VOICE_ENABLED: bool = True
DEFAULT_VOICE_LANG: str = "en"
VOICE_SPEED: int = 150  # Words per minute

# Data Paths
BRAIN_STATE_DIR: str = "data/brain_state"
MEMORIES_DIR: str = "data/memories"
ITERATIONS_DIR: str = "data/iterations"

# Development Settings
MIN_VOCABULARY_SIZE: int = 20
DEVELOPMENT_THRESHOLD: float = 0.3
MIN_AGE_FOR_MATURITY: int = 100

# Type definitions for better IDE support
# Make all settings available when importing from config
__all__ = [
    'WS_HOST',
    'WS_PORT',
    'TRANSFORMER_MODEL',
    'WHISPER_MODEL',
    'LEARNING_RATE',
    'BATCH_SIZE',
    'WARMUP_STEPS',
    'REDIS_HOST',
    'REDIS_PORT',
    'REDIS_DB',
    'DATABASE_PATH',
    'INITIAL_CURIOSITY',
    'EMOTIONAL_STABILITY',
    'LEARNING_EAGERNESS',
    'MAX_SEQUENCE_LENGTH',
    'SAVE_INTERVAL',
    'VOICE_ENABLED',
    'DEFAULT_VOICE_LANG',
    'VOICE_SPEED',
    'BRAIN_STATE_DIR',
    'MEMORIES_DIR',
    'ITERATIONS_DIR',
    'MIN_VOCABULARY_SIZE',
    'DEVELOPMENT_THRESHOLD',
    'MIN_AGE_FOR_MATURITY'
]
