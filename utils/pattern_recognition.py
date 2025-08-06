import numpy as np
import torch
import torch.nn as nn
from transformers import AutoTokenizer

class PatternMatcher:
    def __init__(self):
        self.patterns = {}
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
    
    def add_pattern(self, name, pattern_sequence):
        """Add a new pattern to recognize"""
        self.patterns[name] = self._encode_pattern(pattern_sequence)
    
    def _encode_pattern(self, pattern):
        """Encode pattern into embedding space"""
        return self.tokenizer(pattern, return_tensors="pt")

    def match(self, input_sequence, threshold=0.7):
        """Match input against known patterns"""
        input_encoded = self._encode_pattern(input_sequence)
        matches = {}
        
        for name, pattern in self.patterns.items():
            similarity = self._compute_similarity(input_encoded, pattern)
            if similarity > threshold:
                matches[name] = similarity
        
        return matches

    def _compute_similarity(self, seq1, seq2):
        """Compute similarity between two sequences"""
        # Using cosine similarity on token IDs
        ids1 = seq1['input_ids'].squeeze()
        ids2 = seq2['input_ids'].squeeze()
        
        # Pad sequences to same length
        max_len = max(len(ids1), len(ids2))
        ids1 = torch.nn.functional.pad(ids1, (0, max_len - len(ids1)))
        ids2 = torch.nn.functional.pad(ids2, (0, max_len - len(ids2)))
        
        similarity = torch.cosine_similarity(ids1.float(), ids2.float(), dim=0)
        return similarity.mean().item()

class PatternRecognition:
    def __init__(self):
        self.matcher = PatternMatcher()
        self.sequence_memory = []
        self.pattern_frequencies = {}
    
    def observe(self, sequence):
        """Observe and learn from a new sequence"""
        self.sequence_memory.append(sequence)
        
        # Look for recurring patterns
        if len(self.sequence_memory) > 1:
            new_patterns = self._find_recurring_patterns()
            for pattern in new_patterns:
                if pattern not in self.pattern_frequencies:
                    self.pattern_frequencies[pattern] = 1
                    self.matcher.add_pattern(f"learned_pattern_{len(self.pattern_frequencies)}", pattern)
                else:
                    self.pattern_frequencies[pattern] += 1
    
    def _find_recurring_patterns(self, min_length=3, max_length=10):
        """Find recurring patterns in the sequence memory"""
        patterns = set()
        
        # Convert sequences to token IDs for comparison
        tokenized_sequences = [
            self.matcher.tokenizer(seq, return_tensors="pt")['input_ids'].squeeze()
            for seq in self.sequence_memory[-10:]  # Look at last 10 sequences
        ]
        
        for seq1_idx in range(len(tokenized_sequences)):
            seq1 = tokenized_sequences[seq1_idx]
            
            for length in range(min_length, min(max_length, len(seq1) + 1)):
                for start in range(len(seq1) - length + 1):
                    pattern = seq1[start:start + length]
                    
                    # Look for this pattern in other sequences
                    pattern_found = False
                    for seq2_idx in range(seq1_idx + 1, len(tokenized_sequences)):
                        seq2 = tokenized_sequences[seq2_idx]
                        
                        for start2 in range(len(seq2) - length + 1):
                            if torch.all(seq2[start2:start2 + length] == pattern):
                                pattern_found = True
                                break
                        
                        if pattern_found:
                            # Decode pattern back to text
                            pattern_text = self.matcher.tokenizer.decode(pattern)
                            patterns.add(pattern_text)
                            break
        
        return patterns
    
    def recognize_patterns(self, sequence, threshold=0.7):
        """Recognize learned patterns in a sequence"""
        return self.matcher.match(sequence, threshold)
    
    def get_frequent_patterns(self, min_frequency=2):
        """Get patterns that occur frequently"""
        return {
            pattern: freq
            for pattern, freq in self.pattern_frequencies.items()
            if freq >= min_frequency
        }
    
class RewardCalculator:
    def __init__(self):
        self.pattern_recognition = PatternRecognition()
        self.novelty_memory = []
        self.curiosity_factor = 0.7
        self.consistency_factor = 0.3
    
    def calculate_reward(self, sequence, context=None):
        """Calculate reward based on novelty and pattern matching"""
        reward = 0.0
        
        # Novelty reward
        novelty_score = self._calculate_novelty(sequence)
        reward += self.curiosity_factor * novelty_score
        
        # Pattern matching reward
        if context:
            pattern_score = self._calculate_pattern_match(sequence, context)
            reward += self.consistency_factor * pattern_score
        
        # Update memory
        self.pattern_recognition.observe(sequence)
        self.novelty_memory.append(sequence)
        if len(self.novelty_memory) > 100:  # Keep memory bounded
            self.novelty_memory.pop(0)
        
        return reward
    
    def _calculate_novelty(self, sequence):
        """Calculate novelty of a sequence"""
        if not self.novelty_memory:
            return 1.0  # Maximum novelty for first sequence
            
        # Compare with recent memories
        similarities = []
        for memory in self.novelty_memory[-10:]:  # Compare with last 10 memories
            similarity = self.pattern_recognition.matcher._compute_similarity(
                self.pattern_recognition.matcher._encode_pattern(sequence),
                self.pattern_recognition.matcher._encode_pattern(memory)
            )
            similarities.append(similarity)
        
        # Novelty is inverse of maximum similarity
        return 1.0 - max(similarities)
    
    def _calculate_pattern_match(self, sequence, context):
        """Calculate how well sequence matches learned patterns in context"""
        matches = self.pattern_recognition.recognize_patterns(sequence)
        if not matches:
            return 0.0
            
        # Return average match strength
        return sum(matches.values()) / len(matches)
