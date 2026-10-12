# flet_notifications example

Demonstrates the `LocalNotifications` service from `flet-notifications`
(requires Flet 1.0+).

`flet-notifications` is a custom Flet extension, so the Flutter code must be
compiled into the app. `flet run` alone will not work; build the app first:

```
cd examples/flet_notifications_example
flet build macos -v      # or windows / linux / apk / ipa
```

Then launch the built app. After changing Dart or `pubspec.yaml`, run
`flet clean` and rebuild. Python-only changes to `src/main.py` don't need a
rebuild.

If you change dependencies, refresh the lock file: `uv lock --upgrade`.
