# CuteJoe
> Commands to automate some release tasks.

![Comb](./comb.svg)

## Installation

### Or on the local machine
```sh
pip install cutejoe
```

## Usage

Some commands are available on CLI. To see all available commands, type:

```sh
cutejoe --help
```

## Commands

### Configuration File
> Script to create default configuration file.

```sh
cutejoe config-file --help
```

`start` and `end` are the range commits to get the log messages.
`folder` is where the changelogs will be saved.
`kinds` are composed of:
    - labels (prefix of the commit messages),
    - title (title of this kind section),
    - version (`major`, `minor` or `patch`).
`default_title` is the title used if the commit message has no valid kind.

### Changelog
> Script to generate changelog based on the commit messages.

```sh
cutejoe changelog --help
```

#### Changes on changelog generation

For every PR, the reviewer will be required to follow this pattern when "squash and merge" the PR:

`<kind>:<message>`

The kind and message must be written by the PR owner on the PR message. The reviewer must only copy the kind and message to the merge commit body.


**\* Valid kinds:**
- `break`: fix or feature that would cause existing functionality to not work as expected;
- `add`: non-breaking change that adds functionality;
- `change`: non-breaking change that changes existing functionality;
- `deprecate`: non-breaking change that deprecates existing functionality;
- `remove`: non-breaking change that removes existing functionality;
- `security`: non-breaking change that fixes existing vulnerability;
- `fix`: non-breaking change that fixes existing issue.

(kinds are defined on the configuration file)

\*\*If someone forget to prefix with the kind, the message will be on the `Uncategorized` subsection.


_Example:_

`add:script to generate changelog based on commit messages`  *<- THIS MESSAGE MUST BE COPIED TO THE MERGE COMMIT MESSAGE*


#### Changes on release and tag process

When a release is to be made, we checkout to the `develop` specific commit and run this command:

```sh
cutejoe changelog
```

The changelog is created to the `/changelog` folder and the release branch name is printed on the screen, like `release/v1.0.1`

#### Template for the `.github/PULL_REQUEST_TEMPLATE.md` of your project

In order to standardize the PR commit messages, it's desirable to create/change the `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Squash and Merge Message

Please write the merge message:

`<type*>:<message>`

**\* Valid types:**
- `break`: fix or feature that would cause existing functionality to not work as expected;
- `add`: non-breaking change that adds functionality;
- `change`: non-breaking change that changes existing functionality;
- `deprecate`: non-breaking change that deprecates existing functionality;
- `remove`: non-breaking change that removes existing functionality;
- `security`: non-breaking change that fixes existing vulnerability;
- `fix`: non-breaking change that fixes existing issue.
```
(kinds are defined on the config file, change the valid types section according to your config file)

### Template for the `README.md` of your project

It's advisable to inform on the `README.md` the PR commit pattern adopted by your project:

```markdown
This project follows the [CuteJoe PR commit pattern and changelog](https://github.com/MatheusBrochi/CuteJoe).
```

## TODOs

- Commands to automate the entire release process (create branch, change version, etc);
