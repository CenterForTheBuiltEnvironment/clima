---
description: Guide on how to contribute to this project
---

# How to contribute

First off, thanks for taking the time to contribute!

## General Feedback

If you have a general feedback about our project, please do not open an issue but instead please fill in this [form](https://forms.gle/LRUq3vsFnE1QCLiA6)

## Code of Conduct

Available [here](code_of_conduct.md)

## Code style

We use ruff to enforce the code style and code formatting. You can run it with:

```bash
pipenv run ruff check .
pipenv run ruff format .
```

To ensure that your code is formatted correctly, we have a pre-commit hook that will run ruff before every commit.
Hence, you will need to make that the code is formatted correctly before committing your changes otherwise the commit will fail.
More information about pre-commit hooks can be found [here](https://pre-commit.com/).

## Submitting changes

Please send a Pull Request with a clear list of what you've done. Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

```text
$ git commit -m "A brief summary of the commit
> 
> A paragraph describing what changed and its impact."
```

## Thanks

Thank you again for being interested in this project! You are awesome!

