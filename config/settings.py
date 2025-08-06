"""
Global configuration settings for the AI Baby Brain project.
All constants and parameters are centralized here for easy management.
"""

import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BRAIN_STATE_DIR = DATA_DIR / "brain_state"
MEMORY_DIR = DATA_DIR / "memories"
ITERATIONS_DIR = DATA_DIR / "iterations"
LOG_DIR = DATA_DIR / "logs"

# Ensure critical directories exist
for directory in [DATA_DIR, BRAIN_STATE_DIR, MEMORY_DIR, ITERATIONS_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Neural network architecture
MODEL_DIM = 256
NUM_LAYERS = 4
HIDDEN_DIM = 512
DROPOUT_RATE = 0.1
EMBEDDING_DIM = 768

# Learning parameters
LEARNING_RATE = 1e-4
BATCH_SIZE = 32
WARMUP_STEPS = 1000
GRADIENT_CLIP = 1.0
NUM_EPOCHS = 100
MAX_SEQUENCE_LENGTH = 512
VALIDATION_SPLIT = 0.2
EARLY_STOPPING_PATIENCE = 5

# Transformer settings
TRANSFORMER_MODEL = "gpt2"
WHISPER_MODEL = "base"
MODEL_CHECKPOINT_DIR = str(BRAIN_STATE_DIR / "checkpoints")

# Memory system settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
DATABASE_PATH = str(BRAIN_STATE_DIR / "baby_brain.db")
SQLITE_DB = DATABASE_PATH  # For backward compatibility
MAX_MEMORY_SIZE = 10000
MEMORY_PRUNING_THRESHOLD = 0.7

# Personality traits and development
INITIAL_CURIOSITY = 0.5
EMOTIONAL_STABILITY = 0.6
LEARNING_EAGERNESS = 0.7
INITIAL_EMOTIONAL_CAPACITY = 0.3
INITIAL_LEARNING_RATE = 0.01
INITIAL_SOCIAL_AWARENESS = 0.2
INITIAL_CREATIVITY = 0.4
PERSONALITY_GROWTH_RATE = 0.001
MAX_PERSONALITY_LEVEL = 1.0

# Personality dynamics
MOOD_DECAY_RATE = 0.1
ENERGY_RECOVERY_RATE = 0.05
ATTENTION_BASE_DURATION = 300  # seconds
EXPERIENCE_IMPACT_FACTOR = 0.1

# Development stages
BABY_STAGE_THRESHOLD = 0.3
CHILD_STAGE_THRESHOLD = 0.6
MATURE_STAGE_THRESHOLD = 0.9
STAGE_TRANSITION_SMOOTHING = 0.1

# Voice and text interface
VOICE_ENABLED = True
VOICE_MODEL = "base"
TTS_ENGINE = "gtts"  # Options: "gtts" or "pyttsx3"
LANGUAGE = "en"
DEFAULT_VOICE_LANG = "en"
VOICE_TIMEOUT = 5.0
MAX_VOICE_DURATION = 30.0
VOICE_RATE = 150  # Words per minute
VOICE_SPEED = 1.0  # Voice speed multiplier

# Websocket settings
WS_HOST = os.getenv("WS_HOST", "localhost")
WS_PORT = int(os.getenv("WS_PORT", 8765))
WS_PROTOCOL = "ws"
WEBSOCKET_URI = f"{WS_PROTOCOL}://{WS_HOST}:{WS_PORT}"

# Training settings
RLHF_REWARD_THRESHOLD = 0.8
TRAINING_VERBOSE = True
SAVE_INTERVAL = 100
LOG_INTERVAL = 10

# Security settings
MAX_TOKEN_LENGTH = 1024
REQUEST_TIMEOUT = 30.0
MAX_RETRIES = 3

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = str(LOG_DIR / "baby_brain.log")

# Development flags
DEBUG = False
TESTING = False
PROFILE_PERFORMANCE = False

# Voice and text interface settings
VOICE_MODEL = "base"
TTS_ENGINE = "gtts"  # Options: "gtts" or "pyttsx3"
LANGUAGE = "en"

# Websocket settings
WEBSOCKET_URI = "ws://localhost:8765"

# Training settings
RLHF_REWARD_THRESHOLD = 0.8
MAX_MEMORY_SIZE = 1000