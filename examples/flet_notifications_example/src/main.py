from datetime import datetime, timedelta

import flet as ft
from flet_notifications import (
    LocalNotifications,
    NotificationAction,
    NotificationActionEvent,
)


async def main(page: ft.Page):
    page.title = "Flet Notifications Example"
    page.theme_mode = ft.ThemeMode.DARK

    # Set iOS-like padding for the page
    page.padding = 20
    page.window.width = 400
    page.window.height = 700
    page.scroll = ft.ScrollMode.ADAPTIVE

    def show_message(text: str, bgcolor: ft.ColorValue):
        page.show_dialog(ft.SnackBar(content=ft.Text(text), bgcolor=bgcolor))

    # Handle notification taps and action buttons
    async def on_notification_action(e: NotificationActionEvent):
        message = f"Action '{e.action_id}' received with payload: {e.payload}"
        action_text.value = message
        action_text.color = None
        show_message(message, ft.Colors.BLUE)
        page.update()

    # LocalNotifications is a service: creating it registers it with the page,
    # so it must not be added to page.controls or page.overlay.
    notifications = LocalNotifications(
        on_notification_action=on_notification_action,
    )

    def build_actions() -> list[NotificationAction] | None:
        actions = []
        if accept_checkbox.value:
            actions.append(
                NotificationAction(id="accept", title="Accept", foreground=True)
            )
        if decline_checkbox.value:
            actions.append(
                NotificationAction(
                    id="decline", title="Decline", destructive=True, foreground=False
                )
            )
        if view_checkbox.value:
            actions.append(
                NotificationAction(id="view", title="View", foreground=True)
            )
        return actions or None

    def notification_id() -> int:
        value = id_field.value
        return int(value) if value and value.isdigit() else 0

    # Request notification permissions
    async def request_permissions(e):
        granted = await notifications.request_permissions()
        show_message(
            f"Permissions {'granted' if granted else 'denied'}!",
            ft.Colors.BLUE_ACCENT if granted else ft.Colors.RED_ACCENT,
        )

    # Show an immediate notification
    async def show_notification(e):
        result = await notifications.show_notification(
            notification_id(),
            title_field.value or "Test Notification",
            body_field.value or "This is a test message",
            payload=payload_field.value,
            actions=build_actions(),
        )
        show_message(
            f"Notification {'sent successfully' if result else 'not sent'}",
            ft.Colors.GREEN_ACCENT if result else ft.Colors.RED_ACCENT,
        )

    # Schedule a notification 10 seconds in the future
    async def schedule_notification(e):
        scheduled_time = datetime.now() + timedelta(seconds=10)
        result = await notifications.schedule_notification(
            notification_id(),
            title_field.value or "Scheduled Notification",
            body_field.value or "This notification was scheduled",
            scheduled_time,
            payload=payload_field.value,
            actions=build_actions(),
        )
        if result:
            show_message(
                f"Notification scheduled for {scheduled_time.strftime('%H:%M:%S')}",
                ft.Colors.GREEN_ACCENT,
            )
        else:
            show_message("Notification could not be scheduled", ft.Colors.RED_ACCENT)

    # Create input fields with Cupertino style
    id_field = ft.CupertinoTextField(
        placeholder_text="Notification ID",
        value="0",
        border_radius=ft.BorderRadius.all(8),
    )

    title_field = ft.CupertinoTextField(
        placeholder_text="Title",
        value="Test Notification",
        border_radius=ft.BorderRadius.all(8),
    )

    body_field = ft.CupertinoTextField(
        placeholder_text="Body",
        value="This is a test message",
        border_radius=ft.BorderRadius.all(8),
        max_lines=3,
    )

    payload_field = ft.CupertinoTextField(
        placeholder_text="Payload (optional)",
        value="test-payload-123",
        border_radius=ft.BorderRadius.all(8),
    )

    # Create checkboxes for notification actions
    accept_checkbox = ft.Checkbox(label="Include 'Accept' action", value=True)
    decline_checkbox = ft.Checkbox(
        label="Include 'Decline' action (destructive)", value=True
    )
    view_checkbox = ft.Checkbox(label="Include 'View' action", value=True)

    # Create action buttons with Cupertino style
    perm_button = ft.CupertinoFilledButton(
        content=ft.Text("Request Permissions"),
        on_click=request_permissions,
    )

    show_button = ft.CupertinoFilledButton(
        content=ft.Text("Show Notification"),
        on_click=show_notification,
    )

    schedule_button = ft.CupertinoFilledButton(
        content=ft.Text("Schedule (10s)"),
        on_click=schedule_notification,
    )

    # Create a Cupertino-styled card for the form
    form_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Configure Notification", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.BLACK_12),
                ft.Container(height=10),
                id_field,
                ft.Container(height=10),
                title_field,
                ft.Container(height=10),
                body_field,
                ft.Container(height=10),
                payload_field,
                ft.Container(height=10),
                ft.Text("Notification Actions", size=14, weight=ft.FontWeight.BOLD),
                accept_checkbox,
                decline_checkbox,
                view_checkbox,
                ft.Container(height=20),
                ft.Row(
                    [
                        perm_button,
                        ft.Container(width=10),
                        show_button,
                        ft.Container(width=10),
                        schedule_button,
                    ],
                    wrap=True,
                    spacing=10,
                ),
            ]
        ),
        padding=15,
        border_radius=ft.BorderRadius.all(15),
        border=ft.Border.all(1, ft.Colors.BLACK_12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, ft.Colors.GREY),
            offset=ft.Offset(0, 5),
        ),
    )

    # Action response display; updated by on_notification_action
    action_text = ft.Text(
        "Actions will appear here when tapped",
        size=14,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.CENTER,
    )

    action_display = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Notification Action Responses",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(height=1, color=ft.Colors.BLACK_12),
                ft.Container(content=action_text, padding=20),
            ]
        ),
        padding=15,
        border_radius=ft.BorderRadius.all(15),
        border=ft.Border.all(1, ft.Colors.BLACK_12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, ft.Colors.GREY),
            offset=ft.Offset(0, 5),
        ),
    )

    # Add components to the page with iOS-like styling
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Notification Actions Example",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=10),
                    form_card,
                    ft.Container(height=20),
                    action_display,
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Text(
                            "Note: Action handling may behave differently on each "
                            "platform. On iOS, ensure notifications are enabled "
                            "in settings.",
                            size=12,
                            color=ft.Colors.GREY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.Padding.symmetric(horizontal=20),
                    ),
                ]
            ),
            padding=ft.Padding.only(bottom=30),
        )
    )


ft.run(main)
