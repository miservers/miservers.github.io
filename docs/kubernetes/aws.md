

### Aws cli depuid Termux
1. Install cli: `pip install awscli`
2. creer/donner les droits au user: IAM → Users → aws-cli-poco → Add permissions → Attach policies directly → chercher AdministratorAccess
2. Creer une paire de clé: IAM > Users 
3. Configure le cli: `aws configure` saisir api key/secret, eu-west-3, json
4. Test connexion: `aws sts get-caller-identity`

### Commands aws cli
- Liste de volumes: `aws ec2 describe-volumes`
- 

### Se connecter sur VM ec2 avec clé ssh
1. Fixer les droits sur la clé ssh
~~~
 chmod 0600 aws-redm-key.pem
~~~

2. se connecter
~~~
~$ ssh  ec2-user@node-3 -i aws-redm-key.pem
~~~

cela peut etre automatiser en ajoutant dans *~/.ssh/config*
~~~
Host node-*
  User ec2-user
  IdentityFile ~/aws-redm-key.pem
~~~

Pour une instance Ubuntu, le user est **ubuntu**

