# AwesomeBuild

## Philosophy

Similar to Makefiles, AwesomeBuild is structured in rules. Each rule may depend on other rules and may include so-called _triggers_, which are used to check whether the rule needs to run.

## Usage
```
usage: AwesomeBuild [-h] [--config CONFIG] [targets [targets ...]]

Awesome build manager to replace Makefiles. It allows very fast building!

positional arguments:
  targets          defaults to the main rule defined in the config file

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  default: awesomebuild.json
  --status STATUS  Relative to project folder, default: awesomestatus.json
  -j JOBS          Maximum number of jobs running in parallel. Defaults to the
                   number of cores available.
  --updater        Run Updater to fix deprecations.
```
## Configuration

First off, you need to create a configuration file called `awesomebuild.json` in your project´s main directory.

```json
{
  "project": "TestProject",
  "import": {
    "rules": []
  },
  "main": "mainrule",
  "rules": {}
}
```
Empty properties can be omitted.

Property overview:

`project`: project name

`import`: Here you can define which external configuration files you want to import. The currently only available import type is `rules`.

`main`: This defines which rule to run if no targets were defined by the user. This rule may be defined in an external configuration file.

`rules`: Here you can define rules.

### Rule Definition

```json
"rule-name": {
  "cmd": [
    "cmd1",
    {
      "type": "the-type",
      "cmd": "cmd-1",
      "rule": "rule-2"
    }
  ],
  "call":[
    "other-rule-1",
    "other-rule-2"
  ],
  "callBefore": [
    "other-rule-3",
    "other-rule-4"
  ],
  "callAfter":"other-rule-5",
  "trigger": [],
}
```
All properties may be omitted or provided as single value or list.
`"property": "hello world"` is the same as `"property": ["hello world"]` and `"property": []` is the same as omitting `property`.

`cmd`: This defines (shell) commands to be executed.
There are two for defining a command:
1. `"cmd"` defines a simple shell command.
2. Calling a command or a rule may be defined as json. It allows calling other rules between shell commans and not only after all shell command compared to the deprecated property `call`.
```json
  {
    "type": "the-type",
    "cmd": "cmd-1",
    "rule": "rule-2"
  }
```
  Properties:
  `type`: This property defines whether this command is a shell command (`cmd`), a rule (`rule`) or a internal command for AwesomeBuild (`AwesomeBuild`).
  `cmd`: This property defines the shell command or thw internal command for AwesomeBuild.
  `rule`: This property defines the name of the rule to be executed.

All shell commands run in the main project directory.

`callBefore`: This property handles all rules that need to run before.

`callAfter`: This property handles all rules that need to run after. There is a little difference to `call`. Check [Rule Execution](#rule-execution).

`trigger`: This property handles the rule´s triggers.

Deprecated properties:

`call`: This property handles other rules which will run. It should be migrated in the `cmd` property.

#### Internal Commands
Sometimes rules need to communicate with the current instance of AwesomeBuild. The following commands are currently know:
- `reset-status`: Resets the status file to its defaults.

#### Trigger Definition
```json
{
  "type": "trigger type",
  "subtype": "trigger sub type",
  "value": "value for trigger"
}
```

Currently known triggers are:

type | subtype | value usage
--- | --- | ---
file | changed | path to file
file | exist | path to file
file | not exist | path to file
directory | changed | path to directory
directory | exist | path to directory
directory | not exist | path to directory

### Import Rules

```json
{
  "rules": "name",
  "type": "importtype",
  "value": "path"
}
```

Property overview:

`rules`: This can either be the name of a single rule `"rules": "rulename"`, a list of rules `"rules": ["rule-1", "rule-2"]` or a wildcard `"rules": "*"` to import all rules found.

`type`: This defines whether a single file or a whole directory (recursively) is imported.

`value`: This defines the path to the file or directory.

## Rule Execution
1. If `callBefore` rules are defined, these rules will be executed now. If any of these were executed since the current rule was executed for the last time, the run variable will be set. Check [Status Property _rules-callBefore_](#status-property-rules-callbefore).
2. If `trigger`s are defined, these will be checked now. If any of these triggers was positive or no triggers were defined, the run variable will be set.
3. If the run variable is set, the `cmd`s will run now.
4. If the run variable is set, the `call -rules will run now.
5. If `callAfter` rules are defined, these rules will run now.

## In-depth information
### Status File
To allow fast builds (skipping build steps) it is necessary to save some information about the last known-as-built state of the source and build files. Therefore AwesomeBuild saves many hashes, which are checked upon rule execution. If there is a hash mismatch AwesomeBuild triggers a rebuild.
All information is saved in the file `awesomestatus.json`. Most of its content consits of SHA512 hashes to prevent easy manipulation.

#### Status Property _awesomestatusversion_
From time to time the structure of the status file will change. Therefore the version of the file is saved as an integer. Upon loading, AwesomeBuild will check the version and update the status file as needed.

#### Status Property _configstatus_
When the configuration is changed, AwesomeBuild will trigger a rebuild. To check for configuration changes, it generates a SHA512 hash of the complete configuration. If AwesomeBuild detects a hash mismatch, it clears the `rules`, `rules-callBefore` and `triggers` properties of the status file.

#### Status Property _rules_
After a rule was executed, AwesomeBuild saves a SHA512 hash of the string of python´s `time.time()` function.

#### Status Property _rules-callBefore_
Each rule must know whether its callBefore rules were executed. This is checked by generating a SHA512 hash over the combined string of all affected rules´ time hash. By using this approach, we can just run all callBefore rules without caring whether they really run, because we need to check for rules that were executed before anyway.

#### Status Property _triggers_
Each trigger may need to save its status information. Check [Trigger](#trigger)

### Trigger
#### (Not) Exist Triggers
The technique of checking whether a file/directory exists should be quite clear ;-)

#### Changed Triggers
The most efficient way to check for file/directory changes would be to use inotify. Therefore we would need to have a script running all the time. This might be implemented in a later version.

##### File Changed Trigger
To check whether a file was changed AwesomeBuild generates a SHA512 hash over the file´s content.

##### Directory Changed Trigger
Directories can be quite large in both count and size of files. Generating a checksum over all file contents would be very inefficient. Therefore AwesomeBuild generates a checksum over as much as possible metadata. It generates a SHA512 hash over the output of `ls -RlgAGi --time-style=+%s PATH`. This way it should be quite safe to trigger a rebuild upon file changes. If you have a better solution feel free to open an issue/PR :)

### Multithreading
To allow faster building AwesomeBuild allows multithreading. Normally the number of maximum running jobs is defined by the count of CPU cores. With the `-j` argument it is possible to overide this value.

#### Collision Prevention
To prevent the parallel execution of the same rule the JobManager preserves a list of rules that are in any kind of execution state. If a second instance of the same rule is started, the session manager will prevent it from being executed and hold it until the first instance is unregistered.

#### Thread Count Limitation
To limit the count of parallel running threads the JobManager preserves a list of rules that are currently executing a command. If a rule wants to run a command it has to wait until the count of currently running commands is lower than the maximum allowed threads.
