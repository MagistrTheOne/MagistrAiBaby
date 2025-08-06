import torch
import torch.nn as nn
from torch.optim import Adam
import numpy as np
from config.settings import LEARNING_RATE, BATCH_SIZE, WARMUP_STEPS

class LearningEngine:
    def __init__(self, brain, memory_system):
        self.brain = brain
        self.memory = memory_system
        self.optimizer = Adam(brain.parameters(), lr=LEARNING_RATE)
        self.steps = 0
        
    def compute_curiosity_reward(self, output, expected=None):
        """Calculate curiosity-driven reward"""
        if expected is None:
            # Intrinsic motivation - reward novel patterns
            novelty = torch.std(output['thoughts'])
            return novelty.item()
        else:
            # Extrinsic motivation - reward matching expected patterns
            similarity = -torch.nn.functional.mse_loss(output['thoughts'], expected)
            return similarity.item()
    
    def compute_emotional_reward(self, emotions):
        """Calculate emotion-based reward"""
        # Reward balanced emotional states
        emotional_stability = -torch.std(emotions)
        return emotional_stability.item()
    
    def update_brain(self, experiences, rewards):
        """Update brain weights based on experiences and rewards"""
        self.steps += 1
        
        # Learning rate warmup
        if self.steps < WARMUP_STEPS:
            lr = LEARNING_RATE * (self.steps / WARMUP_STEPS)
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = lr
        
        total_loss = 0
        self.optimizer.zero_grad()
        
        for experience, reward in zip(experiences, rewards):
            # Forward pass
            output = self.brain(experience)
            
            # Calculate losses
            curiosity_reward = self.compute_curiosity_reward(output)
            emotional_reward = self.compute_emotional_reward(output['emotions'])
            
            # Combine rewards
            combined_reward = reward + 0.3 * curiosity_reward + 0.2 * emotional_reward
            
            # Policy gradient loss
            policy_loss = -torch.mean(output['decisions'] * combined_reward)
            
            # Add regularization
            l2_reg = torch.tensor(0.)
            for param in self.brain.parameters():
                l2_reg += torch.norm(param)
            
            loss = policy_loss + 0.01 * l2_reg
            total_loss += loss
            
            # Store experience in memory
            self.memory.store_long_term(
                memory_type='experience',
                content={
                    'input': experience,
                    'output': {k: v.detach().numpy().tolist() for k, v in output.items()},
                    'reward': combined_reward
                },
                emotional_value=emotional_reward,
                importance=abs(combined_reward)
            )
        
        # Backward pass
        avg_loss = total_loss / len(experiences)
        avg_loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(self.brain.parameters(), max_norm=1.0)
        
        self.optimizer.step()
        
        return avg_loss.item()
    
    def learn_from_batch(self, input_batch):
        """Learn from a batch of inputs"""
        experiences = []
        rewards = []
        
        for input_data in input_batch:
            output = self.brain(input_data)
            reward = self.compute_curiosity_reward(output)
            
            experiences.append(input_data)
            rewards.append(reward)
            
            if len(experiences) >= BATCH_SIZE:
                loss = self.update_brain(experiences, rewards)
                experiences = []
                rewards = []
                
                # Store batch statistics
                self.memory.store_short_term(
                    f'learning_stats_{self.steps}',
                    {'loss': loss, 'steps': self.steps}
                )
    
    def learn_from_feedback(self, input_data, feedback_score):
        """Learn from external feedback"""
        output = self.brain(input_data)
        loss = self.update_brain([input_data], [feedback_score])
        
        # Store feedback experience with high importance
        self.memory.store_long_term(
            memory_type='feedback',
            content={
                'input': input_data,
                'output': {k: v.detach().numpy().tolist() for k, v in output.items()},
                'feedback_score': feedback_score
            },
            emotional_value=feedback_score,
            importance=0.8
        )
        
        return loss
