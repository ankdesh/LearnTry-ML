import unittest
from typing import Dict, Any, Optional, List

# Adjust the path if necessary, e.g., if simple_agent_fw is not in PYTHONPATH
# import sys
# import os
# import asyncio # No longer needed if only used for unittest.main()
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from session import InMemorySession
from events import SAFEvent  # Assuming SAFEvent is importable
from a2a_types import TextPart  # Import TextPart for creating event content
class TestInMemorySession(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session_id = "test_session_123"
        self.session = InMemorySession(session_id=self.session_id)

        # Sample events using SAFEvent
        self.event1 = SAFEvent(id="e1", author="user", parts=[
                               TextPart(text="Hello")])
        self.event2 = SAFEvent(id="e2", author="agent", parts=[
                               TextPart(text="Hi")], actions=None)
        self.event3 = SAFEvent(id="e3", author="user", parts=[TextPart(text="Question?")],
                               actions={"a2a_state_update": {"key": "value"}})
        self.event4 = SAFEvent(id="e4", author="system",
                               parts=[TextPart(text="Error")])
        self.event5 = SAFEvent(id="e5", author="agent", parts=[TextPart(text="Answer")],
                               actions={"a2a_state_update": {"key": "value"}})
        self.event6 = SAFEvent(id="e6", author="MyCustomAgent", parts=[
                               TextPart(text="Custom")])

    def test_initialization_empty_state(self):
        self.assertEqual(self.session.session_id, self.session_id)        
        self.assertEqual(self.session._events, [])
        self.assertEqual(self.session._state, {})

    async def test_initialization_with_initial_state(self):
        initial_state = {"user_name": "test_user", "theme": "dark"}
        session_with_state = InMemorySession(
            session_id="s2", initial_state=initial_state)
        self.assertEqual(session_with_state.session_id, "s2")
        self.assertEqual(await session_with_state.get_state(), initial_state)

        # Test that initial_state is copied, not referenced
        initial_state["new_key"] = "new_value"
        self.assertNotIn("new_key", await session_with_state.get_state())

    async def test_add_and_get_events(self):
        await self.session.add_event(self.event1)
        self.assertEqual(await self.session.get_events(), [self.event1])
        await self.session.add_event(self.event2)
        self.assertEqual(await self.session.get_events(), [self.event1, self.event2])

    async def test_get_events_returns_copy(self):
        await self.session.add_event(self.event1)
        events_list_copy = await self.session.get_events()
        # Check it's a different object
        self.assertIsNot(events_list_copy, self.session._events)
        events_list_copy.append(self.event2)
        # Original should be unchanged
        self.assertEqual(await self.session.get_events(), [self.event1])

    async def test_get_state_returns_copy(self):
        await self.session.update_state_value("key1", "value1")
        state_dict_copy = await self.session.get_state()
        # Check it's a different object
        self.assertIsNot(state_dict_copy, self.session._state)
        state_dict_copy["key2"] = "value2"
        # Original should be unchanged
        self.assertEqual(await self.session.get_state(), {"key1": "value1"})

    async def test_update_and_get_state_value(self):
        self.assertIsNone(await self.session.get_state_value("test_key"))
        await self.session.update_state_value("test_key", "test_value")
        self.assertEqual(await self.session.get_state_value(
            "test_key"), "test_value")
        await self.session.update_state_value("test_key", "new_value")
        self.assertEqual(await self.session.get_state_value("test_key"), "new_value")

    async def test_get_state_value_with_default(self):
        self.assertIsNone(await self.session.get_state_value("non_existent_key"))
        self.assertEqual(await self.session.get_state_value(
            "non_existent_key", "default_val"), "default_val")
        await self.session.update_state_value("existent_key", "actual_val")
        self.assertEqual(await self.session.get_state_value(
            "existent_key", "default_val"), "actual_val")

    async def test_get_events_by_author(self):
        await self.session.add_event(self.event1)  # user
        await self.session.add_event(self.event2)  # agent
        await self.session.add_event(self.event3)  # user
        self.assertEqual(await self.session.get_events_by_author(
            "user"), [self.event1, self.event3])
        self.assertEqual(await self.session.get_events_by_author(
            "agent"), [self.event2])
        self.assertEqual(
            await self.session.get_events_by_author("unknown_author"), [])

    async def test_get_events_with_actions(self):
        await self.session.add_event(self.event1)  # actions=None
        await self.session.add_event(self.event2)  # actions=None
        await self.session.add_event(self.event3)  # actions=self.actions_with_update
        self.assertEqual(await self.session.get_events_with_actions(), [self.event3])

    async def test_get_events_with_state_updates(self):
        await self.session.add_event(self.event1)  # actions=None
        # actions=self.actions_without_update (a2a_state_update=None)
        await self.session.add_event(self.event2)
        # actions=self.actions_with_update (a2a_state_update is not None)
        await self.session.add_event(self.event3)
        # actions=self.actions_with_update (a2a_state_update is not None)
        await self.session.add_event(self.event5)

        # Only events with a2a_state_update
        expected_events = [self.event3, self.event5]
        self.assertEqual(
            await self.session.get_events_with_state_updates(), expected_events)

    async def test_get_last_n_events(self):
        await self.session.add_event(self.event1)
        await self.session.add_event(self.event2)
        await self.session.add_event(self.event3)
        self.assertEqual(await self.session.get_last_n_events(2),
                         [self.event2, self.event3])
        self.assertEqual(await self.session.get_last_n_events(
            5), [self.event1, self.event2, self.event3])  # n > len
        self.assertEqual(await self.session.get_last_n_events(0), [])
        self.assertEqual(await self.session.get_last_n_events(1), [self.event3])

    async def test_get_last_user_event(self):
        self.assertIsNone(await self.session.get_last_user_event())
        await self.session.add_event(self.event2)  # agent
        self.assertIsNone(await self.session.get_last_user_event())
        await self.session.add_event(self.event1)  # user
        self.assertEqual(await self.session.get_last_user_event(), self.event1)
        await self.session.add_event(self.event4)  # system
        self.assertEqual(await self.session.get_last_user_event(), self.event1)
        await self.session.add_event(self.event3)  # user
        self.assertEqual(await self.session.get_last_user_event(), self.event3)

    async def test_get_last_agent_event(self):
        self.assertIsNone(await self.session.get_last_agent_event())
        await self.session.add_event(self.event1)  # user
        self.assertIsNone(await self.session.get_last_agent_event())
        await self.session.add_event(self.event2)  # agent
        self.assertEqual(await self.session.get_last_agent_event(), self.event2)
        await self.session.add_event(self.event3)  # user
        self.assertEqual(await self.session.get_last_agent_event(), self.event2)
        await self.session.add_event(self.event5)  # agent
        self.assertEqual(await self.session.get_last_agent_event(), self.event5)

        # Test with custom agent author name and case-insensitivity
        await self.session.add_event(self.event6)
        self.assertEqual(await self.session.get_last_agent_event(
            agent_author="MyCustomAgent"), self.event6)
        self.assertEqual(await self.session.get_last_agent_event(
            agent_author="mycustomagent"), self.event6)
        self.assertEqual(await self.session.get_last_agent_event(
            agent_author="MYCUSTOMAGENT"), self.event6)


if __name__ == '__main__':
    # This allows running the tests directly from the command line
    # python /home/ankdesh/explore/LearnTry-ML/llm/a2a_adk/tests/test_sessions.py
    unittest.main()
