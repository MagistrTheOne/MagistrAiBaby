import torch
import torch.nn as nn
import logging
from transformers import AutoModel, AutoTokenizer
from config.settings import (
    TRANSFORMER_MODEL,
    MAX_SEQUENCE_LENGTH,
    MODEL_DIM,
    NUM_LAYERS,
    HIDDEN_DIM,
    DROPOUT_RATE
)

class PerceptionLayer(nn.Module):
    """
    Encapsulates the perception (input encoding) stage for the AI baby brain.
    Handles transformer-based feature extraction and attention.
    """
    def __init__(self) -> None:
        super().__init__()
        try:
            self.transformer = AutoModel.from_pretrained(TRANSFORMER_MODEL)
            self.tokenizer = AutoTokenizer.from_pretrained(TRANSFORMER_MODEL)
        except Exception as e:
            logging.warning(f"Error loading transformer model: {e}, falling back to distilgpt2")
            self.transformer = AutoModel.from_pretrained("distilgpt2")
            self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        self.attention = nn.MultiheadAttention(
            embed_dim=self.transformer.config.hidden_size,
            num_heads=8,
            batch_first=True
        )

    def encode(self, input_text: str) -> dict:
        """Tokenize input text for the transformer."""
        return self.tokenizer(
            input_text,
            padding=True,
            truncation=True,
            max_length=MAX_SEQUENCE_LENGTH,
            return_tensors="pt"
        )

    def forward(self, tokens: dict) -> torch.Tensor:
        """Forward pass through transformer and attention."""
        with torch.no_grad():
            perception_output = self.transformer(**tokens)[0]
        attention_output, _ = self.attention(
            perception_output,
            perception_output,
            perception_output
        )
        return attention_output

class BabyBrain(nn.Module):
    """
    Main neural architecture for the AI baby brain.
    Handles perception, language, emotion, and decision layers.
    """
    def __init__(self) -> None:
        super().__init__()
        self.perception = PerceptionLayer()
        hidden_size = self.perception.transformer.config.hidden_size
        self.language_layer = nn.Sequential(
            nn.Linear(hidden_size, HIDDEN_DIM),
            nn.ReLU(),
            nn.Dropout(DROPOUT_RATE),
            nn.Linear(HIDDEN_DIM, MODEL_DIM)
        )
        self.emotional_layer = nn.Sequential(
            nn.Linear(MODEL_DIM, HIDDEN_DIM),
            nn.ReLU(),
            nn.Dropout(DROPOUT_RATE),
            nn.Linear(HIDDEN_DIM, 3)  # Valence, Arousal, Dominance
        )
        self.decision_layer = nn.Sequential(
            nn.Linear(MODEL_DIM + 3, HIDDEN_DIM),
            nn.ReLU(),
            nn.Dropout(DROPOUT_RATE),
            nn.Linear(HIDDEN_DIM, MODEL_DIM)
        )

    def forward(self, input_text: str) -> dict:
        """
        Forward pass for the AI baby brain.
        Returns a dict with thoughts, emotions, and decisions tensors.
        """
        tokens = self.perception.encode(input_text)
        perception_output = self.perception(tokens)
        language_features = self.language_layer(perception_output.mean(dim=1))
        emotions = self.emotional_layer(language_features)
        combined_features = torch.cat([language_features, emotions], dim=-1)
        decisions = self.decision_layer(combined_features)
        return {
            'thoughts': language_features,
            'emotions': emotions,
            'decisions': decisions
        }
