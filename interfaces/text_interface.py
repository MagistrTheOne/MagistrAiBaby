import asyncio
from agents.cognitive_agent import CognitiveAgent

class TextInterface:
    def __init__(self):
        self.agent = CognitiveAgent()
        self.conversation_history = []
    
    async def process_message(self, message):
        """Process incoming message and generate response"""
        # Store message in history
        self.conversation_history.append({
            'role': 'user',
            'content': message
        })
        
        # Process through cognitive agent
        response = self.agent.process_input(message)
        
        # Convert neural output to text
        text_response = self._neural_to_text(response)
        
        # Store response in history
        self.conversation_history.append({
            'role': 'assistant',
            'content': text_response
        })
        
        return text_response
    
    def _neural_to_text(self, neural_output):
        """Convert neural network output to human-readable text"""
        thoughts = neural_output['thoughts']
        emotions = neural_output['emotions']
        decisions = neural_output['decisions']
        
        # Get personality influence
        personality_state = self.agent.get_personality_state()
        response_style = personality_state['traits']
        
        # Basic response template
        response = {
            'understanding': thoughts.mean().item(),
            'emotional_response': emotions.mean().item(),
            'action_tendency': decisions.mean().item()
        }
        
        # Apply personality style
        if response_style['curiosity'] > 0.7:
            response['questions'] = ['Tell me more?', 'What do you think?']
        
        if response_style['emotional_stability'] < 0.3:
            response['emotional_expression'] = '!'
        else:
            response['emotional_expression'] = '.'
            
        # Construct text response
        text = f"I understand {response['understanding']:.2f}"
        text += response['emotional_expression']
        
        if 'questions' in response:
            text += f" {' '.join(response['questions'])}"
        
        return text
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history
    
    def provide_feedback(self, feedback_score):
        """Provide feedback to the agent"""
        self.agent.receive_feedback(feedback_score)
    
    async def interactive_session(self):
        """Start an interactive text session"""
        print("Starting conversation (type 'exit' to end)")
        
        while True:
            user_input = input("> ")
            
            if user_input.lower() == 'exit':
                break
            
            response = await self.process_message(user_input)
            print(f"AI: {response}")
            
            # Optional feedback
            feedback = input("Feedback (-1 to 1, or press enter to skip): ")
            if feedback:
                try:
                    feedback_score = float(feedback)
                    if -1 <= feedback_score <= 1:
                        self.provide_feedback(feedback_score)
                except ValueError:
                    pass
            
            # Allow agent to rest periodically
            if len(self.conversation_history) % 10 == 0:
                print("Taking a moment to process...")
                self.agent.rest()

if __name__ == "__main__":
    interface = TextInterface()
    asyncio.run(interface.interactive_session())
