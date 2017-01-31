# -*- mode: yaml -*-
# vi: set ft=yaml :

# run like this: ansible-playbook --vault-password-file <vault-password-file> -K -i <dataverse-host-name>, [-u <ssh-username>] dataverse.pb
# NB: Comma required for -i if only one hostname in list.
# NB: Use the hostname here, not the service name.
# e.g.: ansible-playbook --vault-password-file ~/.ansible/.vault-pw -K -i dms-dv01.mse.jhu.edu, dataverse.pb

---

- hosts: all
  become: yes
  become_user: root
  become_method: sudo
  vars_files:
    - VAULT.yaml
  vars:
    load_mdblocks: true
  roles:
    - role: dataverse
