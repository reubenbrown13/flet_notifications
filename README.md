# flet_notifications
LocalNotifications control for Flet. Based on [flutter_local_notifications](https://pub.dev/packages/flutter_local_notifications)


<div align="center">
  <table>
    <tr>
      <td width="50%">
        <img width="100%" src="https://github.com/user-attachments/assets/b7cbd459-6fa6-4808-8d71-d54605fc85fa" alt="logo">
      </td>
      <td width="50%">
        <img width="100%" src="https://github.com/user-attachments/assets/c9750064-c282-409f-a819-c884c62c3329" >
      </td>
    </tr>
  </table>
</div>

### Usage
#### Initialization
```python
# import the control
from flet_notifications import LocalNotifications
# initialize it
notifications = LocalNotifications()
# add it to the page overlay (since it's non visual)
page.overlay.append(notifications)
```

#### methods
```python
async def show_notification(
    id: int, 
    title: str, 
    body: str, 
    payload: Optional[str] = None
) -> bool
 ```

Displays a local notification with the specified title, body, and payload.

Parameters:

- id ( int ): Unique identifier for the notification.
- title ( str ): Title of the notification.
- body ( str ): Body content of the notification.
- payload ( Optional[str] ): Optional payload that can be used when the notification is tapped.
Returns:

- bool : True if the notification was successfully shown, False otherwise. schedule_notification


```python
async def schedule_notification(
    id: int, 
    title: str, 
    body: str, 
    scheduled_date: datetime,
    payload: Optional[str] = None
) -> bool
 ```

Schedules a local notification to be displayed at a specific date and time.

Parameters:

- id ( int ): Unique identifier for the notification.
- title ( str ): Title of the notification.
- body ( str ): Body content of the notification.
- scheduled_date ( datetime ): Date and time when the notification should be displayed.
- payload ( Optional[str] ): Optional payload that can be used when the notification is tapped.
Returns:

- bool : True if the notification was successfully scheduled, False otherwise. request_permissions

```python
async def request_permissions() -> bool
```

Requests permissions for displaying notifications.

Returns:

- bool : True if permissions were granted, False otherwise.

