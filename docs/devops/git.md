---
layout: default
title: Git
parent: DevOps
nav_order: 2.5
---


## GIT
clone the repository

    git clone --depth 2 https://github.com/magos3/magOS



### Commit
```
  git add -A
  git commit -a -m "comment"
  git push origin master
```

### Checkout
```
  git pull
```

### Misc
```
 make clean
 git pull origin
 git reset --hard origin/master
 git add *
 git commit -a -m "comment"
 git push origin master
```

### Cleanup git commit history
```
  cd /root
  git clone --depth 2 https://github.com/magos3/magOS
  cd magOS/
  git checkout --orphan latest_branch
  git add -A
  git commit -am "cleanup history"
  git branch -D master
  git branch -m master
  git push -f origin master
```
  
### Cannot commit with error like repo is MERGING
```
  - resolve conflicts
  - git add: essencial 
  - git commit
  - git push
```

### Git Password prompt
Make git dont ask for usr/password
```
  git clone ...
  cd magOS
  git config credential.helper store
  git config --global user.email magos3@magos
  git config --global user.name magos3
  ./commit.sh
```

### Git with Proxy (Ubuntu)
```
   export http_proxy="http://proxi-ip:8080"
   git config --global http.proxy $http_proxy
   git clone --depth 1 https://github.com/magos3/magOS
```
  
## Alias
add these alias to *.bashrc* or *.profile*
    
    alias cdm='cd ~/magOS'
    alias commit='cd ~/magOS/tools; ./commit.sh ; cd -'
    alias checkout='~/magOS/tools; ./checkout.sh; cd -'


  
