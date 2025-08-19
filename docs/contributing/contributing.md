---
description: Guide on how to contribute to this project
---

# How to contribute

First off, thanks for taking the time to contribute!

## General Feedback

If you have a general feedback about our project, please do not open an issue but instead please fill in this [form](https://forms.gle/LRUq3vsFnE1QCLiA6)

## Fork & branch processing

First fork the origin repository to your own github repository, then clone the repository to your local computer.

```bash
git clone https://github.com/Your Account name/clima.git
cd clima
```

Set up the upstream repository and check the output respositories.

```bash
git remote add upstream https://github.com/CenterForTheBuiltEnvironment/clima.git

git remote -v
```

The terminal should output a list:

- `origin → your Fork repository`
- `upstream → origin repository`

Check all branches.

```bash
git branch -a
```

The terminal will show a list of branches:

```bash
> * main
  	remotes/origin/HEAD -> origin/main
  	remotes/origin/development
  	remotes/origin/main
```

Pull the development branch first, and if the terminal does not notices you that you should try the second command.

```bash
git checktout development

git checkout -b development origin/development
```

Create a new branch in the development branch.

```bash
git checkout -b (your branch name)
```

Finally update and push to your repository branch if you modify the files.

```bash
git push origin (your branch name)
```

## Pull Request Regulation
**Time to submit PR:**

- User requirements/issues have been addressed or discussed in Issue and consensus has been reached.
- Changes have been minimised (small steps/phased submission) to avoid "mega PRs".

**Classification of Common PR Types:**

- `Main (Master)`: Stable branch, merge code that passes review and CI; merge and release every time,

- `Develop`: Continuous Integration branch for daily integration with multiple collaborators.
- `Feature/*`: feature development branch, cut out from main or develop, send PR to merge in after completing the feature.
- `Fix/*`: defect repair branch, the same process as feature
- `Release/*`: release preparation branch for freezing versions, fixing documentation, doing regressions and tagging.
- `docs/*`, `chore/*`, `refactor/*`, `test/*`: documentation, miscellaneous, refactor, test type branches.
- `Style`: style modification (does not affect the function): code formatting, space adjustment, naming rules unity.
- `Refactor`: Code Refactoring: Refactor existing code to improve maintainability.
- `Test`: Add or modify tests: add unit tests, integration tests, or modify test logic.
- `Chore`: Build Configuration, Dependency Management, CI/CD Configuration Updates.
- `Perf`: Performance Optimisation: Optimising code execution efficiency or memory usage.
- `Ci`: CI Configuration Related: Changing Continuous Integration Configurations for Github Actions, Travis, Jenkins, etc.
- `Build`: build system related: modify build scripts, packaging configuration.
- `Revert`: Rollback Commit: Undoing a Previous Commit
- `Security`: Security fixes, fixing security vulnerabilities, updating dependencies to prevent attacks.
- `Deps`: Dependency Management: Dependency Management/Adding, updating, and removing dependency libraries
- `Infra`: Infrastructure related: changes to development environments, containers, server configurations, etc.


## Code of Conduct

Available [here](code_of_conduct.md)

## Code style

We use Black.exe to format the code.

Install Black:

```bash
pipenv install black
```

Format your code before committing:

```bash
black .
```

## Testing

Before submitting a Pull Request, please make sure:
- All tests should pass.
- Make sure you have installed project dependencies:

```bash
npm install

pipenv install -r requirements.txt
```

From the root directory, run:

```bash
cd tests/node

npx cypress run
```

## Submitting changes

Please send a Pull Request with a clear list of what you've done. Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

```text
$ git commit -m "A brief summary of the commit
> 
> A paragraph describing what changed and its impact."
```

## Thanks

Thank you again for being interested in this project! You are awesome!

