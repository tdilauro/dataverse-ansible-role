# Dataverse 4 Ansible Role & Example Playbook
Install and configure Dataverse 4

Installation, customization, administration, and API documentation can be found in the [Dataverse 4 Guides](http://guides.dataverse.org/en/latest/).
The role installs PostgreSQL, Solr, GlassFish and other prerequisites, then deploys Dataverse.
Finally, it attempts to apply local instance configuration, metadata block (database and Solr), and UI customizations.

This role is heavily based on [dataverse-ansible](https://github.com/IQSS/dataverse-ansible) project.

---

### Usage
  * $ ansible-playbook [--vault-password-file \<vault-password-file>] [-K] -i \<dataverse-host-name>, [-u \<ssh-username>] dataverse.pb
  * e.g.: $ ansible-playbook --vault-password-file ~/.ansible/.vault-pw -K -i myhost.domain.edu, dataverse.pb

### Notes
* The comma after the hostname is needed if only one host is listed, which is probably the normal case.
* This role currently requires CentOS 7 and deploys all services on the same machine.

---

## Assumptions:
* Web certificates
  * All needed certificates and keys are already in the *certs* and *private* sub-directories
(respectively) of the */etc/pki/tls* directory.
  * Wildcard certificates are used and their files named as *star_\<dotted-sub-domain>.crt*.
  * The associated certificate chain files are named as *star_\<dotted-sub-domain>_interim.crt*.
  * Keys for the certificates are named as *star_\<dotted-sub-domain>.key*.
  * If this is not the case, either provide the appropriate certificates or modify
  the httpd [*ssl.conf.j2* template](roles/dataverse/templates/ssl.conf.j2) appropriately.

---

## Result
After completing this installation, you should have a working Dataverse 4 installation.

### Key components
* Apache httpd
  * Acts as a front-end (proxy) for glassfish (and for shibboleth, if used).
  * Default config location: */etc/httpd/conf.d*
  * # systemctl {stop|start|restart|status} httpd.
* GlassFish server (Java EE application server)
  * Default location: */user/local/glassfish4*
  * Default config location: */usr/local/glassfish4/glassfish/domains/domain1/config/domain.xml*
  * # systemctl {start|stop|restart|status} glassfish
* Solr (indexing)
  * Default schema location: */usr/local/solr/example/solr/collection1/conf/schema.xml*
  * # systemctl {start|stop|restart|status} solr
* Postgres (database)
  * Default data/config location: */var/lib/pgsql/9.3/data/*
  * # systemctl {start|stop|restart|status} postgresql-9.3
* Shibboleth
  * Provides capability for an alternative authentication provider.
  * Not activated in the default configuration

## Replicating Existing Data
If you wish to clone an existing installation, you should perform the following:
* On the source instance server
  * $ pg_dump -U postgres dvndb  >  \<source-db-dump-file>
  * Copy the content directory of the source instance to the content directory of this instance.
* On the target instace server
  * # systemctl stop glassfish
  * $ dropdb -U postgres dvndb
  * $ createdb -U postgres dvndb
  * $ psql -U postgres dvndb -f \<source-db-dump-file>
  * # systemctl start glassfish
  * $ curl http://localhost:8080/api/admin/index/clear
  * $ curl http://localhost:8080/api/admin/index
