ELK - Active Directory LDAP User Authentication
===
Elasticsearch Active Directory踩坑记录。

# Active Directory和LDAP是不同的配置
Active Directory的配置要简单的多。

关键是，AD直接是用ID（sAMAccountName）来验证，即`dn='id@example.com'`，所见即所得。

```yml
xpack:
  security:
    authc:
      realms:
        active_directory:
          my_ad:
            order: 0 
            domain_name: example.com
            url: ldaps://ad.example.com:636 
```

测试发现，类似如下配置，登陆时，使cn=id，但实际上，AD里的cn却根本就不是ID，而是一个描述性的名称，所以肯定验证不成功。

AD和LDAP背后的验证机制还是有些不一样。

```yml
xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 0
            url: "ldaps://ldap.example.com:636"
            user_dn_templates:
              - "cn={0}, ou=users, o=marketing, dc=example, dc=com"
              - "cn={0}, ou=users, o=engineering, dc=example, dc=com"
            group_search:
              base_dn: "dc=example,dc=com"
            files:
              role_mapping: "/mnt/elasticsearch/group_to_role_mapping.yml"
            unmapped_groups_as_roles: false
```

使用`bind_dn`和`user_search`配置的话还需要绑定密码。
```yml
xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 0
            url: "ldaps://ldap.example.com:636"
            bind_dn: "cn=ldapuser, ou=users, o=services, dc=example, dc=com"
            user_search:
              base_dn: "dc=example,dc=com"
              filter: "(cn={0})"
            group_search:
              base_dn: "dc=example,dc=com"
            files:
              role_mapping: "ES_PATH_CONF/role_mapping.yml"
            unmapped_groups_as_roles: false
```

# Role Mapping

Role mapping主要是用来测试的，可以找到用户实际cn填进去测试。

vi role_mapping.yml
```yml
superuser:
  - "cn=users,dc=example,dc=com"

```
实际使用应该是保存到Elasticsearch比较多，Kibana提供了配置的页面：`Stack Management -> Security -> Role Mappings`。
```
PUT /_security/role_mapping/basic_users
{
  "roles" : [ "user" ],
  "rules" : { "field" : {
    "groups" : "cn=users,dc=example,dc=com" 
  } },
  "enabled": true
}
```

# 开Debug

最有用的其实是开Debug，一开始错误信息太少，只看到简单的`authenticate failed`，根本就不知道到底哪里出了问题。
```
[2022-05-10T09:19:35,785][WARN ][o.e.x.s.a.RealmsAuthenticator] [] Authentication to realm ldap1 failed - authenticate failed (Caused by LDAPException(resultCode=49 (invalid credentials), diagnosticMessage='80090308: LdapErr: DSID-0C09044E, comment: AcceptSecurityContext error, data 52e, v2580', ldapSDKVersion=4.0.8, revision=28812))
```

开了TRACE以后，可以看到用户LDAP验证过程信息，包括用户组匹配之类， 按实际用户信息配置role mapping即可。

```
PUT /_cluster/settings 
{ 
  "transient": { 
     "logger.org.elasticsearch.xpack.security.authc.ldap":"TRACE", 
   } 
}

# Or vi elasticsearch.yml
logger.org.elasticsearch.xpack.security.authc.ldap: TRACE
```

# ldapsearch

怀疑人生的时候，可以用其他工具试试。
```
ldapsearch -x -h ad.example.com -p 389 -D "testuser@example.com" -W -b "dc=example,dc=com" cn

-D binddn  bind DN
-b basedn  base dn for search
-x         Simple authentication
```
