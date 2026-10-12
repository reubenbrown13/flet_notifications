from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

import flet as ft

__all__ = ["LocalNotifications", "NotificationAction", "NotificationActionEvent"]


@dataclass
class NotificationAction:
    """An action button shown on a notification."""

    id: str
    """Unique identifier reported back in `on_notification_action`."""

    title: str
    """Text displayed on the button."""

    destructive: bool = False
    """Whether the action is destructive (shown in red on iOS/macOS)."""

    foreground: bool = True
    """Whether tapping the action brings the app to the foreground."""

    def _to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "destructive": self.destructive,
            "foreground": self.foreground,
        }


@dataclass
class NotificationActionEvent(ft.Event["LocalNotifications"]):
    """A notification (or one of its action buttons) was tapped."""

    action_id: str
    """The `NotificationAction.id` that was pressed, or `"tap"` when the
    notification body itself was tapped."""

    payload: str
    """The payload the notification was created with (empty string if none)."""


@ft.control("LocalNotifications")
class LocalNotifications(ft.Service):
    """
    Local notifications, based on the `flutter_local_notifications` package.

    This is a non-visual service control. Methods are coroutines and must be
    awaited.
    """

    on_notification_action: Optional[ft.EventHandler[NotificationActionEvent]] = None
    """Called when the user taps a notification or one of its action buttons."""

    async def show_notification(
        self,
        id: int,
        title: str,
        body: str,
        payload: Optional[str] = None,
        actions: Optional[list[NotificationAction]] = None,
        timeout: Optional[float] = None,
    ) -> bool:
        """
        Show a notification immediately.

        Returns:
            `True` if the notification was shown, `False` otherwise.
        """
        result = await self._invoke_method(
            "show_notification",
            {
                "id": id,
                "title": title,
                "body": body,
                "payload": payload,
                "actions": [a._to_dict() for a in actions] if actions else None,
            },
            timeout=timeout,
        )
        return bool(result)

    async def schedule_notification(
        self,
        id: int,
        title: str,
        body: str,
        scheduled_date: datetime,
        payload: Optional[str] = None,
        actions: Optional[list[NotificationAction]] = None,
        timeout: Optional[float] = None,
    ) -> bool:
        """
        Schedule a notification for a future date and time.

        Returns:
            `True` if the notification was scheduled, `False` otherwise.
        """
        result = await self._invoke_method(
            "schedule_notification",
            {
                "id": id,
                "title": title,
                "body": body,
                "scheduled_date": scheduled_date.isoformat(),
                "payload": payload,
                "actions": [a._to_dict() for a in actions] if actions else None,
            },
            timeout=timeout,
        )
        return bool(result)

    async def request_permissions(self, timeout: Optional[float] = None) -> bool:
        """
        Ask the user for permission to show notifications.

        Returns:
            `True` if permission was granted, `False` otherwise.
        """
        return bool(await self._invoke_method("request_permissions", timeout=timeout))
