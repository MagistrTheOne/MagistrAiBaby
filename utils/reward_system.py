import torch
import numpy as np
from utils.pattern_recognition import RewardCalculator

class RewardSystem:
    def __init__(self):
        self.reward_calculator = RewardCalculator()
        self.reward_history = []
        self.learning_rate = 0.1
        
        # Reward weights for different aspects
        self.weights = {
            'novelty': 0.3,
            'coherence': 0.2,
            'emotional': 0.2,
            'engagement': 0.15,
            'learning': 0.15
        }
        
        # Thresholds for different reward levels
        self.thresholds = {
            'excellent': 0.8,
            'good': 0.6,
            'neutral': 0.4,
            'poor': 0.2
        }
    
    def calculate_reward(self, interaction_data):
        """Calculate overall reward for an interaction"""
        total_reward = 0.0
        rewards = {}
        
        # Calculate novelty reward
        if 'response' in interaction_data:
            novelty_reward = self.reward_calculator.calculate_reward(
                interaction_data['response'],
                context=interaction_data.get('context')
            )
            rewards['novelty'] = novelty_reward * self.weights['novelty']
        
        # Calculate coherence reward
        if 'context' in interaction_data and 'response' in interaction_data:
            coherence_reward = self._calculate_coherence(
                interaction_data['context'],
                interaction_data['response']
            )
            rewards['coherence'] = coherence_reward * self.weights['coherence']
        
        # Calculate emotional reward
        if 'emotional_state' in interaction_data:
            emotional_reward = self._calculate_emotional_reward(
                interaction_data['emotional_state']
            )
            rewards['emotional'] = emotional_reward * self.weights['emotional']
        
        # Calculate engagement reward
        if 'user_engagement' in interaction_data:
            engagement_reward = self._calculate_engagement(
                interaction_data['user_engagement']
            )
            rewards['engagement'] = engagement_reward * self.weights['engagement']
        
        # Calculate learning reward
        if 'learning_progress' in interaction_data:
            learning_reward = self._calculate_learning_reward(
                interaction_data['learning_progress']
            )
            rewards['learning'] = learning_reward * self.weights['learning']
        
        # Calculate total reward
        total_reward = sum(rewards.values())
        
        # Store reward in history
        self.reward_history.append({
            'total': total_reward,
            'components': rewards
        })
        
        # Adjust weights based on reward history
        self._adjust_weights()
        
        return total_reward, rewards
    
    def _calculate_coherence(self, context, response):
        """Calculate coherence between context and response"""
        # Use pattern recognition to check if response follows learned patterns
        coherence_score = self.reward_calculator._calculate_pattern_match(
            response, context
        )
        return coherence_score
    
    def _calculate_emotional_reward(self, emotional_state):
        """Calculate reward based on emotional state"""
        # Reward balanced emotional states
        emotional_values = np.array(list(emotional_state.values()))
        
        # Calculate entropy of emotional distribution
        # Higher entropy means more balanced emotions
        entropy = -np.sum(emotional_values * np.log(emotional_values + 1e-10))
        normalized_entropy = entropy / np.log(len(emotional_values))
        
        return normalized_entropy
    
    def _calculate_engagement(self, engagement_data):
        """Calculate reward based on user engagement"""
        engagement_score = 0.0
        
        if 'response_time' in engagement_data:
            # Faster responses indicate higher engagement
            response_time = engagement_data['response_time']
            time_factor = np.exp(-response_time / 5.0)  # 5 second characteristic time
            engagement_score += 0.4 * time_factor
        
        if 'interaction_length' in engagement_data:
            # Longer interactions indicate higher engagement
            length = engagement_data['interaction_length']
            length_factor = min(length / 10.0, 1.0)  # Cap at 10 turns
            engagement_score += 0.3 * length_factor
        
        if 'user_initiative' in engagement_data:
            # Reward user taking initiative
            engagement_score += 0.3 * engagement_data['user_initiative']
        
        return engagement_score
    
    def _calculate_learning_reward(self, learning_data):
        """Calculate reward based on learning progress"""
        if 'error_reduction' in learning_data:
            # Reward error reduction
            error_reduction = learning_data['error_reduction']
            return np.clip(error_reduction, 0, 1)
        
        if 'knowledge_gain' in learning_data:
            # Reward knowledge acquisition
            return learning_data['knowledge_gain']
        
        return 0.0
    
    def _adjust_weights(self):
        """Adjust reward weights based on history"""
        if len(self.reward_history) < 10:
            return
        
        # Look at last 10 interactions
        recent_rewards = self.reward_history[-10:]
        component_averages = {}
        
        # Calculate average reward for each component
        for component in self.weights.keys():
            values = [r['components'].get(component, 0) for r in recent_rewards]
            component_averages[component] = np.mean(values)
        
        # Adjust weights to favor more reliable reward components
        total_average = sum(component_averages.values())
        if total_average > 0:
            new_weights = {
                component: (avg / total_average) * (1 - self.learning_rate) + 
                          weight * self.learning_rate
                for component, (weight, avg) in 
                zip(self.weights.keys(), zip(self.weights.values(), component_averages.values()))
            }
            
            # Normalize weights
            weight_sum = sum(new_weights.values())
            self.weights = {
                component: weight / weight_sum
                for component, weight in new_weights.items()
            }
    
    def get_reward_level(self, reward):
        """Get qualitative level of reward"""
        if reward >= self.thresholds['excellent']:
            return 'excellent'
        elif reward >= self.thresholds['good']:
            return 'good'
        elif reward >= self.thresholds['neutral']:
            return 'neutral'
        elif reward >= self.thresholds['poor']:
            return 'poor'
        else:
            return 'very_poor'
    
    def get_reward_summary(self):
        """Get summary of reward history"""
        if not self.reward_history:
            return None
            
        recent_rewards = self.reward_history[-50:]  # Last 50 interactions
        
        return {
            'average_reward': np.mean([r['total'] for r in recent_rewards]),
            'reward_trend': np.diff([r['total'] for r in recent_rewards])[-5:].tolist(),
            'component_weights': self.weights,
            'recent_levels': [
                self.get_reward_level(r['total'])
                for r in recent_rewards[-5:]
            ]
        }
