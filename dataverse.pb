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
    mail_relay: smtp.johnshopkins.edu
    dv_ui_use_custom_header: true
    dv_ui_repo:
      url: "https://github.com/jhu-sheridan-libraries/dataverse.git"
      branch: "2003-instance-branding-on-v4.6"
    dv_ui_custom_values:
      - { prop: ":instanceLogoFile",
          val: "/resources/images/libraries.logo.small.horizontal.white.cropped.png",
          desc: "URL (relative or absolute) for instance logo file" }
      - { prop: ":instanceNameFull",
          val: "Johns Hopkins University Data Archive",
          desc: "Full branded name for this Dataverse instance" }
      - { prop: ":instanceNameShort", val: "JHU Data Archive",
          desc: "Short branded name for this Dataverse instance" }
      - { prop: ":instanceTextFull",
          val: "Johns Hopkins University Data Management Services",
          desc: "Full upper right-hand text for wider window" }
      - { prop: ":instanceTextShort", val: "JHU DMS",
          desc: "Short upper right-hand text for narrow window" }
      - { prop: ":instanceTextLink", val: "http://dms.data.jhu.edu/",
          desc: "Link for click on upper right-hand branding text" }
      - { prop: ":instanceLogoLink", val: "http://www.library.jhu.edu/",
          desc: "Link for click on instance branding logo" }
  roles:
    - role: dataverse
