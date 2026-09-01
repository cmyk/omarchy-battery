# Changelog

All notable user-facing changes to this plugin. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## v0.1.0 — Initial release

### Added

- Everything Omarchy's built-in Power widget already does, unchanged:
  battery percentage/bar, size/cycles/time/rate stats, charge-threshold
  detection, power-profile picker.
- **Charge-threshold toggle** — enable/disable firmware-backed charge
  protection via UPower's own `EnableChargeThreshold` method. Only shown
  when the battery reports a configured threshold.
- **Quick Dim** — one-click 40% brightness with exact restore, reading
  current brightness first so it never guesses.
- **Travel Mode** — saves power profile, brightness, and monitor refresh
  rate as one bundle; applies a travel preset; restores all three on
  toggle-off. Session-only.
- **GPU status** — discrete-GPU power draw and utilization, shown only on
  hybrid-GPU hardware.
- **Power draw history** — a 10-minute in-memory sparkline plus a live
  watts readout, built from data the widget already samples. No database.
- Independent plugin id (`io.github.aryan-techie.battery`) — installs
  alongside the built-in widget rather than replacing it, so both can run
  side by side while you decide which one to keep on the bar.
