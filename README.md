##How to prepare state
```shell
$ terraform plan -out=plan.out
$ terraform show -json plan.out > plan.json
```

##Resources that Support Diff Detection
The following resource types support diff detection.

Service | Resource
------------ | -------------
IAM | AWS::IAM::Group <br /> AWS::IAM::InstanceProfile <br /> AWS::IAM::ManagedPolicy <br /> AWS::IAM::Role <br /> AWS::IAM::User
CloudWatch | AWS::CloudWatch::ListDashboards 
Lambda | AWS::Lambda::Function
Amazon RDS | AWS::RDS::DBInstance
Amazon SNS | AWS::SNS::Topic
## License

This code is released under the Apache 2.0 License. Please see LICENSE for more details.

Copyright © 2020 Anton Shakh