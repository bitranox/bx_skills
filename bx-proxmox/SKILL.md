---
name: bx-proxmox
description: >-
  Use when configuring, managing, or troubleshooting Proxmox VE -
  installation, host administration, clusters, VMs, containers,
  storage, Ceph, SDN, firewall, user management, HA, backups,
  notifications, and CLI tools. Covers Proxmox VE 9.1.2.
---

# Proxmox VE Administration Guide (Release 9.1.2)

Reference documentation for Proxmox VE administration extracted from
the official admin guide. Use the Read tool to load files relevant
to the current task.

## Which File Do I Need?

| I need to...                       | Read                                        |
|------------------------------------|---------------------------------------------|
| Understand PVE features            | `ch01-introduction.md`                      |
| Install or upgrade Proxmox VE      | `ch02-installation.md`                      |
| Use advanced installer options     | `ch02-installation-advanced.md`             |
| Configure package repositories     | `ch03-host-admin/package-repositories.md`   |
| Set up networking                  | `ch03-host-admin/network-configuration.md`  |
| Manage ZFS on the host             | `ch03-host-admin/zfs.md`                    |
| Manage LVM on the host             | `ch03-host-admin/lvm.md`                    |
| Manage BTRFS on the host           | `ch03-host-admin/btrfs.md`                  |
| Configure certificates / ACME      | `ch03-host-admin/certificate-management.md` |
| Configure the bootloader           | `ch03-host-admin/host-bootloader.md`        |
| Monitor disk health                | `ch03-host-admin/disk-health.md`            |
| Set up time sync / NTP             | `ch03-host-admin/time-synchronization.md`   |
| Use the web GUI                    | `ch04-gui.md`                               |
| Create or manage a cluster         | `ch05-cluster-manager/_index.md`            |
| Understand pmxcfs                  | `ch06-pmxcfs.md`                            |
| Add or configure storage           | `ch07-storage/_index.md`                    |
| Deploy Ceph                        | `ch08-ceph/_index.md`                       |
| Set up storage replication         | `ch09-storage-replication.md`               |
| Create or manage VMs               | `ch10-qemu/_index.md`                       |
| Import a VM (OVF, disk images)     | `ch10-qemu/importing-vms.md`               |
| Set up PCI passthrough             | `ch10-qemu/pci-passthrough.md`              |
| Use Cloud-Init with VMs            | `ch10-qemu/cloud-init.md`                   |
| Create or manage containers        | `ch11-containers/_index.md`                 |
| Configure SDN                      | `ch12-sdn/_index.md`                        |
| Configure the firewall             | `ch13-firewall/_index.md`                   |
| Manage users and permissions       | `ch14-user-management/_index.md`            |
| Set up High Availability           | `ch15-high-availability/_index.md`          |
| Back up or restore VMs/CTs         | `ch16-backup-restore/_index.md`             |
| Configure notifications            | `ch17-notifications.md`                     |
| Manage PVE service daemons         | `ch18-service-daemons.md`                   |
| Find answers to common questions   | `ch20-faq.md`                               |
| Look up a CLI command              | `appendix-a-cli/_index.md`                  |
| Check firewall macros              | `appendix-f-firewall-macros.md`             |
| Understand config file format      | `appendix-c-config-files.md`                |
| Schedule jobs (calendar events)    | `appendix-d-calendar-events.md`             |
| Look up QEMU vCPU types           | `appendix-e-vcpu-list.md`                   |
| Daemon CLI (pve-firewall, etc.)    | `appendix-b-service-daemons.md`             |

---

## Chapter Detail (tier 2)

For topics not in the quick-lookup table, find the right chapter here,
then read its `_index.md` for sub-topic routing to individual files.

| Topic — key terms                                                                                  | Chapter index                    |
|----------------------------------------------------------------------------------------------------|----------------------------------|
| Host Admin — repos, updates, firmware, networking, bonding, VLANs, NTP, metrics, disk health, LVM, ZFS, ZFS encryption, BTRFS, node management, certs, ACME, bootloader, GRUB, Secure Boot, KSM | `ch03-host-admin/_index.md`      |
| Cluster — create, join, quorum, corosync, QDevice, cluster network, remove node, rejoin            | `ch05-cluster-manager/_index.md` |
| Storage backends — Dir, NFS, CIFS, PBS, ZFS pool, LVM, LVM-thin, iSCSI, Ceph RBD, CephFS, BTRFS, ZFS-over-iSCSI | `ch07-storage/_index.md`         |
| Ceph — install, config, monitors, managers, OSDs, pools, CRUSH, CephFS, client, maintenance        | `ch08-ceph/_index.md`            |
| QEMU/KVM — settings, hardware, CPU, memory, encryption, display, USB, PCI, boot, migration, clones, templates, import, cloud-init, passthrough, hookscripts, hibernation, resource mapping, qm, locks | `ch10-qemu/_index.md`            |
| Containers — LXC, distributions, images, settings, security, apparmor, storage, backup, migration, pct config, locks | `ch11-containers/_index.md`      |
| SDN — zones, VNets, subnets, controllers, fabrics, IPAM, DNS, DHCP, firewall integration           | `ch12-sdn/_index.md`             |
| Firewall — directions, zones, cluster.fw, host rules, VM/CT rules, security groups, IP sets, nftables | `ch13-firewall/_index.md`        |
| Users — users, groups, tokens, pools, auth realms, LDAP, AD, OpenID, 2FA, TOTP, WebAuthn, permissions, ACLs, roles | `ch14-user-management/_index.md` |
| HA — resources, groups, fencing, watchdog, error recovery, maintenance, scheduling                  | `ch15-high-availability/_index.md` |
| Backup — modes (snapshot/suspend/stop), fleecing, compression, encryption, jobs, retention, restore | `ch16-backup-restore/_index.md`  |

---

## CLI Reference (Appendix A)

| Tool              | File                                                    |
|-------------------|---------------------------------------------------------|
| -                 | [general-and-format-options.md](appendix-a-cli/general-and-format-options.md) |
| `pvesm`           | [pvesm.md](appendix-a-cli/pvesm.md)                     |
| `pveceph`         | [pveceph.md](appendix-a-cli/pveceph.md)                 |
| `pvenode`         | [pvenode.md](appendix-a-cli/pvenode.md)                  |
| `pvesh`           | [pvesh.md](appendix-a-cli/pvesh.md)                     |
| `qm`              | [qm.md](appendix-a-cli/qm.md)                           |
| `qmrestore`       | [qmrestore.md](appendix-a-cli/qmrestore.md)             |
| `pct`             | [pct.md](appendix-a-cli/pct.md)                         |
| `pveam`           | [pveam.md](appendix-a-cli/pveam.md)                     |
| `pvecm`           | [pvecm.md](appendix-a-cli/pvecm.md)                     |
| `pvesr`           | [pvesr.md](appendix-a-cli/pvesr.md)                     |
| `pveum`           | [pveum.md](appendix-a-cli/pveum.md)                     |
| `vzdump`          | [vzdump.md](appendix-a-cli/vzdump.md)                   |
| `ha-manager`      | [ha-manager.md](appendix-a-cli/ha-manager.md)           |

