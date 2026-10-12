import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/timezone.dart' as tz;
import 'package:timezone/data/latest.dart' as tz_data;

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();
  bool _isInitialized = false;

  factory NotificationService() {
    return _instance;
  }

  NotificationService._internal() {
    // Initialize timezone data
    tz_data.initializeTimeZones();
  }

  Future<void> initialize() async {
    if (_isInitialized) return;
    
    debugPrint('Initializing notification service...');
    
    // Android initialization
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');
    
    // iOS initialization
    final DarwinInitializationSettings initializationSettingsIOS =
        DarwinInitializationSettings(
          notificationCategories: [
            DarwinNotificationCategory(
              'default_category',
              actions: [
                DarwinNotificationAction.plain(
                  'view', 
                  'View',
                ),
                DarwinNotificationAction.plain(
                  'dismiss', 
                  'Dismiss',
                  options: <DarwinNotificationActionOption>{
                    DarwinNotificationActionOption.destructive,
                  },
                ),
                DarwinNotificationAction.plain(
                  'open', 
                  'Open',
                  options: <DarwinNotificationActionOption>{
                    DarwinNotificationActionOption.foreground,
                  },
                ),
              ],
            ),
          ],
        );
    
    // macOS initialization
    final DarwinInitializationSettings initializationSettingsMacOS =
        DarwinInitializationSettings(
          notificationCategories: [
            DarwinNotificationCategory(
              'default_category',
              actions: [
                DarwinNotificationAction.plain(
                  'view', 
                  'View',
                ),
                DarwinNotificationAction.plain(
                  'dismiss', 
                  'Dismiss',
                  options: <DarwinNotificationActionOption>{
                    DarwinNotificationActionOption.destructive,
                  },
                ),
                DarwinNotificationAction.plain(
                  'open', 
                  'Open',
                  options: <DarwinNotificationActionOption>{
                    DarwinNotificationActionOption.foreground,
                  },
                ),
              ],
            ),
          ],
        );
    
    // Linux initialization (required when running on Linux)
    const LinuxInitializationSettings initializationSettingsLinux =
        LinuxInitializationSettings(defaultActionName: 'Open notification');
 
    // Combine settings
    final InitializationSettings initializationSettings = InitializationSettings(
        android: initializationSettingsAndroid,
        iOS: initializationSettingsIOS,
        macOS: initializationSettingsMacOS);
    
    // Initialize plugin
    await flutterLocalNotificationsPlugin.initialize(
      initializationSettings,
      onDidReceiveNotificationResponse: (NotificationResponse response) {
        debugPrint('Notification tapped: ${response.id}, ${response.payload}, ${response.actionId}');
        // Handle notification response
        if (_onActionCallback != null) {
          _onActionCallback!(response.actionId ?? 'tap', response.payload ?? '');
        }
      },
    );
    
    _isInitialized = true;
    debugPrint('Notification service initialized successfully');
  }

  // Callback for notification actions
  Function(String, String)? _onActionCallback;

  void setActionCallback(Function(String, String) callback) {
    _onActionCallback = callback;
  }

  /// Clears the callback, but only if it is still [callback]. This keeps a
  /// disposed service from removing the callback of a newer one.
  void clearActionCallback(Function(String, String) callback) {
    if (identical(_onActionCallback, callback)) {
      _onActionCallback = null;
    }
  }

  // Show a notification with actions. Returns true on success.
  Future<bool> showNotification(
    int id, 
    String title, 
    String body, 
    {String? payload, List<NotificationActionData>? actions}
  ) async {
    if (!_isInitialized) {
      await initialize();
    }
    
    // Android details
    AndroidNotificationDetails androidDetails = const AndroidNotificationDetails(
      'your_channel_id',
      'your_channel_name',
      channelDescription: 'your_channel_description',
      importance: Importance.max,
      priority: Priority.high,
    );
    
    // Add actions to Android notification if provided
    if (actions != null && actions.isNotEmpty) {
      List<AndroidNotificationAction> androidActions = actions.map((action) => 
        AndroidNotificationAction(
          action.id, 
          action.title,
          showsUserInterface: action.foreground,
        )
      ).toList();
      
      androidDetails = AndroidNotificationDetails(
        'your_channel_id',
        'your_channel_name',
        channelDescription: 'your_channel_description',
        importance: Importance.max,
        priority: Priority.high,
        actions: androidActions,
      );
    }
    
    // iOS/macOS details
    DarwinNotificationDetails darwinDetails = const DarwinNotificationDetails(
      categoryIdentifier: 'default_category',
    );
    
    // Combine details
    NotificationDetails notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: darwinDetails,
      macOS: darwinDetails,
    );
    
    // Show notification
    try {
      await flutterLocalNotificationsPlugin.show(
        id,
        title,
        body,
        notificationDetails,
        payload: payload,
      );
      debugPrint('Notification shown successfully: ID=$id, Title=$title');
      return true;
    } catch (e) {
      debugPrint('Error showing notification: $e');
      return false;
    }
  }
  
  // Schedule a notification. Returns true on success.
  Future<bool> scheduleNotification(
    int id,
    String title,
    String body,
    DateTime scheduledDate,
    {String? payload, List<NotificationActionData>? actions}
  ) async {
    if (!_isInitialized) {
      await initialize();
    }
    
    // Android details
    AndroidNotificationDetails androidDetails = const AndroidNotificationDetails(
      'your_channel_id',
      'your_channel_name',
      channelDescription: 'your_channel_description',
      importance: Importance.max,
      priority: Priority.high,
    );
    
    // Add actions to Android notification if provided
    if (actions != null && actions.isNotEmpty) {
      List<AndroidNotificationAction> androidActions = actions.map((action) => 
        AndroidNotificationAction(
          action.id, 
          action.title,
          showsUserInterface: action.foreground,
        )
      ).toList();
      
      androidDetails = AndroidNotificationDetails(
        'your_channel_id',
        'your_channel_name',
        channelDescription: 'your_channel_description',
        importance: Importance.max,
        priority: Priority.high,
        actions: androidActions,
      );
    }
    
    // iOS/macOS details
    DarwinNotificationDetails darwinDetails = const DarwinNotificationDetails(
      categoryIdentifier: 'default_category',
    );
    
    // Combine details
    NotificationDetails notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: darwinDetails,
      macOS: darwinDetails,
    );
    
    // Schedule notification
    try {
      await flutterLocalNotificationsPlugin.zonedSchedule(
        id,
        title,
        body,
        tz.TZDateTime.from(scheduledDate, tz.local),
        notificationDetails,
        androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
        payload: payload,
      );
      debugPrint('Notification scheduled successfully for: ${scheduledDate.toString()}');
      return true;
    } catch (e) {
      debugPrint('Error scheduling notification: $e');
      return false;
    }
  }
  
  // Request permissions
  Future<bool?> requestPermissions() async {
    if (!_isInitialized) {
      await initialize();
    }
    
    // Android
    bool? androidResult;
    try {
      androidResult = await flutterLocalNotificationsPlugin
          .resolvePlatformSpecificImplementation<AndroidFlutterLocalNotificationsPlugin>()
          ?.requestNotificationsPermission();
      debugPrint('Android permissions: $androidResult');
    } catch (e) {
      debugPrint('Error requesting Android permissions: $e');
    }
    
    // iOS
    bool? iosResult;
    try {
      iosResult = await flutterLocalNotificationsPlugin
          .resolvePlatformSpecificImplementation<IOSFlutterLocalNotificationsPlugin>()
          ?.requestPermissions(
            alert: true,
            badge: true,
            sound: true,
          );
      debugPrint('iOS permissions: $iosResult');
    } catch (e) {
      debugPrint('Error requesting iOS permissions: $e');
    }
    
    // macOS
    bool? macOSResult;
    try {
      macOSResult = await flutterLocalNotificationsPlugin
          .resolvePlatformSpecificImplementation<MacOSFlutterLocalNotificationsPlugin>()
          ?.requestPermissions(
            alert: true,
            badge: true,
            sound: true,
          );
      debugPrint('macOS permissions: $macOSResult');
    } catch (e) {
      debugPrint('Error requesting macOS permissions: $e');
    }
    
    return macOSResult ?? iosResult ?? androidResult;
  }
}

