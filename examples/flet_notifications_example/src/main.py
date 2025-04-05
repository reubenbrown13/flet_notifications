import flet as ft
from datetime import datetime, timedelta
from flet_notifications import LocalNotifications

async def main(page: ft.Page):
    page.title = "Flet Notifications Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Set iOS-like padding for the page
    page.padding = 20
    page.window.width = 400
    page.window.height = 700
    
    # Initialize the notifications control
    notifications = LocalNotifications()
    page.overlay.append(notifications)
    
    # Request notification permissions
    async def request_permissions(e):
        granted = await notifications.request_permissions()
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Permissions {'granted' if granted else 'denied'}!"),
            bgcolor=ft.colors.BLUE_ACCENT if granted else ft.colors.RED_ACCENT,
        )
        page.snack_bar.open = True
        page.update()
    
    # Show an immediate notification
    async def show_notification(e):
        id_val = int(id_field.value) if id_field.value and id_field.value.isdigit() else 0
        title = title_field.value or "Test Notification"
        body = body_field.value or "This is a test message"
        
        result = await notifications.show_notification(id_val, title, body)
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Notification {'sent successfully' if result else 'not sent'}"),
            bgcolor=ft.colors.GREEN_ACCENT if result else ft.colors.RED_ACCENT,
        )
        page.snack_bar.open = True
        page.update()
    
    # Schedule a notification
    async def schedule_notification(e):
        id_val = int(id_field.value) if id_field.value and id_field.value.isdigit() else 0
        title = title_field.value or "Scheduled Notification"
        body = body_field.value or "This notification was scheduled"
        
        # Schedule the notification for 10 seconds in the future
        scheduled_time = datetime.now() + timedelta(seconds=10)
        
        result = await notifications.schedule_notification(
            id_val, title, body, scheduled_time
        )
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Notification scheduled for {scheduled_time.strftime('%H:%M:%S')}"),
            bgcolor=ft.colors.GREEN_ACCENT if result else ft.colors.RED_ACCENT,
        )
        page.snack_bar.open = True
        page.update()
    
    # Create input fields with Cupertino style
    id_field = ft.CupertinoTextField(
        placeholder_text="Notification ID",
        value="0",
        border_radius=ft.border_radius.all(8),
    )
    
    title_field = ft.CupertinoTextField(
        placeholder_text="Title",
        value="Test Notification",
        border_radius=ft.border_radius.all(8),
    )
    
    body_field = ft.CupertinoTextField(
        placeholder_text="Body",
        value="This is a test message",
        max_lines=3,
    )
    
    # Create action buttons with Cupertino style
    perm_button = ft.CupertinoFilledButton(
        text="Request Permissions",
        on_click=request_permissions,
    )
    
    show_button = ft.CupertinoFilledButton(
        text="Show Notification",
        on_click=show_notification,
    )
    
    schedule_button = ft.CupertinoFilledButton(
        text="Schedule (10s)",
        on_click=schedule_notification,
    )
    
    # Create a Cupertino-styled card for the form
    form_card = ft.Container(
        content=ft.Column([
            ft.Text("Configure Notification", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(height=1, color=ft.colors.BLACK12),
            ft.Container(height=10),
            id_field,
            ft.Container(height=10),
            title_field,
            ft.Container(height=10),
            body_field,
            ft.Container(height=20),
            ft.ResponsiveRow([
                perm_button,
                ft.Container(width=10),
                show_button,
                ft.Container(width=10),
                schedule_button,
            ], # scroll=ft.ScrollMode.AUTO
            ),
        ]),
        padding=15,
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.colors.WHITE,
        border=ft.border.all(1, ft.colors.BLACK12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.2, ft.colors.GREY),
            offset=ft.Offset(0, 5),
        )
    )
    
    # Add components to the page with iOS-like styling
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Flet Notifications Example", size=24, weight=ft.FontWeight.BOLD),
                form_card,
                ft.Container(height=20),
                ft.Container(
                    content=ft.Text(
                        "Note: You may need to manually configure notification permissions in your device settings",
                        size=12,
                        color=ft.colors.GREY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=20),
                ),
            ]),
            padding=ft.padding.only(bottom=30),
        )
    )

ft.app(main)