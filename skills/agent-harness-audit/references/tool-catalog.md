# Tool catalog and results

Tools cost context in two ways. Every definition (name, description, parameter schema) is sent whether or not the tool is used, and every call returns its output into the conversation at the price of another model request. Tools that look alike also cost accuracy: the model picks the wrong one or passes the wrong arguments.

## Inventory

- List every tool exposed to the model, grouped by source: built-in, each MCP server, each plugin. Record the size of each definition and the total.
- Over representative tasks, record which tools are used on most turns and which are rarely used, how many calls and model requests each task took, and how large the results were.
- Before attributing a failure to a tool, check what the model had actually loaded at that turn. A deferred tool may never have been surfaced.

## Checklist

| Item | Question |
| --- | --- |
| Intent grouping | Are tools serving one user intent split into API-shaped variants ("list issues", "filter issues by label", "filter by author") that could be one tool with parameters? |
| Distinguishability | Could the model tell any two tools apart from their names and descriptions alone? Does each description state what the tool returns? |
| Namespacing | Are tools grouped by domain, with small groups? |
| Resident set | Are the tools used on most turns (read, edit, search, run a command) always loaded, and the rarely used ones deferred? |
| Deferred discovery | When tools are found by search, do realistic requests find the right tool in this catalog? A miss that looks like "no such tool" usually traces to a vague description. |
| Remote catalogs | Does fetching a remote tool list delay the first token of each request? A slow catalog may be better kept resident. |
| Result size | Are large results truncated or written to a file and read in parts, with truncation stated in the result? |
| Composition | For filtering or aggregating large data, three or more dependent calls, or batches, can the model compose the calls in code and return only what it needs? |

Search recall measured on clean benchmark catalogs does not transfer to a large real catalog with overlapping tools; test it on this one.

## Choose the first move

| Bottleneck | First move |
| --- | --- |
| Too many or too similar tools | Merge by intent, rename, group |
| Definitions take too much context | Deferred loading with tool search |
| Results or round trips take too much context | Programmatic composition |
| Arguments often wrong | Better descriptions and examples |

These steps build on each other: a clean catalog makes search reliable, and reliable search makes composition worthwhile. Measure each step separately.

## Constraints on programmatic composition

- Move the tools into the program's path. A code tool offered alongside every direct tool tends to go unused.
- Keep at the top level any tool that asks the user something, changes session state, or whose result must be read before the next decision (loading a tool or a skill), plus browser, publishing, and agent-spawning tools.
- Calls made from inside a program go through the same validation, hooks, permission prompts, and display as direct calls.
- Return a tool failure as a result rather than raising, so one failure does not discard the program's other results.
- Prefer structured tool output so the program can select fields. A program that returns raw output saves nothing.
- Search the harness for logic keyed on tool names, such as reminders, counters, and telemetry. It silently stops firing once those calls move inside a program.
