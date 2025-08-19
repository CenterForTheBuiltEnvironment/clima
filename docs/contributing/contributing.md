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



## Code of Conduct

Available [here](code_of_conduct.md)

## Code style

We use Black.exe to format the code.

## Submitting changes

Please send a Pull Request with a clear list of what you've done. Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

```text
$ git commit -m "A brief summary of the commit
> 
> A paragraph describing what changed and its impact."
```

## Thanks

Thank you again for being interested in this project! You are awesome!

