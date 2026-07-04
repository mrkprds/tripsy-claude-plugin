# Tripsy plugin for Claude

Connects Claude to [Tripsy](https://tripsy.app), the travel planner, through Tripsy's official MCP server (`https://mcp.tripsy.app`). Once installed you can ask Claude to create trips, add activities, organize reservations, track expenses, and query your itineraries.

This plugin contains no code — it simply registers Tripsy's hosted MCP server, which uses OAuth. You sign in with your own Tripsy account on first use.

## Install

Add this repo as a plugin marketplace, then install the plugin:

```
/plugin marketplace add <your-github-user>/tripsy-claude-plugin
/plugin install tripsy@tripsy-marketplace
```

Restart Claude Code (or reload the session) when prompted.

## Authenticate

The first time Claude calls a Tripsy tool you'll be asked to sign in. You can also trigger it manually:

```
/mcp
```

Select **tripsy** and choose *Authenticate*. A browser window opens for the Tripsy (my.tripsy.app) OAuth login.

## Usage examples

- "What trips do I have coming up?"
- "Add a dinner reservation at 19:00 on the second day of my Lisbon trip."
- "Build me a 3-day itinerary for my Tokyo trip with museums and good ramen spots."
- "How much have I spent on the Rome trip so far?"

## Uninstall

```
/plugin uninstall tripsy@tripsy-marketplace
```
