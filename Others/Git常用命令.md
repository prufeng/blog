## Clone
```bash
git clone https://github.com/prufeng/hellowork.git

git remote show origin
git remote get-url origin
git remote remove origin
git remote add origin https://github.com/prufeng/hellowork.git
```

## Store/Unset Password
```
git config --global credential.helper store
git config --global --unset credential.helper
```
## Changes
### Commit
```bash
echo "Helloworld" >>README.md
git add .
git commit -m "First commit"
git commit -m 'Multiple lines comment

1. Fix bug 1
2. Fix bug 2'

git push
```

### Status
```
git status
```

### Amend
```
git log -1
git show
git log -1 -p

git commit --amend --only
git commit --amend --only -m 'xxxxxxx'
git commit --amend --author "New Authorname <authoremail@mydomain.com>"
```

### Add Change to Last Commit
```
git add .
git commit --amend
```

### Add Some Change in <file>
```
git add -p <file>
```

### Discard changes in <file>
```
git checkout <file>
```

### Undo Add
```
git reset
```

### Reset Commit
```
git reset HEAD~
git reset HEAD~1
git reset <commit id> <--soft|mixed|hard>
```
### Remove <file>
```
git rm --cached <file>
```

### Remove <file> from last commit
```
git checkout HEAD~ <file>
git add .
git commit --amend
```
### Find back Hard Reset
```
git reflog -2
git reset --hard <commit id>
```

### Stash 
```
git stash
git pull
git stash pop

git push
```

### Cherry Pick
```
git cherry-pick <commit id>
```

## Branch
### Pull Wrong Branch
```
git reflog
git reset --hard <commit id>
```

### Align Local with Remote
```
git reset --hard origin/master
```
### Checkout From Remote Branch
```
git fetch --all
git checkout --track origin/<branch>
git checkout -b <branch> origin/<branch>
```
### Delete Branch
```
git branch -D <branch>
git push origin --delete <branch>
```
### Restore Deleted Branch
```
git reflog
git checkout -b <new-branch>
git reset --hard <commit id>
```

### Fallback Rebase and Merge
```
git reset --hard ORIG_HEAD
```