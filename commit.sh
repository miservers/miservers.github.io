
pwd=$(pwd)
commit() {
  repo=$1
  echo "Repo: $repo"
  cd $repo
  git pull
  git add .
  git commit -m poco
  git push
}
 commit ~/provision-k8s
 commit ~/miservers.gitlab.io
 commit ~/openshif-webapp
 
 cd $pwd


