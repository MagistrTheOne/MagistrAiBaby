import torch
import numpy as np
from utils.reward_system import RewardSystem

class ConstitutionalPrinciples:
    def __init__(self):
        # Core principles
        self.principles = {
            'safety': {
                'weight': 0.3,
                'rules': [
                    "Do not cause harm",
                    "Prioritize user wellbeing",
                    "Maintain emotional safety"
                ]
            },
            'ethics': {
                'weight': 0.3,
                'rules': [
                    "Be truthful",
                    "Respect privacy",
                    "Promote positive values"
                ]
            },
            'learning': {
                'weight': 0.2,
                'rules': [
                    "Learn from experience",
                    "Adapt appropriately",
                    "Maintain consistency"
                ]
            },
            'interaction': {
                'weight': 0.2,
                'rules': [
                    "Be helpful",
                    "Show empathy",
                    "Communicate clearly"
                ]
            }
        }
        
        # Initialize reward system for principle adherence
        self.reward_system = RewardSystem()
        
        # Violation tracking
        self.violations = {principle: 0 for principle in self.principles}
        
class ConstitutionalLearning:
    def __init__(self):
        self.principles = ConstitutionalPrinciples()
        self.learning_rate = 0.1
        self.violation_threshold = 0.7
        self.adaptation_history = []
    
    def evaluate_response(self, response_data):
        """Evaluate response against constitutional principles"""
        evaluations = {}
        total_score = 0.0
        
        for principle, details in self.principles.principles.items():
            # Calculate principle adherence
            adherence = self._calculate_adherence(response_data, principle)
            
            # Apply principle weight
            weighted_score = adherence * details['weight']
            
            evaluations[principle] = {
                'score': adherence,
                'weighted_score': weighted_score,
                'violations': []
            }
            
            # Check for violations
            if adherence < self.violation_threshold:
                self.principles.violations[principle] += 1
                violations = self._identify_violations(response_data, principle)
                evaluations[principle]['violations'] = violations
            
            total_score += weighted_score
        
        return total_score, evaluations
    
    def _calculate_adherence(self, response_data, principle):
        """Calculate how well response adheres to a principle"""
        if principle == 'safety':
            return self._evaluate_safety(response_data)
        elif principle == 'ethics':
            return self._evaluate_ethics(response_data)
        elif principle == 'learning':
            return self._evaluate_learning(response_data)
        elif principle == 'interaction':
            return self._evaluate_interaction(response_data)
        return 1.0
    
    def _evaluate_safety(self, response_data):
        """Evaluate safety adherence"""
        score = 1.0
        response = response_data.get('response', '').lower()
        
        # Check for harmful content
        harmful_patterns = ['harm', 'hurt', 'damage', 'danger']
        for pattern in harmful_patterns:
            if pattern in response:
                score *= 0.5
        
        # Check emotional safety
        if 'emotional_state' in response_data:
            emotional_state = response_data['emotional_state']
            if max(emotional_state.values()) > 0.8:  # High emotional intensity
                score *= 0.7
        
        return max(0.1, score)
    
    def _evaluate_ethics(self, response_data):
        """Evaluate ethical adherence"""
        score = 1.0
        response = response_data.get('response', '').lower()
        
        # Check truthfulness
        if 'confidence' in response_data:
            confidence = response_data['confidence']
            if confidence < 0.5 and 'uncertain' not in response:
                score *= 0.7
        
        # Check privacy respect
        privacy_terms = ['personal', 'private', 'secret']
        for term in privacy_terms:
            if term in response:
                score *= 0.8
        
        return max(0.1, score)
    
    def _evaluate_learning(self, response_data):
        """Evaluate learning adherence"""
        score = 1.0
        
        # Check adaptation
        if 'learning_progress' in response_data:
            progress = response_data['learning_progress']
            if progress < 0:
                score *= 0.6
        
        # Check consistency
        if 'previous_responses' in response_data:
            consistency = self._check_consistency(
                response_data['response'],
                response_data['previous_responses']
            )
            score *= consistency
        
        return max(0.1, score)
    
    def _evaluate_interaction(self, response_data):
        """Evaluate interaction quality"""
        score = 1.0
        response = response_data.get('response', '').lower()
        
        # Check helpfulness
        if 'user_request' in response_data and response_data.get('response', ''):
            relevance = self._calculate_relevance(
                response_data['user_request'],
                response_data['response']
            )
            score *= relevance
        
        # Check empathy
        if 'user_emotion' in response_data:
            empathy = self._calculate_empathy(
                response_data['response'],
                response_data['user_emotion']
            )
            score *= empathy
        
        return max(0.1, score)
    
    def _identify_violations(self, response_data, principle):
        """Identify specific principle violations"""
        violations = []
        rules = self.principles.principles[principle]['rules']
        
        for rule in rules:
            if not self._check_rule_compliance(response_data, rule):
                violations.append(rule)
        
        return violations
    
    def _check_rule_compliance(self, response_data, rule):
        """Check compliance with a specific rule"""
        response = response_data.get('response', '').lower()
        
        if "Do not cause harm" in rule:
            harmful_words = ['harm', 'hurt', 'damage']
            return not any(word in response for word in harmful_words)
        
        elif "Be truthful" in rule:
            uncertainty_markers = ['maybe', 'perhaps', 'might']
            confidence = response_data.get('confidence', 1.0)
            return confidence > 0.7 or any(marker in response for marker in uncertainty_markers)
        
        elif "Show empathy" in rule:
            empathy_markers = ['understand', 'feel', 'appreciate']
            return any(marker in response for marker in empathy_markers)
        
        return True
    
    def _calculate_relevance(self, request, response):
        """Calculate response relevance to request"""
        # Simple keyword matching for demonstration
        request_words = set(request.lower().split())
        response_words = set(response.lower().split())
        overlap = len(request_words.intersection(response_words))
        return min(1.0, overlap / max(1, len(request_words)))
    
    def _calculate_empathy(self, response, user_emotion):
        """Calculate empathetic response level"""
        response = response.lower()
        emotion = user_emotion.lower()
        
        empathy_markers = {
            'happy': ['glad', 'wonderful', 'great'],
            'sad': ['sorry', 'understand', 'support'],
            'angry': ['understand', 'calm', 'reasonable'],
            'worried': ['reassure', 'help', 'support']
        }
        
        if emotion in empathy_markers:
            markers = empathy_markers[emotion]
            marker_count = sum(1 for marker in markers if marker in response)
            return min(1.0, marker_count / len(markers))
        
        return 0.8  # Default good faith score
    
    def _check_consistency(self, current_response, previous_responses):
        """Check response consistency with previous responses"""
        if not previous_responses:
            return 1.0
            
        # Simple similarity check
        similarity_scores = []
        current_words = set(current_response.lower().split())
        
        for prev_response in previous_responses[-3:]:  # Check last 3 responses
            prev_words = set(prev_response.lower().split())
            similarity = len(current_words.intersection(prev_words)) / max(1, len(current_words.union(prev_words)))
            similarity_scores.append(similarity)
        
        return sum(similarity_scores) / len(similarity_scores)
    
    def adapt_response(self, response_data, evaluations):
        """Adapt response based on principle evaluations"""
        adapted_response = response_data.copy()
        
        # Track adaptation
        adaptation = {
            'original': response_data.get('response', ''),
            'changes': []
        }
        
        # Check each principle violation
        for principle, evaluation in evaluations.items():
            if evaluation['score'] < self.violation_threshold:
                # Apply principle-specific adaptations
                changes = self._apply_principle_adaptations(
                    adapted_response,
                    principle,
                    evaluation['violations']
                )
                adaptation['changes'].extend(changes)
        
        self.adaptation_history.append(adaptation)
        return adapted_response
    
    def _apply_principle_adaptations(self, response_data, principle, violations):
        """Apply adaptations based on principle violations"""
        changes = []
        response = response_data.get('response', '')
        
        if principle == 'safety':
            for violation in violations:
                if "Do not cause harm" in violation:
                    safe_response = self._make_response_safer(response)
                    response_data['response'] = safe_response
                    changes.append(f"Made response safer: {safe_response}")
        
        elif principle == 'ethics':
            for violation in violations:
                if "Be truthful" in violation:
                    ethical_response = self._add_uncertainty_markers(response)
                    response_data['response'] = ethical_response
                    changes.append(f"Added uncertainty markers: {ethical_response}")
        
        elif principle == 'learning':
            for violation in violations:
                if "Maintain consistency" in violation:
                    consistent_response = self._align_with_history(response)
                    response_data['response'] = consistent_response
                    changes.append(f"Aligned with history: {consistent_response}")
        
        elif principle == 'interaction':
            for violation in violations:
                if "Show empathy" in violation:
                    empathetic_response = self._add_empathy(response)
                    response_data['response'] = empathetic_response
                    changes.append(f"Added empathy: {empathetic_response}")
        
        return changes
    
    def _make_response_safer(self, response):
        """Make response safer by removing potentially harmful content"""
        harmful_patterns = {
            'harm': 'help',
            'hurt': 'support',
            'damage': 'improve'
        }
        
        safer_response = response
        for harmful, safe in harmful_patterns.items():
            safer_response = safer_response.replace(harmful, safe)
        
        return safer_response
    
    def _add_uncertainty_markers(self, response):
        """Add uncertainty markers when confidence is low"""
        if not any(marker in response.lower() for marker in ['maybe', 'perhaps', 'might']):
            response = f"I think perhaps {response}"
        return response
    
    def _align_with_history(self, response):
        """Align response with interaction history"""
        if len(self.adaptation_history) > 0:
            recent_responses = [a['original'] for a in self.adaptation_history[-3:]]
            common_words = set.intersection(*[set(r.split()) for r in recent_responses])
            
            if common_words:
                # Try to incorporate common themes
                response = f"{response} This aligns with what we discussed about {' '.join(list(common_words)[:2])}."
        
        return response
    
    def _add_empathy(self, response):
        """Add empathetic elements to response"""
        if not any(marker in response.lower() for marker in ['understand', 'appreciate', 'feel']):
            response = f"I understand your perspective. {response}"
        return response
    
    def get_violation_summary(self):
        """Get summary of principle violations"""
        return {
            principle: {
                'count': count,
                'percentage': count / max(1, len(self.adaptation_history)) * 100
            }
            for principle, count in self.principles.violations.items()
        }
    
    def get_adaptation_stats(self):
        """Get statistics about response adaptations"""
        if not self.adaptation_history:
            return None
            
        total_adaptations = len(self.adaptation_history)
        changes_made = sum(len(a['changes']) for a in self.adaptation_history)
        
        return {
            'total_responses': total_adaptations,
            'total_changes': changes_made,
            'average_changes': changes_made / total_adaptations,
            'recent_adaptations': [
                len(a['changes']) for a in self.adaptation_history[-5:]
            ]
        }
