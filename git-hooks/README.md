## Why pre-commit hooks?

[Git pre-commit hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) are a simple way to ensure all code 
to be committed passes tests. To summarize [guidelines](http://codeinthehole.com/tips/tips-for-using-a-git-pre-commit-hook/) for writing hooks:

* Hooks should be version controlled
* Unstaged changes should be stashed before running hooks
* Remember that hooks are skippable - `git commit --no-verify`
* Search staged files for debugging code
* Consider checking commit messages for spelling errors
* Consider enforcing style checks

## Writing pre-commit hooks

* `touch pre-commit.sh`
* `chmod +x pre-commit.sh`
* Write code
* `ln -s ../../git-hooks/pre-commit.sh .git/hooks/pre-commit`

## Git tricks

Git commands useful for writing pre-commit hooks:

* Find files unstaged for commit: `git diff --name-status`
* Find files staged for commit: `git diff --cached --name-status`
