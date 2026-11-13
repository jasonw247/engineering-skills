# Long commands and background tasks

The question is whether the agent should wait for a shell command to finish. Fast commands belong in the foreground and long ones in the background, ideally as the same process moving between the two.

Waiting has two costs. The user waits while nothing else happens. And no model request is sent while a command blocks, so if the wait outlasts the provider's cache lifetime, the next request reprocesses the whole prefix: a slower first token and a higher cost. Backgrounding does not keep the cache warm by itself; it lets the agent do useful work instead of idling. Look up the cache lifetime in the provider's current documentation.

## Checklist

Read the shell tool and background-task code. Answer each item with evidence, or record it as unknown.

| # | Item | Question |
| --- | --- | --- |
| 1 | Foreground limit | What is the longest foreground wait? Is it comfortably below the cache lifetime, leaving room for generation? |
| 2 | No rerun | When a command moves to the background, does the same process continue, or is it killed and started again? |
| 3 | Deadline | After a move to the background, or after its output is read, is the original deadline kept? Resetting it lets a stuck command run forever. |
| 4 | Completion delivery | Does the model learn that a background task finished from a notification, or only by polling? |
| 5 | Notification position | Is the notification appended at the end, or does it edit an already cached part of the request? |
| 6 | Polling | Is blocking wait time capped, and does repeated reading with no new output produce a hint to stop polling? |
| 7 | Output size | Is large output truncated or written to a file and read in parts? Is incomplete output labeled as incomplete? |
| 8 | Cleanup | Are background tasks stopped when the user stops the agent, when a one-shot headless run exits, and when the process restarts? Are orphaned tasks marked rather than left showing "running"? |
| 9 | After compaction | Is "finished but result not yet read" tracked outside the conversation, such as in a task table, so it survives compaction? |
| 10 | Precondition | If the current environment cannot deliver background results, is backgrounding disabled? |

## Behavioral checks

When the agent can be run, record what actually happens:

1. Ask it to start a dev server and then do something else. Does it hang?
2. Run a command that takes several minutes. Does it move to the background without starting a second copy?
3. Start a background task, then stop the agent. Does the task stop?
4. Let a background task finish, then trigger compaction before the result is read. Is the unread result still surfaced afterwards?
