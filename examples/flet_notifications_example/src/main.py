import flet as ft
from datetime import datetime, timedelta
from flet_notifications import LocalNotifications, NotificationAction

async def main(page: ft.Page):
   page.title = "Flet Notifications Example"
   page.theme_mode = ft.ThemeMode.LIGHT
   
   # Set iOS-like padding for the page
   page.padding = 20
   page.window.width = 400
   page.window.height = 700
   
   # Handle notification actions
   async def on_notification_action(action_id, payload):
       page.open(ft.SnackBar(
           content=ft.Text(f"Action '{action_id}' received with payload: {payload}"),
           bgcolor=ft.Colors.BLUE,
       ))
       page.update()
   
   # Initialize the notifications control
   notifications = LocalNotifications(
       on_notification_action=on_notification_action
   )
   page.add(notifications)
   
   # Request notification permissions
   async def request_permissions(e):
       granted = await notifications.request_permissions()
       page.open(ft.SnackBar(
           content=ft.Text(f"Permissions {'granted' if granted else 'denied'}!"),
           bgcolor=ft.Colors.BLUE_ACCENT if granted else ft.Colors.RED_ACCENT,
       ))
       page.update()
   
   # Show an immediate notification
   async def show_notification(e):
       id_val = int(id_field.value) if id_field.value and id_field.value.isdigit() else 0
       title = title_field.value or "Test Notification"
       body = body_field.value or "This is a test message"
       payload = payload_field.value
       
       # Create notification actions based on checkbox selections
       actions = []
       print(accept_checkbox.value, decline_checkbox.value, view_checkbox.value)
       if accept_checkbox.value:
           actions.append(NotificationAction(
               id="accept", 
               title="Accept", 
               foreground=True
           ))
       if decline_checkbox.value:
           actions.append(NotificationAction(
               id="decline", 
               title="Decline", 
               destructive=True, 
               foreground=False
           ))
       if view_checkbox.value:
           actions.append(NotificationAction(
               id="view", 
               title="View", 
               foreground=True
           ))
       
       result = await notifications.show_notification(
           id_val, 
           title, 
           body, 
           payload=payload,
           actions=actions if actions else None
       )
       
       page.open(ft.SnackBar(
           content=ft.Text(f"Notification {'sent successfully' if result else 'not sent'}"),
           bgcolor=ft.Colors.GREEN_ACCENT if result else ft.Colors.RED_ACCENT,
       ))
       page.update()
   
   # Schedule a notification
   async def schedule_notification(e):
       id_val = int(id_field.value) if id_field.value and id_field.value.isdigit() else 0
       title = title_field.value or "Scheduled Notification"
       body = body_field.value or "This notification was scheduled"
       payload = payload_field.value
       
       # Create notification actions based on checkbox selections
       actions = []
       if accept_checkbox.value:
           actions.append(NotificationAction(
               id="accept", 
               title="Accept", 
               foreground=True
           ))
       if decline_checkbox.value:
           actions.append(NotificationAction(
               id="decline", 
               title="Decline", 
               destructive=True, 
               foreground=False
           ))
       if view_checkbox.value:
           actions.append(NotificationAction(
               id="view", 
               title="View", 
               foreground=True
           ))
       
       # Schedule the notification for 10 seconds in the future
       scheduled_time = datetime.now() + timedelta(seconds=10)
       
       result = await notifications.schedule_notification(
           id_val, 
           title, 
           body, 
           scheduled_time,
           payload=payload,
           actions=actions if actions else None
       )
       
       page.open(ft.SnackBar(
           content=ft.Text(f"Notification scheduled for {scheduled_time.strftime('%H:%M:%S')}"),
           bgcolor=ft.Colors.GREEN_ACCENT if result else ft.Colors.RED_ACCENT,
       ))
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
       border_radius=ft.border_radius.all(8),
       max_lines=3,
   )
   
   payload_field = ft.CupertinoTextField(
       placeholder_text="Payload (optional)",
       value="test-payload-123",
       border_radius=ft.border_radius.all(8),
   )
   
   # Create checkboxes for notification actions
   accept_checkbox = ft.Checkbox(
       label="Include 'Accept' action",
       value=True,
   )
   
   decline_checkbox = ft.Checkbox(
       label="Include 'Decline' action (destructive)",
       value=True,
   )
   
   view_checkbox = ft.Checkbox(
       label="Include 'View' action",
       value=True,
   )
   
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
       content=ft.Column([
           ft.Text("Configure Notification", size=16, weight=ft.FontWeight.BOLD),
           ft.Divider(height=1, color=ft.Colors.BLACK12),
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
           ft.Row([
               perm_button,
               ft.Container(width=10),
               show_button,
               ft.Container(width=10),
               schedule_button,
           ], wrap=True, spacing=10),
       ]),
       padding=15,
       border_radius=ft.border_radius.all(15),
       bgcolor=ft.Colors.WHITE,
       border=ft.border.all(1, ft.Colors.BLACK12),
       shadow=ft.BoxShadow(
           spread_radius=1,
           blur_radius=15,
           color=ft.Colors.with_opacity(0.2, ft.Colors.GREY),
           offset=ft.Offset(0, 5),
       )
   )
   
   # Action response display
   action_display = ft.Container(
       content=ft.Column([
           ft.Text("Notification Action Responses", size=16, weight=ft.FontWeight.BOLD),
           ft.Divider(height=1, color=ft.Colors.BLACK12),
           ft.Container(
               content=ft.Text(
                   "Actions will appear here when tapped",
                   size=14,
                   color=ft.Colors.GREY,
                   text_align=ft.TextAlign.CENTER,
               ),
               padding=20,
           ),
       ]),
       padding=15,
       border_radius=ft.border_radius.all(15),
       bgcolor=ft.Colors.WHITE,
       border=ft.border.all(1, ft.Colors.BLACK12),
       shadow=ft.BoxShadow(
           spread_radius=1,
           blur_radius=15,
           color=ft.Colors.with_opacity(0.2, ft.Colors.GREY),
           offset=ft.Offset(0, 5),
       )
   )
   
   # Add components to the page with iOS-like styling
   page.add(
       ft.Container(
           content=ft.Column([
               ft.Text("Notification Actions Example", size=24, weight=ft.FontWeight.BOLD),
               ft.Container(height=10),
               form_card,
               ft.Container(height=20),
               action_display,
               ft.Container(height=20),
               ft.Container(
                   content=ft.Text(
                       "Note: Action handling may behave differently on each platform. On iOS, ensure notifications are enabled in settings.",
                       size=12,
                       color=ft.Colors.GREY,
                       text_align=ft.TextAlign.CENTER,
                   ),
                   padding=ft.padding.symmetric(horizontal=20),
               ),
           ]),
           padding=ft.padding.only(bottom=30),
       )
   )

ft.app(main)