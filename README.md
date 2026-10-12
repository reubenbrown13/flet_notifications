# flet_notifications

`LocalNotifications` service for Flet 1.0+, based on
[flutter_local_notifications](https://pub.dev/packages/flutter_local_notifications).

Requires `flet>=1.0.0`. For Flet 0.27 use the 0.1.x releases.

## Usage

`LocalNotifications` is a non-visual **service**, not a visual control: do not
add it to `page.overlay` or `page.controls`.

```python
import flet as ft
from flet_notifications import LocalNotifications


async def main(page: ft.Page):
    notifications = LocalNotifications()
    # If your Flet version does not register services automatically,
    # add it explicitly:
    # page.services.append(notifications)

    await notifications.request_permissions()
    await notifications.show_notification(id=1, title="Hello", body="From Flet")


ft.run(main)
```

> Custom extensions need `flet build`. `flet run` alone shows "Unknown
> service" / "Unknown control" because it uses a prebuilt binary.

## Methods

All methods are coroutines and return `bool`. Each accepts an optional
`timeout` (seconds).

```python
await show_notification(id: int, title: str, body: str,
                        payload: str | None = None,
                        actions: list[NotificationAction] | None = None) -> bool

await schedule_notification(id: int, title: str, body: str,
                            scheduled_date: datetime,
                            payload: str | None = None,
                            actions: list[NotificationAction] | None = None) -> bool

await request_permissions() -> bool
```

## Notification actions

```python
from flet_notifications import LocalNotifications, NotificationAction

accept = NotificationAction(id="accept", title="Accept")
decline = NotificationAction(id="decline", title="Decline", destructive=True)

await notifications.show_notification(
    id=1,
    title="Meeting Invitation",
    body="Team meeting at 3:00 PM",
    actions=[accept, decline],
)
```

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `id` | `str` | | Reported back in the event. |
| `title` | `str` | | Button text. |
| `destructive` | `bool` | `False` | Destructive styling (iOS/macOS). |
| `foreground` | `bool` | `True` | Bring the app to the foreground when pressed. |

## Handling taps and actions

```python
def on_action(e: NotificationActionEvent):
    print(e.action_id, e.payload)   # action_id is "tap" for the notification body

notifications = LocalNotifications(on_notification_action=on_action)
```

`e.action_id` is the pressed `NotificationAction.id`, or `"tap"` when the
notification itself was tapped. `e.payload` is the payload passed when the
notification was created (empty string if none).

## Migrating from 0.1.x (Flet 0.27)

- Requires `flet>=1.0.0`.
- Do not add `LocalNotifications` to `page.overlay`.
- Handlers receive `NotificationActionEvent` (`e.action_id`, `e.payload`)
  instead of `e.data["actionId"]`.
- Methods return real booleans.

Notification actions may look different per platform. On iOS/macOS the
buttons currently come from a fixed built-in category.
