## 0.2.0

* Port to Flet 1.0 (`flet>=1.0.0`). **Breaking changes:**
  * `LocalNotifications` is now an `ft.Service`; it is no longer added to
    `page.overlay`.
  * `on_notification_action` handlers receive a `NotificationActionEvent`
    with `e.action_id` and `e.payload` (previously `e.data["actionId"]`).
  * `NotificationAction` is a plain dataclass (same constructor arguments).
* `show_notification`, `schedule_notification` and `request_permissions` now
  return real booleans, and accept an optional `timeout`.
* Removed the old `createControl` / `create_control.dart` registration.

## 0.1.0

* TODO: Describe initial release.
