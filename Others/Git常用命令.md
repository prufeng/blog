## Get Started
### Clone
```bash
git clone https://github.com/prufeng/hellowork.git

git remote show origin
git remote get-url origin
git remote remove origin
git remote add origin https://github.com/prufeng/hellowork.git
```

### Store/Unset Password
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
git status -s
```

### List Changed Files in Commit
```
git show --name-only --oneline HEAD
git show --stat --oneline HEAD

git log --stat --oneline HEAD
git log --name-only --oneline -2
git diff-tree --name-only -r <commit id>
```

### Amend
```
git commit --amend --only
git commit --amend --only -m 'xxxxxxx'
git commit --amend --author "New Authorname <authoremail@mydomain.com>"
```

### Add Change to Last Commit
```
git add .
git commit --amend
```

### Add Some Change in File
```
git add -p <file>
```

### Discard changes in File
```
git checkout <file>
git checkout HEAD <file>
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
### Remove File
```
git rm --cached <file>
```

### Remove File from Last Commit
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
### New Branch Without Local Changes
```
git checkout -b current_feature
git add .
git commit -m "Add current feature"

git checkout master
git checkout -b new_feature_without_current_feature
```

### Push Commit from New Branch
```
git checkout new_feature_without_current_feature   
git cherry-pick <commit id>
git push origin HEAD:master
```
