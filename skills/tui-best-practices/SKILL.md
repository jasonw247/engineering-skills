---
name: tui-best-practices
description: Design, implement, refactor, or review terminal user interfaces (TUIs) and interactive CLIs covering screen models, keyboard focus, input and paste handling, Unicode cell layout, async streaming, terminal teardown, and PTY testing. Use when building or reviewing interactive terminal apps or coding-agent TUIs; not for non-interactive CLI flag parsing alone, web or native GUIs, or backend service logic.
---

# TUI best practices

Build terminal interfaces that stay responsive under load, restore the user's shell cleanly on exit, and keep four things clear at a glance: where focus is, what is running, what keys work here, and what succeeded or failed.

## Steps

1. **Inspect the runtime and environment.** Check the TUI framework in use (Ratatui/Crossterm, Bubble Tea, Textual, Ink, curses, or raw ANSI), target OSes, expected viewport sizes down to `80x24`, SSH/tmux/Zellij usage, and whether `stdin` or `stdout` can be piped.
2. **Choose the screen model that fits the job:**

   | Task shape | Screen model | Watch out for |
   | --- | --- | --- |
   | Short prompts, progress bars, composable commands | Inline / normal buffer (keeps native scrollback and selection) | Multi-line cursor rewrites breaking when lines wrap on narrow terminals |
   | Sustained navigation, filtering, live tables, multi-pane views | Alternate screen (`?1049h`) with explicit focus and key hints | Losing native scrollback and copy unless search, copy, or plain export is provided |
   | Long-running streaming or chat sessions | Inline history with a pinned bottom composer/status bar, or alternate screen with virtualized scrollback | Re-parsing and reflowing the full transcript on every new chunk |

3. **Build one vertical slice.** Keep domain and execution state separate from view state (scroll offsets, selection, open modals). Install terminal cleanup hooks before entering raw mode. When the interface supervises coding agents, tool calls, approvals, or diffs, also read [agent interfaces](references/agent-interfaces.md).
4. **Verify.** Test state reducers directly, check narrow layouts and wide Unicode glyphs with frame snapshots, and exercise raw-mode restoration, resize (`SIGWINCH`), `Ctrl-C`, and piped non-TTY output in a real PTY when touching lifecycle or input code.

## Interaction and layout rules

- Give most of the viewport to the primary work area plus a single-line status and key-hint bar. Open modals or split panes on demand rather than framing small terminals with nested borders and permanent sidebars.
- Keep global navigation keys consistent (`Esc` closes transient overlays without discarding drafts, `?` opens key help, `Ctrl-C` interrupts or exits predictably), and never steal focus when background output arrives.
- Auto-scroll new output only while the viewport sits at the bottom; freeze the scroll position anchored by item or line ID as soon as the user scrolls up, with a cue to jump back to live output.
- Pair every color state cue with text or a symbol (`[FAIL]`, `*`, `[running]`) so status remains legible under `NO_COLOR`, monochrome themes, and color-vision differences. Show percentage bars only when the total is known; otherwise show active step and elapsed time.
- Before irreversible actions, display the target and consequence, default focus to cancel, and enforce permissions in the action runner rather than UI handlers alone.

## Terminal traps builds miss

- Entering raw mode, the alternate screen, mouse capture, or Kitty keyboard mode without panic and signal teardown leaves the user's shell with a hidden cursor, staircase newlines (`\n` without `\r`), and echoed mouse escape codes. Install panic hooks and `try`/`finally` or `Drop` guards before switching modes, and write teardown sequences to the same TTY stream (`stdout` or `stderr`) that entered raw mode.
- Input backends such as Crossterm on Windows and terminals with the Kitty keyboard protocol emit `Release` and `Repeat` events alongside `Press`. Handling key events without filtering for `KeyEventKind::Press` (and intentional repeats) fires actions twice.
- Stray writes from `println!`, `eprintln!`, `logging.StreamHandler`, or child processes inheriting stdio print straight across the alternate screen and desynchronize cursor tracking. Route logs to a file or ring buffer and pipe child stdio before starting the UI.
- Slicing UTF-8 strings by byte index panics on multibyte characters, and counting bytes or codepoints misaligns columns on 2-cell CJK characters, 0-cell combining marks, emoji grapheme clusters, and ANSI escape codes. Measure width in terminal display cells (`unicode-width` / `wcwidth` over grapheme clusters) and clip on grapheme boundaries.
- Without bracketed paste (`?2004h`), or when paste chunks pass through the normal key handler, pasted newlines trigger `Enter` and submit partial input. Enable bracketed paste and insert pasted text directly into the buffer.
- Blocking network, disk, or subprocess calls on the render thread freeze input and resize handling, while redrawing on every output line from a fast child process starves keystrokes. Run I/O off the UI loop with bounded buffers and coalesce redraws onto a frame tick (16 to 33 ms, wrapped in synchronized output `?2026h`/`?2026l` where supported).
- Rendering raw log lines, commit messages, or tool output lets untrusted bytes inject CSI or OSC sequences that rewrite screen lines, spoof prompts, alter titles, or write to the clipboard via `OSC 52`, including sequences split across chunks. Strip or parse control bytes (`0x00-0x1F`, `0x7F`, `0x80-0x9F`, CSI/OSC/DCS) statefully before rendering.
- Sending cursor escapes or waiting on raw TTY reads when `!isatty(stdout)` or `TERM=dumb` breaks `cmd | head`, file redirects, and CI runs. Check TTY status on `stdin` and `stdout` independently, honor `NO_COLOR`, and fall back to plain line output when piped.
