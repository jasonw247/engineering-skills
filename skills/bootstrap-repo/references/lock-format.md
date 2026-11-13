# Catalog lock format, version 1

A skill catalog is a directory holding a lock file and a `skills/` folder of packages. A repository's catalog is its `.agents/` directory; a host catalog is any directory the host chooses. Installers write catalogs and hosts read them. This document is the whole contract between them: neither side needs the other's code.

## Layout

- `skills.lock.json` is the lock. Readers also accept the original name `skill-repo.lock.json` when `skills.lock.json` is absent, and reject a catalog that contains both. Writers write `skills.lock.json` and remove the original name when they migrate a catalog.
- `skills/<name>/` holds one locked package: exactly the files its record lists, including `SKILL.md`, and no symlinks.

The lock is UTF-8 JSON of at most 1 MiB and is not a symlink.

## Lock

```json
{"schema_version": 1, "skills": {"<name>": {"version": "...", "files": {}, "dependencies": [], "roles": [], "use_when": "...", "cues": []}}}
```

`schema_version` is `1`; readers reject any other value. Package names are lowercase letters and digits in hyphen-separated words (`[a-z0-9]+(-[a-z0-9]+)*`). Each record has these fields:

| Field | Required | Type and meaning |
| --- | --- | --- |
| `version` | yes | Non-empty string: the package version. |
| `files` | yes | Object mapping each file's POSIX path, relative to the package directory, to the lowercase hex SHA-256 of its bytes. Lists every file, including `SKILL.md`. |
| `dependencies` | no | Array of package names. An absent field means none; writers always include it. |
| `roles` | yes | Non-empty array of `actor` (suited to implementing work) and `reviewer` (suited to reviewing work). |
| `use_when` | yes | Non-empty string: when the package helps. |
| `cues` | yes | Non-empty array of non-empty strings: terms a host may match against a task. |
| `upstream` | no | When present, an object describing the source the package was adapted from. Omit the field instead of writing `null` to mean none. |

Readers ignore fields they do not know, so a revision can add optional fields without changing `schema_version`.

## Meaning

- **Integrity.** A package is usable only when its directory matches `files` exactly, with no missing, extra, or changed file.
- **Dependencies.** Writers keep each catalog closed under dependencies. Readers resolve dependencies across the catalogs they combine and reject a missing or cyclic one.
- **Precedence.** When a host combines catalogs, a project entry replaces a host entry with the same name. Updating one catalog never refreshes another.
- **Advisory metadata.** `roles`, `use_when`, and `cues` describe a package and grant nothing. Each host applies its own selection policy, limits, and stage rules, and presents package text as subordinate to its own instructions.
- **No downloads.** Hosts read catalogs locally and never fetch packages during a run.

## Example

The engineering-skills repository's `evaluations/bootstrap-repo/fixtures/catalog-v1/` is a complete valid catalog of two example packages. Hosts can copy it into their own tests. engineering-skills checks the example and the installer's output against these rules.
