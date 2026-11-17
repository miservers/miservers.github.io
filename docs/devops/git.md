---
layout: default
title: Git
parent: DevOps
nav_order: 2.5
---
  
### Bitbucket
**Droits**
    - groups: dev-team, ops-team
    - droits pour les devs: project=read, repo=write
    - dans project->worflow-> branch restrictions créer les droits 
        • Les branches int=devs/ops/write, main=ops/write
        • Mergd Settings: cocher number minimal of approval = 1 et from reviewers à 1( sur la branche main)


**Branching model**
Projet->Worflow->Branching model
Définir les branches de dev et prod ainsi qu'es les branches features/hotfix/release

**Merge Stratégie : Projet->Worflow->Merge strategies**
    - Merge commit = standard GitOps ✅. 
       • PR visible: Oui
       • Complexité faible 
    - Fast forward (Pas de commit de merge)
       • PR visible: non
       • Historique linéaire et propre
       • Complexe car il faut que les branches soient à jour, sinon il faut faire un rebase

**Commiter**
  - Ne jamais faire un push direct , toujours passer par un PR
  - pour l'int, créer une branches sous feature/my-modif puis faire un PR sur l'int
 


### Clone the repository

    git clone https://github.com/your-repo



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


### Branches
**Switch Branch**
~~~sh
$ git checkout <existing_branch>

$ git checkout -b <new_branch>
~~~

**Current branch**
~~~sh
git branch`
~~~

**Commit on a branch**
~~~sh
git push origin <branch_name>
~~~

**Make a branch as default for commit**
~~~sh
git push --set-upstream origin <branch_name>
~~~

Now you can commit on your branch as
~~~sh
git add .
git commit -m "aa"
git push
~~~

### Tags
Create a tag:
~~~sh
git tag -a v1.4 -m 'version 1.4'
~~~

Push/push Tags
~~~sh
 git [push | pull] --tags
~~~

List of tags
~~~sh
git tag
~~~

### Commands
**Display current branch**
~~~
git branch
~~~

**Update local with remote**
~~~
git pull [origin branch_name]
~~~



**Switch to a branch**
~~~
git switch branch_name
~~~

**Create a branch and switch to it**
~~~
git switch -c br1
~~~

**Is there is something to commit**
~~~
git status 
~~~

**Commit**
~~~
git add -A
git commit -m "e"
git push
~~~

**Reset / Pull / Fetch**

- ```git reset```: Adjusts your local repo, undoing changes or moving commits.

- ```git fetch```: Downloads remote updates without merging.

- ```git pull```: Fetches and merges remote changes into your branch.

**Undo local modifications**
~~~
git reset --hard origin/recette
~~~

**Removing local untracked files:**
~~~
git clean -f

Remove untracked files and directories:

git clean -fd
~~~


### Rollback modification
For example to reset the master branch to a previous state (commit hash 80c93fd6)

```
git switch master
git pull
git reset --hard 80c93fd6
git push origin master --force
```

**List of commits**
~~~
git log
~~~
or: <br>
<a>gitlab-> project -> Code -> commits</a>


Error: You are not allowed to force push code to a protected branch on this project.

 => in gitlab -> <a>Project Settings -> Repository -> Branch rules -> Allow force push</a>


### Modif en Recette
~~~sh
git checkout rec  
git pull origin rec  
git checkout -b fix-rec  # Créez 

git add .  
git commit -m "Correction"
git push origin fix-rec

~~~

Ensuite créer un merge request pour fusionner fix-rec dans rec.

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
  
### Alias
add these alias to *.bashrc* or *.profile*
    
    alias cdm='cd ~/magOS'
    alias commit='cd ~/magOS/tools; ./commit.sh ; cd -'
    alias checkout='~/magOS/tools; ./checkout.sh; cd -'



### Hard , Soft Reset
Réinitialiser complètement l'État de ton repository à un commit spécifique.

Attention: cela va supprimer tous les commit qui ont été effectués après ce commit

1. identifier le numero commit
2. désactiver temporairement le protect sur la branche master: *Setting->Repository->Protected Branchs*
3. faire un hard reset 
  ~~~
  git reset --hard|--soft <commit_id>
  ~~~

4. vérifier les fichiers qui ont été modifiés
  ~~~
  git status
  git log --oneline
  ~~~


5. pousser le commit
  ~~~
  git push origin HEAD --force
  ~~~

### Runners
Les Jobs sont executé sur un docker

~~~
stages :
     - build

build_1 :
     image : openjdk:17-jdk-alpine
     stage : build
     # Possible d'utiliser Gradle car le JDK est disponible
     script :  ./gradlew build
~~~

### Erreurs
**You have divergent branches and need to specify how to reconcile them**

- ta branche locale et la branche distante ont divergé — chacune contient des commits que l’autre n’a pas. Comment tu veux les fusionner?
- **Rebase**: rejoue tes commits locaux au-dessus des commits distants -> Propore
  
  ``git pull --rebase``

- **Merge**: crée un commit de fusion
  
  ``git pull --no-rebase``
  