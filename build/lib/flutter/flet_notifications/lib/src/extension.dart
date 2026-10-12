import 'package:flet/flet.dart';

import 'flet_notifications.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "LocalNotifications":
        return LocalNotificationsService(control: control);
      default:
        return null;
    }
  }
}
