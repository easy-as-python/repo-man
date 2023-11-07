# 3. Use a configuration file to store repository flavors

Date: 2023-11-07

## Status

Accepted

## Context

Common approaches to tagging on file systems are filename embedding and sidecars[^1]. When working with repositories under version control, these approaches don't work well because they require changing file names or adding new files to the repository, both of which incur additional repository actions to commit, ignore, or otherwise manage the changes. Other approaches such as [macOS tags](https://support.apple.com/guide/mac-help/tag-files-and-folders-mchlp15236/mac) and [extended attributes](https://www.man7.org/linux/man-pages/man7/xattr.7.html) are either too platform-specific or don't work well at the command line.

These approaches mainly seek to be able to abstract the tagging implementation completely from the consumer. The consumer using repo-man is trusted instead to know a bit about the tagging system because if they have the problems repo-man solves they're already more likely to care about or be accepting of a mild level of configuration burden.

## Decision

Use a separate configuration file for tagging directories.

## Consequences

- No repository has to know about the details of repo-man at all
- Consumers will need to know about and manage repo-man configuration, the burden of which can be mitigated by tooling
- The repo-man file is prone to loss because it isn't under version control

[^1]: [https://unix.stackexchange.com/a/388201](https://unix.stackexchange.com/a/388201)
