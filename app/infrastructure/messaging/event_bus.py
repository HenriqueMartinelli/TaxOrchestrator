from typing import Callable, Any, Dict, List

class EventBus:
    _subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    @classmethod
    def subscribe(cls, event_type: str, handler: Callable[[Any], None]):
        cls._subscribers.setdefault(event_type, []).append(handler)

    @classmethod
    def publish(cls, event_type: str, payload: Any):
        for handler in cls._subscribers.get(event_type, []):
            handler(payload)
