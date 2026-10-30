# Capturing real screens and flows from the app (iOS simulator)

Use this when a scene needs something the screenshot set doesn't have: a real flow (typing, tapping, saving), a specific status bar (no network), or fresh data.

## Build without touching the app's repo

1. Copy the source to a scratch folder (`rsync -a --exclude /build --exclude .dart_tool --exclude /ios/Pods ...`). Exclude **top-level** folders with a leading `/`: a bare `--exclude sync` also drops `lib/data/sync` and the build fails with dozens of missing types.
2. Match the toolchain to `pubspec.yaml`'s SDK constraint (`flutter --version`). Upgrading a Homebrew Flutter: `brew upgrade --cask flutter` (ask first — it is the person's machine).
3. If a newer Flutter rejects an exact pin (e.g. `intl 0.20.2` vs the SDK's `^0.20.3`), relax it **in the copy only**.
4. Flutter: `flutter pub get && dart run build_runner build --delete-conflicting-outputs && flutter build ios --simulator --debug` → `build/ios/iphonesimulator/Runner.app`.
5. Launch it on a simulator whose screen size matches your screenshot set (iPhone 17 / 17 Pro = 1206 × 2622) and open the live panel so the person can watch.

Never use a simulator that holds someone's real data; a fresh install is a fresh book.

## Set up demo data by hand

Go through onboarding in the film's language, then add only what the flow needs (a farm, a crop season, a party). Use the same names as the existing screenshots so the film stays consistent.

Driving the simulator:
- A cheap screenshot helper: `xcrun simctl io <udid> screenshot` → `ffmpeg scale=402` (1 px = 1 tap point) with a 50-pt grid; crop to the area you need. Don't use full-resolution screenshots for navigation.
- The first tap or text after a screen change is sometimes dropped; check, and repeat once.
- Typed words show only after a space commits them: type `"Farm "` with a trailing space. Numbers appear on the second attempt more often than the first: check the field before moving on.
- Do a dry run of the whole flow first to learn every tap target; the order of pickers can change after the first use (recently used items move first).

## Demo data that doesn't look empty

- A fresh book makes lists and totals look empty. With the app terminated, back up its SQLite, then insert parties, seasons and entries the way the app's own repository writes them (read its insert code: dates at local start of day, a payment row for paid entries, base quantities). Run `PRAGMA integrity_check` and relaunch. Keep the seeder script in `inputs/<slug>/` so the next video can reuse it.
- Things the voice shows, like a bill photo, can be demo media: render a simple page with headless Chrome and `xcrun simctl addmedia` it into Photos. Then attach it in the app.
- Non-Latin text (Hindi) can't be typed with `simctl`'s text input; it arrives garbled. Use `printf '…' | LANG=en_US.UTF-8 xcrun simctl pbcopy <udid>`, long-press the field and tap Paste. Cut the Paste bubble and the permission dialog out of the clip.

## Record

- Clean status bar: `xcrun simctl status_bar <udid> override --time 9:41 --dataNetwork wifi --wifiMode active --wifiBars 3 --cellularMode active --cellularBars 4 --batteryState charged --batteryLevel 100`.
- No network: `... override --time 9:41 --dataNetwork hide --wifiMode failed --wifiBars 0 --cellularMode notSupported`. Restore afterwards.
- `xcrun simctl io <udid> recordVideo --codec=h264 --force take.mp4` in the background; stop it with `SIGINT` (`pkill -INT -f take.mp4`).
- Take your time between steps (check each one); the pauses are cut later.

## Cut to the voice

For a tutorial, record one long take of the whole flow. Then cut one clip per voice line with `scripts/cut_takes.py`: anchors `(film_t, take_t, play_s)` jump to each event on its spoken word, play the animation, and hold.

The simulator writes variable-frame-rate video, so a seek lands on the next frame that changed, not on the time you asked for. Find event times with `fps=10,tblend=all_mode=difference,signalstats` (YAVG per frame), not by sampling seeks. Typing shows up as YAVG of only about 0.1–0.2. To check a moment by eye, use frame timestamps (`showinfo` with `-fps_mode passthrough`) or the same `fps=30,trim` path the cutter uses. Don't use `-ss` seeks: on a static screen the recording has no frames, so a seek to 528.0 returns the next change (530.4) and makes the event look 2 s early.

1. Find each event: big screen changes with ffmpeg scene detection on a 200-px copy; small ones (digits appearing) with a frame difference on a crop of that field at 10 fps.
2. Build one clip per scene with exact holds and plays (`hold` a frame for N s, `play` t0–t1), concatenated at 30 fps, so each event lands on its word. A scene's clip runs from the moment it first shows to the scene's end.
3. Take stills from the same takes for `lift()` cards, so the lifted card matches what is on screen.
4. In the build: add the `.mp4` to `SHOTS`, show it with `sc.screen(key, t_in, t_out, enter="fade")` (a recording is its own timed clip; it fades but never moves), and keep zooms, taps and lifts in screenshot pixels as before.
