# AWS VPC Configuration for lambda/zappa
- lambda need to configured with subnets which has both NAT and IGW access. So it can access RDS like services within 
AWS and access Internet resources through NAT.
- Ref:
    https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-nat-gateway.html
    https://aws.amazon.com/premiumsupport/knowledge-center/internet-access-lambda-function/
    https://gist.github.com/reggi/dc5f2620b7b4f515e68e46255ac042a7
    http://marcelog.github.io/articles/aws_lambda_internet_vpc.html
- create a public subnet
- when creating NAT Gateway use this public subnet
- create two route tables for each of IGW and NAT
- create three or more private subnet pointing to NAT
- set these subnets in zappa settings
- update ACL as recommended here for public and private subnets in scenario 2
    https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Appendix_NACLs.html

# Create new Cloud9 instance
- after creating cloud9 environment, go to the security group of RDS instance 
and updated the inbound rules to allow mysql-aurora source from security group of Cloud9 IDE


# setting up Gitlab CI/CD
1. created the gitlab.ci.yml file from one of its sample for a django project with test job
2. It is failing and decided to test it on cloud9 first
    i. first adding gitlab repo to cloud9 by
        ```
        curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash
        ```
    ii. installing gitlab runner
        ```
        sudo yum install gitlab-runner
        ```
    iii. installing docker - it is already installed 
    iv. running inside cloud9 using gitlab runner. The same can be used in local machine as well. 
        ```
        gitlab-runner exec docker test
        # here test is the name of the job
        ```
    v. **Debug only:** to login to the docker shell
        a. start mysql service
        
        ```
         docker run --name mysql57 -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=easybookingdb -d mysql:5.7
        ```
        
        b. interactive shell
        
        ```
        sudo docker run -it -p 8000:8000 python:latest /bin/bash
        
        # to mount the current directory inside
        sudo docker run -v $(pwd):/root/app -it python:latest /bin/bash
        ```
  

# moving to RDS Aurora serverless
1. backup existing database with `zappa manage production dbbackup` 
2. Take a snapshot of the database.
3. From RDS dashboard click create and select Aurora mysql edition that supports serverless
4. Create project database with the command
```
zappa manage production create_db
zappa manage production migrate
```

# Moving to normal RDS from Aurora serverless
1. backup existing database by logging into cloud9 IDE environment and running 
```
pew workon bf
python manage.py dbbackup -z
```
2. create new RDS instance and give a database name as in config ``easybookingdb``
3. login to cloud9 environment and set the new DB URL and import back
`python manage.py dbrestore -z`
4. update environment variable **DB_HOST** in zappa_settings.json
