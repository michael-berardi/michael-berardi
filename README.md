<picture>
  <source media="(max-width: 600px)" srcset="./assets/header-mobile.svg?v=4">
  <img src="./assets/header.svg?v=4" alt="Michael Berardi. Building Motorcycles for the Mind." width="100%">
</picture>

I'm Mike. I run [Liberty Design Studio](https://libertydesign.studio/) from New York and Buenos Aires, and most days a few dozen AI coding agents work alongside me.

The repos here are the tools that way of working needed: memory the agents share, a browser they can drive, plans they keep, delegation that checks its own results, compaction that costs nothing, and a reaper that cleans up after them. All of it runs on your own machine and keeps your data in plain files, written in whichever of Swift, Rust, TypeScript or Python the problem prefers.

## Agent infrastructure

| | |
|---|---|
| **[Steak Pi](https://github.com/michael-berardi/steak-pi)** | The [Pi coding agent](https://pi.dev), cooked properly. Native subagents, deterministic compaction, automatic verification, and a TUI worth living in. Eight parallel workers finish in under 1.5 s, and a full session peaks at the same memory as stock Pi. `TypeScript` |
| **[UltraCompress](https://github.com/michael-berardi/ultracompress)** | Context compaction with no LLM in the loop. About 65 ms where Claude Code's own summarizer takes 23 to 52 seconds, at $0 per compaction, and anything it condenses stays searchable. Ships for Pi and as a Claude Code plugin. `Rust` |
| **[UltraTerm Plan](https://github.com/michael-berardi/ultraterm-plan)** | The plan the agent keeps and you can read. Phases in order, one active task, blocked means blocked. Survives compaction, resume, and a change of agent. `TypeScript` |
| **[USAP](https://github.com/michael-berardi/ultraterm-subagent-protocol)** | A delegation protocol for subagents. Parallelize only what is actually independent, send each task to the cheapest model that can finish it, and treat "done" as evidence to check. `Protocol` |
| **[UTP](https://github.com/michael-berardi/ultraterm-protocol)** | Lets local agents inspect and drive persistent terminal sessions. JSON Lines over a `0600` Unix socket, and every destructive action dry-runs first. `Python` |
| **[TrimReaper](https://github.com/michael-berardi/TrimReaper)** | Reclaims the disk agent swarms leave behind: clones, `node_modules`, Rust targets, scratch and screenshots. Deletes only what it can prove is safe, archives unsaved work first, and writes a receipt before every removal. CLI and MCP server. `Python` |

## Memory and hands

| | |
|---|---|
| **[Retex](https://github.com/michael-berardi/retex)** | A Markdown vault engine and machine-readable CLI for people and agents. Search, recall, backlinks, boards, undo, and MCP over an ordinary folder. No database to get locked into. `Swift` |
| **[OverSeer Browser](https://github.com/michael-berardi/overseer-browser)** | Model-agnostic browser automation for Chromium. Agents get their own window; your tabs stay yours until you lend one. `TypeScript` `Python` |
| **[UltraTerm Computer Use](https://github.com/michael-berardi/ultraterm-computer-use)** | Desktop automation for any MCP-capable agent on macOS, Linux, and Windows. Screenshots and keystrokes never leave the machine. `Swift` |
| **[Rusty Mirror](https://github.com/michael-berardi/rusty-mirror)** | A hidden, disposable twin of your real Tauri app window, so agents can poke, screenshot and hot-swap the actual app instead of a browser stand-in. `Rust` |

## Apps

| | |
|---|---|
| **[UltraVox](https://github.com/michael-berardi/ultravox)** | Private, on-device transcription for macOS, Windows, and Linux. Dictate into any app, transcribe meetings and media, keep every recording local. [Download](https://github.com/michael-berardi/ultravox/releases/latest) `Rust` |
| **[Skribi](https://github.com/michael-berardi/skribi)** | A calm reader and editor for Markdown libraries and Retex vaults. Imports Obsidian and Notion without holding your notes hostage. `Rust` |
| **[Concept](https://github.com/michael-berardi/concept)** | Pages, databases and boards for your team, stored as plain Markdown. Self-host it or use the native Mac app, sync with Git, and read the same folder with Retex. `TypeScript` |
| **[Good Night](https://github.com/michael-berardi/goodnight)** | Warms your screen after sunset and dims it all the way to black, external monitors included. Free for macOS and Windows. [Download](https://github.com/michael-berardi/goodnight/releases/latest) `Swift` |
| **[UltraLink](https://github.com/michael-berardi/ultralink)** | Your Starlink connection, live in the Mac menu bar: speed, outages, history and the sky view. Read-only, no account, no cloud. [Download](https://github.com/michael-berardi/ultralink/releases/latest) `Swift` |

## Libraries and methods

| | |
|---|---|
| **[Carapace](https://github.com/michael-berardi/carapace)** | Write your app's brain once in Rust and give each platform a thin, generated shell: SwiftUI, Tauri, or anything that can call C. Good Night runs on it. `Rust` |
| **[Champollion](https://github.com/michael-berardi/champollion)** | An open method and offline toolkit for translating complete works directly from their originals, with the checks to prove it. Grew out of [Mouseia](https://mouseia.org). `Python` |
| **[cd-case](https://github.com/michael-berardi/cd-case)** | A CD jewel case in three.js, built to the real dimensions: light refracts through the shell and the disc throws a true diffraction rainbow. [Live demo](https://cd-case.pages.dev) `TypeScript` |
| **[ultra-media-remote](https://github.com/michael-berardi/ultra-media-remote)** | Reads and controls macOS Now Playing from safe Rust, without linking Apple's private framework. `Rust` |

## How it's built

Your data stays on your machine. Permissions and failure modes are designed first. Every dependency earns its place, and every number ships with the benchmark behind it.

## Work with me

[Liberty Design Studio](https://libertydesign.studio/) builds websites, brands and search strategy for businesses, and software when the problem calls for it. Independent software lives at [Pareto Cybernetics](https://paretocybernetics.com/software/). Issues and pull requests are welcome on any repo here.
