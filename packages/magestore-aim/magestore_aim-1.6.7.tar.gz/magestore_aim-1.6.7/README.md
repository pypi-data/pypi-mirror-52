## Original 
This repo has been moved from [auto_install_magento_package](https://gitlab.com/general-oil/infrastructure/tree/master/Tool/auto_install_magento_package)


## How to use
This package provided function *install_magento* for install magento using [magento-apache](https://gitlab.com/general-oil/infrastructure/tree/master/Environment/Magento/DemoPortalApache) running on docker engine.<br/>
The function has required params:
+ **env_params**: (type:dict) 
  + *magento_version*: (type:str) x.x.x  
  e.g: 2.2.5
  + *magento_type* (optional): (type:str) **ce** (Comunity Edition) or **ee** (Enterprise Edition), default **ce**
  + *sample_data* (optional): (type:bool) **True** or **False**, default **False**
  + *performance_test*: (type:bool) True or False (this key only has effective and required when sample_data is False)
  + *peformance_test_profile* (optional): (type:str) (this key only has effective and required when sample_data is False and performance_test is True) 
  valid values : **small**, **medium**, **medium_msite**, **large**, **extra_large**
  + *php_version* (optional): (type:str) **x.x.x**, default **7.1.25**  
+ **server_params**: (type:dict)
  + *ip*: (type:str) remove server ip address
  + *user*: (type:str) remote server username
  + *key_path*: (type:str) local private key file path to conect to remote server
  + *password*: (type:str) remote server password (if *key_path* has value, this key is optional)
+ **gitlab_access_token**: (type:str) gitlab_access_token that have permission to access to [infrastructure](https://gitlab.com/general-oil/infrastructure) repo  
[How to get gitlab access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

1. Install package *magestore-aim*
2. Import function to other file
```python
from magestore_aim import install_magento
```
3. Execute it and wait for result
