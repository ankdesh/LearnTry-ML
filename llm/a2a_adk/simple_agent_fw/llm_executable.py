import asyncio
import random
#import executable
from executable import SAFExecutable
from events import SAFEvent  
import a2a_types 
from typing import override

class LLMExecutable(SAFExecutable):
    def __init__(self):
        self.sentences = [
            "This is the first sentence.",
            "The quick brown rabbit jumps over the lazy frogs with no effort.",
            "Another day, another dollar.",
            "To be or not to be, that is the question.",
            "All that glitters is not gold.",
            "The only way to do great work is to love what you do.",
            "In three words I can sum up everything I've learned about life: it goes on."]
        
    @override 
    async def execute(self, input_event: SAFEvent) -> SAFEvent:
        # Ignore input_event for this dummy LLM, the core logic remains the same
        sentence = random.choice(self.sentences)

        # Create and return an SAFEvent
        output_event = SAFEvent(
            author=self.__class__.__name__,
            parts=[a2a_types.TextPart(text=sentence)],
            turn_complete=True,
            partial=False # Explicitly stating this is not a partial event
        )
        return output_event

async def main():
    llm_executable = LLMExecutable()
    input_event = SAFEvent(author="user", parts=[a2a_types.TextPart(text="Hello, how are you?")], turn_complete=True)
    output_event = await llm_executable.execute(input_event)
    print(output_event)

# Usage
if __name__ == "__main__":
    asyncio.run(main())


