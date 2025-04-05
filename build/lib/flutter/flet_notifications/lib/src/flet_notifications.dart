import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
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

  NotificationService._internal();

  Future<void> initialize() async {
    if (_isInitialized) return;
    
    debugPrint('Inizializzazione del servizio notifiche...');
    
    // Inizializzazione per Android
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');  // Usa l'icona dell'app
    
    // Inizializzazione per iOS
    final DarwinInitializationSettings initializationSettingsIOS =
        DarwinInitializationSettings();
    
    // Inizializzazione per macOS
    final DarwinInitializationSettings initializationSettingsMacOS =
        DarwinInitializationSettings();
    
    // Combinazione delle impostazioni
    final InitializationSettings initializationSettings = InitializationSettings(
        android: initializationSettingsAndroid,
        iOS: initializationSettingsIOS,
        macOS: initializationSettingsMacOS);
    
    // Inizializza il plugin
    await flutterLocalNotificationsPlugin.initialize(
      initializationSettings,
      onDidReceiveNotificationResponse: (NotificationResponse response) {
        debugPrint('Notifica toccata: ${response.id}, ${response.payload}');
      },
    );
    
    _isInitialized = true;
    debugPrint('Servizio notifiche inizializzato con successo');
  }

  // Mostra una notifica semplice
  Future<void> showNotification(int id, String title, String body, {String? payload}) async {
    if (!_isInitialized) {
      await initialize();
    }
    
    // Dettagli per Android
    const AndroidNotificationDetails androidDetails = AndroidNotificationDetails(
      'your_channel_id',
      'your_channel_name',
      channelDescription: 'your_channel_description',
      importance: Importance.max,
      priority: Priority.high,
    );
    
    // Dettagli per iOS/macOS
    const DarwinNotificationDetails darwinDetails = DarwinNotificationDetails();
    
    // Combina i dettagli
    const NotificationDetails notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: darwinDetails,
      macOS: darwinDetails,
    );
    
    // Mostra la notifica
    try {
      await flutterLocalNotificationsPlugin.show(
        id,
        title,
        body,
        notificationDetails,
        payload: payload,
      );
      debugPrint('Notifica mostrata con successo: ID=$id, Titolo=$title');
    } catch (e) {
      debugPrint('Errore durante la visualizzazione della notifica: $e');
    }
  }
  
  // Programma una notifica
  Future<void> scheduleNotification(
    int id,
    String title,
    String body,
    DateTime scheduledDate,
    {String? payload}
  ) async {
    if (!_isInitialized) {
      await initialize();
    }
    
    // Dettagli per Android
    const AndroidNotificationDetails androidDetails = AndroidNotificationDetails(
      'your_channel_id',
      'your_channel_name',
      channelDescription: 'your_channel_description',
      importance: Importance.max,
      priority: Priority.high,
    );
    
    // Dettagli per iOS/macOS
    const DarwinNotificationDetails darwinDetails = DarwinNotificationDetails();
    
    // Combina i dettagli
    const NotificationDetails notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: darwinDetails,
      macOS: darwinDetails,
    );
    
    // Programma la notifica
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
      debugPrint('Notifica programmata con successo per: ${scheduledDate.toString()}');
    } catch (e) {
      debugPrint('Errore durante la programmazione della notifica: $e');
    }
  }
  
  // Richiedi permessi
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
      debugPrint('Permessi Android: $androidResult');
    } catch (e) {
      debugPrint('Errore durante la richiesta di permessi Android: $e');
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
      debugPrint('Permessi iOS: $iosResult');
    } catch (e) {
      debugPrint('Errore durante la richiesta di permessi iOS: $e');
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
      debugPrint('Permessi macOS: $macOSResult');
    } catch (e) {
      debugPrint('Errore durante la richiesta di permessi macOS: $e');
    }
    
    return macOSResult ?? iosResult ?? androidResult;
  }
}

class FletNotificationsControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final FletControlBackend backend;

  const FletNotificationsControl({
    Key? key,
    required this.parent,
    required this.control,
    required this.children,
    required this.backend,
  }) : super(key: key);

  @override
  State<FletNotificationsControl> createState() => _FletNotificationsControlState();
}

class _FletNotificationsControlState extends State<FletNotificationsControl> {
  final NotificationService _notificationService = NotificationService();
  
  @override
  void initState() {
    super.initState();
    _initializeNotifications();
    _subscribeMethods();
  }

  Future<void> _initializeNotifications() async {
    await _notificationService.initialize();
  }

  void _subscribeMethods() {
    widget.backend.subscribeMethods(widget.control.id, _handleMethods);
  }

  Future<String?> _handleMethods(String methodName, Map<String, String> args) async {
    debugPrint('Metodo chiamato: $methodName con argomenti: $args');
    
    switch (methodName) {
      case 'show_notification':
        final id = int.tryParse(args['id'] ?? '0') ?? 0;
        final title = args['title'] ?? '';
        final body = args['body'] ?? '';
        final payload = args['payload'];
        
        await _notificationService.showNotification(id, title, body, payload: payload);
        return 'ok';
      
      case 'schedule_notification':
        final id = int.tryParse(args['id'] ?? '0') ?? 0;
        final title = args['title'] ?? '';
        final body = args['body'] ?? '';
        final payload = args['payload'];
        final dateTimeStr = args['scheduled_date'] ?? '';
        
        if (dateTimeStr.isEmpty) {
          return 'error:missing_date';
        }
        
        try {
          final scheduledDate = DateTime.parse(dateTimeStr);
          await _notificationService.scheduleNotification(
            id, title, body, scheduledDate, payload: payload
          );
          return 'ok';
        } catch (e) {
          debugPrint('Errore durante l\'analisi della data: $e');
          return 'error:invalid_date';
        }
      
      case 'request_permissions':
        final result = await _notificationService.requestPermissions();
        return result.toString();
      
      default:
        debugPrint('Metodo non riconosciuto: $methodName');
        return null;
    }
  }

  @override
  void dispose() {
    widget.backend.unsubscribeMethods(widget.control.id);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Questo è un controllo non visuale
    return const SizedBox.shrink();
  }
}