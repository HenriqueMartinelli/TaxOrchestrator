from app.infrastructure.messaging.event_bus import EventBus

def on_order_processed(payload):
    print(f"[Metrics] Processed {payload['order_count']} orders, first_id={payload['first_order_id']}")

def on_order_failed(payload):
    print(f"[Alert] Order processing failed for file {payload['file']}: {payload['error']}")

EventBus.subscribe("order.processed", on_order_processed)
EventBus.subscribe("order.failed", on_order_failed)