// Class to represent notification action data
class NotificationActionData {
  final String id;
  final String title;
  final bool destructive;
  final bool foreground;
  
  NotificationActionData({
    required this.id,
    required this.title,
    this.destructive = false,
    this.foreground = true,
  });
}

/// Flet 1.0 service exposing [NotificationService] to Python as
/// `LocalNotifications`.
class LocalNotificationsService extends FletService {
  LocalNotificationsService({required super.control});

  final NotificationService _notificationService = NotificationService();

  late final void Function(String, String) _onAction =
      (String actionId, String payload) {
    control.triggerEvent("notification_action", {
      "action_id": actionId,
      "payload": payload,
    });
  };

  @override
  void init() {
    super.init();
    control.addInvokeMethodListener(_invokeMethod);
    unawaited(_initializeNotifications());
  }

  Future<void> _initializeNotifications() async {
    try {
      await _notificationService.initialize();
      _notificationService.setActionCallback(_onAction);
    } catch (e) {
      debugPrint('Error initializing LocalNotifications: $e');
    }
  }

  int _parseId(dynamic value) => value is num ? value.toInt() : 0;

  // Actions arrive from Python as a list of
  // {id, title, destructive, foreground} maps.
  List<NotificationActionData>? _parseActions(dynamic raw) {
    if (raw is! List || raw.isEmpty) {
      return null;
    }

    final actions = <NotificationActionData>[];
    for (final item in raw) {
      if (item is! Map) {
        continue;
      }
      final id = item["id"]?.toString();
      final title = item["title"]?.toString();
      if (id == null || title == null) {
        continue;
      }
      actions.add(NotificationActionData(
        id: id,
        title: title,
        destructive: item["destructive"] == true,
        foreground: item["foreground"] != false,
      ));
    }

    return actions.isNotEmpty ? actions : null;
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint('LocalNotifications.$name($args)');
    final map = args is Map ? Map<String, dynamic>.from(args) : <String, dynamic>{};

    switch (name) {
      case 'show_notification':
        return _notificationService.showNotification(
          _parseId(map['id']),
          (map['title'] as String?) ?? '',
          (map['body'] as String?) ?? '',
          payload: map['payload'] as String?,
          actions: _parseActions(map['actions']),
        );

      case 'schedule_notification':
        final scheduledDate =
            DateTime.tryParse((map['scheduled_date'] as String?) ?? '');
        if (scheduledDate == null) {
          debugPrint('LocalNotifications: invalid or missing scheduled_date');
          return false;
        }
        return _notificationService.scheduleNotification(
          _parseId(map['id']),
          (map['title'] as String?) ?? '',
          (map['body'] as String?) ?? '',
          scheduledDate,
          payload: map['payload'] as String?,
          actions: _parseActions(map['actions']),
        );

      case 'request_permissions':
        final granted = await _notificationService.requestPermissions();
        return granted == true;

      default:
        throw Exception('Unknown LocalNotifications method: $name');
    }
  }

  @override
  void dispose() {
    control.removeInvokeMethodListener(_invokeMethod);
    _notificationService.clearActionCallback(_onAction);
    super.dispose();
  }
}
