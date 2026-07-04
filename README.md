# Tripsy plugin for Claude

Connects Claude to [Tripsy](https://tripsy.app), the travel planner, through Tripsy's official **local MCP server** (`tripsy-mcp`, part of the [Tripsy CLI](https://github.com/tripsyapp/cli)). Once installed you can ask Claude to create trips, add activities, organize reservations, track expenses, and query your itineraries.

The server runs as a local process and authenticates with a token stored by the Tripsy CLI — no OAuth connector flow, which makes it usable on accounts where custom remote connectors are disabled.

## Prerequisites

Install the Tripsy CLI and log in once:

```
curl -fsSL https://tripsy.app/install_cli | bash
tripsy auth login --username you@example.com
```

This installs `tripsy` and `tripsy-mcp` to `~/.local/bin` and stores your token in the OS credential store (macOS Keychain).

> **Note:** `.mcp.json` points at `/Users/patrickperdon/.local/bin/tripsy-mcp`. If your username or install dir differs, edit that path. It's absolute because GUI apps don't inherit your shell PATH.

## Install

Add this repo as a plugin marketplace, then install the plugin:

```
/plugin marketplace add mrkprds/tripsy-claude-plugin
/plugin install tripsy@tripsy-marketplace
```

Restart Claude (or reload the session) when prompted. In the Claude desktop app: Settings → Plugins → install from marketplace, then connect the **tripsy** connector on the plugin page.

## Usage examples

- "What trips do I have coming up?"
- "Add a dinner reservation at 19:00 on the second day of my Lisbon trip."
- "Build me a 3-day itinerary for my Tokyo trip with museums and good ramen spots."
- "How much have I spent on the Rome trip so far?"

## Troubleshooting

- Run `tripsy doctor` to check CLI health and authentication.
- If the server starts but tools fail with auth errors, re-run `tripsy auth login`.
- If credential-store access fails when launched from a GUI app, set `TRIPSY_AUTH_BACKEND=file` in the server `env` in `.mcp.json`.

## Uninstall

```
/plugin uninstall tripsy@tripsy-marketplace
```
