#!/usr/bin/env python3
"""Extract Proxmox VE Admin Guide PDF into hierarchical markdown skill files.

Usage: python3 extract.py

Requires: pdftotext (from poppler-utils)
"""

import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).parent
PDF_PATH = BASE_DIR / "pve-admin-guide.pdf"

# PDF physical page offset: content page 1 = PDF page 23
PDF_OFFSET = 22


@dataclass
class Section:
    """A section to extract from the PDF."""
    id: str
    title: str
    pdf_start: int  # physical PDF page
    pdf_end: int    # physical PDF page (inclusive)
    output: str     # relative output path
    chapter_num: str = ""  # e.g. "3", "A"
    section_prefix: str = ""  # e.g. "3.1", "A.3"
    nav_parent: str = ""  # relative path to parent _index.md
    nav_root: str = "SKILL.md"  # relative path to SKILL.md
    see_also: list = field(default_factory=list)  # [(path, description)]


# ── Section definitions ──────────────────────────────────────────────
# PDF page mappings from analysis:
# Ch1:23, Ch2:32, Ch3:49, Ch4:119, Ch5:132, Ch6:158, Ch7:163,
# Ch8:195, Ch9:221, Ch10:225, Ch11:309(corrected:340), Ch12:340(corrected:367)
# etc. Let me use exact findings:
# Ch1:23-31, Ch2:32-48, Ch3:49-118, Ch4:119-131, Ch5:132-157,
# Ch6:158-162, Ch7:163-194, Ch8:195-220, Ch9:221-224, Ch10:225-308(corrected:339)
# Ch11:340-366, Ch12:367-385(corrected), Ch13:386(corrected)-408
# Actually, from exact findings:
# Ch1:23, Ch2:32, Ch3:49, Ch4:119, Ch5:132, Ch6:158, Ch7:163,
# Ch8:195, Ch9:221, Ch10:225, Ch11:309, Ch12:340, Ch13:367,
# Ch14:386, Ch15:409, Ch16:434, Ch17:450, Ch18:461, Ch19:467,
# Ch20:469, Ch21:472, AppA:474, AppB:616, AppC:623, AppD:629,
# AppE:632, AppF:634, AppG:647, AppH:651

SECTIONS = [
    # ── Chapter 1: Introduction (small, single file) ──
    Section("ch01", "Introduction", 23, 31, "ch01-introduction.md",
            chapter_num="1", section_prefix="1",
            see_also=[("ch02-installation.md", "Installing Proxmox VE"),
                      ("ch04-gui.md", "Graphical User Interface")]),

    # ── Chapter 2: Installation (single file) ──
    Section("ch02", "Installing Proxmox VE", 32, 48, "ch02-installation.md",
            chapter_num="2", section_prefix="2",
            see_also=[("ch01-introduction.md", "Introduction and overview"),
                      ("ch03-host-admin/_index.md", "Host System Administration")]),

    # ── Chapter 3: Host System Administration (subdirectory) ──
    Section("ch03-idx", "Host System Administration", 49, 49,
            "ch03-host-admin/_index.md",
            chapter_num="3", section_prefix="3",
            see_also=[("ch02-installation.md", "Installation"),
                      ("ch07-storage/_index.md", "Storage")]),
    Section("ch03-repos", "Package Repositories", 49, 55,
            "ch03-host-admin/package-repositories.md",
            chapter_num="3", section_prefix="3.1",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("ch03-host-admin/software-updates.md", "System Software Updates")]),
    Section("ch03-updates", "System Software Updates", 55, 56,
            "ch03-host-admin/software-updates.md",
            chapter_num="3", section_prefix="3.2",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("ch03-host-admin/package-repositories.md", "Package Repositories")]),
    Section("ch03-firmware", "Firmware Updates", 56, 59,
            "ch03-host-admin/firmware-updates.md",
            chapter_num="3", section_prefix="3.3",
            nav_parent="ch03-host-admin/_index.md"),
    Section("ch03-network", "Network Configuration", 59, 73,
            "ch03-host-admin/network-configuration.md",
            chapter_num="3", section_prefix="3.4",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("ch12-sdn/_index.md", "Software-Defined Network"),
                      ("ch13-firewall.md", "Firewall")]),
    Section("ch03-time", "Time Synchronization", 73, 75,
            "ch03-host-admin/time-synchronization.md",
            chapter_num="3", section_prefix="3.5",
            nav_parent="ch03-host-admin/_index.md"),
    Section("ch03-metrics", "External Metric Server", 75, 76,
            "ch03-host-admin/external-metrics.md",
            chapter_num="3", section_prefix="3.6",
            nav_parent="ch03-host-admin/_index.md"),
    Section("ch03-disk", "Disk Health Monitoring", 76, 77,
            "ch03-host-admin/disk-health.md",
            chapter_num="3", section_prefix="3.7",
            nav_parent="ch03-host-admin/_index.md"),
    Section("ch03-lvm", "Logical Volume Manager (LVM)", 77, 80,
            "ch03-host-admin/lvm.md",
            chapter_num="3", section_prefix="3.8",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("ch07-storage/lvm-backend.md", "LVM Storage Backend"),
                      ("ch07-storage/lvm-thin-backend.md", "LVM-thin Storage Backend")]),
    Section("ch03-zfs", "ZFS on Linux", 80, 94,
            "ch03-host-admin/zfs.md",
            chapter_num="3", section_prefix="3.9",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("ch07-storage/zfs-pool-backend.md", "ZFS Pool Storage Backend"),
                      ("ch07-storage/zfs-over-iscsi.md", "ZFS over iSCSI Backend")]),
    Section("ch03-btrfs", "BTRFS", 94, 97,
            "ch03-host-admin/btrfs.md",
            chapter_num="3", section_prefix="3.10",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("ch07-storage/btrfs-backend.md", "BTRFS Storage Backend")]),
    Section("ch03-node", "Proxmox Node Management", 97, 99,
            "ch03-host-admin/node-management.md",
            chapter_num="3", section_prefix="3.11",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("appendix-a-cli/pvenode.md", "pvenode CLI Reference")]),
    Section("ch03-certs", "Certificate Management", 99, 107,
            "ch03-host-admin/certificate-management.md",
            chapter_num="3", section_prefix="3.12",
            nav_parent="ch03-host-admin/_index.md",
            see_also=[("ch18-service-daemons.md", "Service Daemons (pveproxy)")]),
    Section("ch03-boot", "Host Bootloader", 107, 117,
            "ch03-host-admin/host-bootloader.md",
            chapter_num="3", section_prefix="3.13",
            nav_parent="ch03-host-admin/_index.md"),
    Section("ch03-ksm", "Kernel Samepage Merging (KSM)", 117, 118,
            "ch03-host-admin/ksm.md",
            chapter_num="3", section_prefix="3.14",
            nav_parent="ch03-host-admin/_index.md"),

    # ── Chapter 4: GUI (single file) ──
    Section("ch04", "Graphical User Interface", 119, 131, "ch04-gui.md",
            chapter_num="4", section_prefix="4",
            see_also=[("ch14-user-management/_index.md", "User Management"),
                      ("ch01-introduction.md", "Introduction")]),

    # ── Chapter 5: Cluster Manager (single file) ──
    Section("ch05", "Cluster Manager", 132, 157, "ch05-cluster-manager.md",
            chapter_num="5", section_prefix="5",
            see_also=[("ch06-pmxcfs.md", "Proxmox Cluster File System"),
                      ("ch15-high-availability/_index.md", "High Availability"),
                      ("appendix-a-cli/pvecm.md", "pvecm CLI Reference")]),

    # ── Chapter 6: pmxcfs (single file) ──
    Section("ch06", "Proxmox Cluster File System (pmxcfs)", 158, 162,
            "ch06-pmxcfs.md",
            chapter_num="6", section_prefix="6",
            see_also=[("ch05-cluster-manager.md", "Cluster Manager")]),

    # ── Chapter 7: Storage (subdirectory) ──
    Section("ch07-idx", "Proxmox VE Storage", 163, 163,
            "ch07-storage/_index.md",
            chapter_num="7", section_prefix="7",
            see_also=[("ch08-ceph/_index.md", "Ceph Cluster"),
                      ("appendix-a-cli/pvesm.md", "pvesm CLI Reference")]),
    Section("ch07-types", "Storage Types and Configuration", 163, 169,
            "ch07-storage/storage-types-and-config.md",
            chapter_num="7", section_prefix="7.1-7.4",
            nav_parent="ch07-storage/_index.md"),
    Section("ch07-dir", "Directory Backend", 169, 172,
            "ch07-storage/directory-backend.md",
            chapter_num="7", section_prefix="7.5",
            nav_parent="ch07-storage/_index.md"),
    Section("ch07-nfs", "NFS Backend", 172, 173,
            "ch07-storage/nfs-backend.md",
            chapter_num="7", section_prefix="7.6",
            nav_parent="ch07-storage/_index.md"),
    Section("ch07-cifs", "CIFS Backend", 173, 175,
            "ch07-storage/cifs-backend.md",
            chapter_num="7", section_prefix="7.7",
            nav_parent="ch07-storage/_index.md"),
    Section("ch07-pbs", "Proxmox Backup Server", 175, 178,
            "ch07-storage/proxmox-backup-server.md",
            chapter_num="7", section_prefix="7.8",
            nav_parent="ch07-storage/_index.md"),
    Section("ch07-zfspool", "Local ZFS Pool Backend", 178, 180,
            "ch07-storage/zfs-pool-backend.md",
            chapter_num="7", section_prefix="7.9",
            nav_parent="ch07-storage/_index.md",
            see_also=[("ch03-host-admin/zfs.md", "ZFS on Linux (Host)")]),
    Section("ch07-lvm", "LVM Backend", 180, 183,
            "ch07-storage/lvm-backend.md",
            chapter_num="7", section_prefix="7.10",
            nav_parent="ch07-storage/_index.md",
            see_also=[("ch03-host-admin/lvm.md", "LVM (Host)")]),
    Section("ch07-lvmthin", "LVM thin Backend", 183, 184,
            "ch07-storage/lvm-thin-backend.md",
            chapter_num="7", section_prefix="7.11",
            nav_parent="ch07-storage/_index.md"),
    Section("ch07-iscsi", "iSCSI Backends", 184, 186,
            "ch07-storage/iscsi-backends.md",
            chapter_num="7", section_prefix="7.12-7.13",
            nav_parent="ch07-storage/_index.md"),
    Section("ch07-rbd", "Ceph RADOS Block Devices (RBD)", 186, 189,
            "ch07-storage/ceph-rbd.md",
            chapter_num="7", section_prefix="7.14",
            nav_parent="ch07-storage/_index.md",
            see_also=[("ch08-ceph/_index.md", "Ceph Cluster")]),
    Section("ch07-cephfs", "Ceph Filesystem (CephFS)", 189, 191,
            "ch07-storage/cephfs.md",
            chapter_num="7", section_prefix="7.15",
            nav_parent="ch07-storage/_index.md",
            see_also=[("ch08-ceph/cephfs.md", "CephFS (Ceph chapter)")]),
    Section("ch07-btrfs", "BTRFS Backend", 191, 192,
            "ch07-storage/btrfs-backend.md",
            chapter_num="7", section_prefix="7.16",
            nav_parent="ch07-storage/_index.md",
            see_also=[("ch03-host-admin/btrfs.md", "BTRFS (Host)")]),
    Section("ch07-zfsiscsi", "ZFS over ISCSI Backend", 192, 194,
            "ch07-storage/zfs-over-iscsi.md",
            chapter_num="7", section_prefix="7.17",
            nav_parent="ch07-storage/_index.md"),

    # ── Chapter 8: Ceph (subdirectory) ──
    Section("ch08-idx", "Deploy Hyper-Converged Ceph Cluster", 195, 195,
            "ch08-ceph/_index.md",
            chapter_num="8", section_prefix="8",
            see_also=[("ch07-storage/_index.md", "Storage"),
                      ("appendix-a-cli/pveceph.md", "pveceph CLI Reference")]),
    Section("ch08-install", "Ceph Installation and Configuration", 195, 202,
            "ch08-ceph/installation-and-config.md",
            chapter_num="8", section_prefix="8.1-8.4",
            nav_parent="ch08-ceph/_index.md"),
    Section("ch08-mon", "Ceph Monitors and Managers", 202, 204,
            "ch08-ceph/monitors-and-managers.md",
            chapter_num="8", section_prefix="8.5-8.6",
            nav_parent="ch08-ceph/_index.md"),
    Section("ch08-osd", "Ceph OSDs", 204, 207,
            "ch08-ceph/osds.md",
            chapter_num="8", section_prefix="8.7",
            nav_parent="ch08-ceph/_index.md"),
    Section("ch08-pools", "Ceph Pools and Configuration", 207, 212,
            "ch08-ceph/pools-and-config.md",
            chapter_num="8", section_prefix="8.8-8.9",
            nav_parent="ch08-ceph/_index.md"),
    Section("ch08-crush", "CRUSH and Ceph Client", 212, 215,
            "ch08-ceph/crush-and-client.md",
            chapter_num="8", section_prefix="8.10-8.11",
            nav_parent="ch08-ceph/_index.md"),
    Section("ch08-cephfs", "CephFS", 215, 218,
            "ch08-ceph/cephfs.md",
            chapter_num="8", section_prefix="8.12",
            nav_parent="ch08-ceph/_index.md",
            see_also=[("ch07-storage/cephfs.md", "CephFS Storage Backend")]),
    Section("ch08-maint", "Ceph Maintenance and Troubleshooting", 218, 220,
            "ch08-ceph/maintenance-and-troubleshooting.md",
            chapter_num="8", section_prefix="8.13-8.14",
            nav_parent="ch08-ceph/_index.md"),

    # ── Chapter 9: Storage Replication (single file) ──
    Section("ch09", "Storage Replication", 221, 224,
            "ch09-storage-replication.md",
            chapter_num="9", section_prefix="9",
            see_also=[("ch07-storage/_index.md", "Storage"),
                      ("appendix-a-cli/pvesr.md", "pvesr CLI Reference")]),

    # ── Chapter 10: QEMU/KVM (subdirectory) ──
    Section("ch10-idx", "QEMU/KVM Virtual Machines", 225, 225,
            "ch10-qemu/_index.md",
            chapter_num="10", section_prefix="10",
            see_also=[("appendix-a-cli/qm.md", "qm CLI Reference"),
                      ("ch16-backup-restore.md", "Backup and Restore"),
                      ("ch11-containers/_index.md", "Containers")]),
    Section("ch10-general", "VM Settings: General, OS, System", 225, 229,
            "ch10-qemu/vm-settings-general.md",
            chapter_num="10", section_prefix="10.1-10.2.3",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-hw", "VM Settings: Hardware", 229, 248,
            "ch10-qemu/vm-settings-hardware.md",
            chapter_num="10", section_prefix="10.2.4-10.2.16",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-adv", "VM Settings: Advanced", 248, 253,
            "ch10-qemu/vm-settings-advanced.md",
            chapter_num="10", section_prefix="10.2.17-10.2.20",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-migrate", "VM Migration", 253, 256,
            "ch10-qemu/migration.md",
            chapter_num="10", section_prefix="10.3",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-clone", "Copies, Clones and Templates", 256, 258,
            "ch10-qemu/copies-clones-templates.md",
            chapter_num="10", section_prefix="10.4-10.6",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-import", "Importing Virtual Machines", 258, 262,
            "ch10-qemu/importing-vms.md",
            chapter_num="10", section_prefix="10.7",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-cloud", "Cloud-Init Support", 262, 269,
            "ch10-qemu/cloud-init.md",
            chapter_num="10", section_prefix="10.8",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-pci", "PCI(e) Passthrough", 269, 277,
            "ch10-qemu/pci-passthrough.md",
            chapter_num="10", section_prefix="10.9",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-hook", "Hookscripts, Hibernation, and Resource Mapping", 277, 280,
            "ch10-qemu/hookscripts-hibernation-mapping.md",
            chapter_num="10", section_prefix="10.10-10.12",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-qm", "Managing VMs with qm", 280, 282,
            "ch10-qemu/managing-with-qm.md",
            chapter_num="10", section_prefix="10.13",
            nav_parent="ch10-qemu/_index.md",
            see_also=[("appendix-a-cli/qm.md", "qm CLI Reference")]),
    Section("ch10-config", "VM Configuration Options", 282, 308,
            "ch10-qemu/configuration-options.md",
            chapter_num="10", section_prefix="10.14",
            nav_parent="ch10-qemu/_index.md"),
    Section("ch10-locks", "VM Locks", 308, 309,
            "ch10-qemu/locks.md",
            chapter_num="10", section_prefix="10.15",
            nav_parent="ch10-qemu/_index.md"),

    # ── Chapter 11: Containers (subdirectory) ──
    Section("ch11-idx", "Proxmox Container Toolkit", 309, 309,
            "ch11-containers/_index.md",
            chapter_num="11", section_prefix="11",
            see_also=[("appendix-a-cli/pct.md", "pct CLI Reference"),
                      ("ch16-backup-restore.md", "Backup and Restore"),
                      ("ch10-qemu/_index.md", "QEMU/KVM VMs")]),
    Section("ch11-tech", "Technology Overview and Distributions", 309, 315,
            "ch11-containers/technology-and-distributions.md",
            chapter_num="11", section_prefix="11.1-11.2",
            nav_parent="ch11-containers/_index.md"),
    Section("ch11-images", "Container Images", 315, 317,
            "ch11-containers/container-images.md",
            chapter_num="11", section_prefix="11.3",
            nav_parent="ch11-containers/_index.md"),
    Section("ch11-settings", "Container Settings", 317, 325,
            "ch11-containers/container-settings.md",
            chapter_num="11", section_prefix="11.4",
            nav_parent="ch11-containers/_index.md"),
    Section("ch11-security", "Security and OS Configuration", 325, 328,
            "ch11-containers/security-and-os-config.md",
            chapter_num="11", section_prefix="11.5-11.6",
            nav_parent="ch11-containers/_index.md"),
    Section("ch11-storage", "Container Storage", 328, 330,
            "ch11-containers/container-storage.md",
            chapter_num="11", section_prefix="11.7",
            nav_parent="ch11-containers/_index.md"),
    Section("ch11-backup", "Backup, Migration, and Configuration", 330, 339,
            "ch11-containers/backup-migration-config.md",
            chapter_num="11", section_prefix="11.8-11.11",
            nav_parent="ch11-containers/_index.md",
            see_also=[("ch16-backup-restore.md", "Backup and Restore")]),
    Section("ch11-locks", "Container Locks", 339, 340,
            "ch11-containers/locks.md",
            chapter_num="11", section_prefix="11.12",
            nav_parent="ch11-containers/_index.md"),

    # ── Chapter 12: SDN (subdirectory) ──
    Section("ch12-idx", "Software-Defined Network", 340, 340,
            "ch12-sdn/_index.md",
            chapter_num="12", section_prefix="12",
            see_also=[("ch03-host-admin/network-configuration.md", "Network Configuration"),
                      ("ch13-firewall.md", "Firewall")]),
    Section("ch12-overview", "SDN Overview and Installation", 340, 344,
            "ch12-sdn/overview-and-installation.md",
            chapter_num="12", section_prefix="12.1-12.5",
            nav_parent="ch12-sdn/_index.md"),
    Section("ch12-zones", "Zones", 344, 348,
            "ch12-sdn/zones.md",
            chapter_num="12", section_prefix="12.6",
            nav_parent="ch12-sdn/_index.md"),
    Section("ch12-vnets", "VNets, Subnets, and Controllers", 348, 352,
            "ch12-sdn/vnets-subnets-controllers.md",
            chapter_num="12", section_prefix="12.7-12.9",
            nav_parent="ch12-sdn/_index.md"),
    Section("ch12-fabrics", "Fabrics", 352, 358,
            "ch12-sdn/fabrics.md",
            chapter_num="12", section_prefix="12.10",
            nav_parent="ch12-sdn/_index.md"),
    Section("ch12-ipam", "IPAM, DNS, and DHCP", 358, 362,
            "ch12-sdn/ipam-dns-dhcp.md",
            chapter_num="12", section_prefix="12.11-12.13",
            nav_parent="ch12-sdn/_index.md"),
    Section("ch12-fw", "SDN Firewall Integration and Examples", 362, 367,
            "ch12-sdn/firewall-and-examples.md",
            chapter_num="12", section_prefix="12.14-12.16",
            nav_parent="ch12-sdn/_index.md",
            see_also=[("ch13-firewall.md", "Proxmox VE Firewall")]),

    # ── Chapter 13: Firewall (single file) ──
    Section("ch13", "Proxmox VE Firewall", 367, 385, "ch13-firewall.md",
            chapter_num="13", section_prefix="13",
            see_also=[("ch12-sdn/_index.md", "Software-Defined Network"),
                      ("ch14-user-management/_index.md", "User Management"),
                      ("appendix-f-firewall-macros.md", "Firewall Macro Definitions")]),

    # ── Chapter 14: User Management (subdirectory) ──
    Section("ch14-idx", "User Management", 386, 386,
            "ch14-user-management/_index.md",
            chapter_num="14", section_prefix="14",
            see_also=[("ch13-firewall.md", "Firewall"),
                      ("appendix-a-cli/pveum.md", "pveum CLI Reference")]),
    Section("ch14-users", "Users, Groups, Tokens, and Pools", 386, 390,
            "ch14-user-management/users-groups-tokens.md",
            chapter_num="14", section_prefix="14.1-14.4",
            nav_parent="ch14-user-management/_index.md"),
    Section("ch14-auth", "Authentication Realms", 390, 397,
            "ch14-user-management/authentication-realms.md",
            chapter_num="14", section_prefix="14.5",
            nav_parent="ch14-user-management/_index.md"),
    Section("ch14-2fa", "Two-Factor Authentication", 397, 403,
            "ch14-user-management/two-factor-auth.md",
            chapter_num="14", section_prefix="14.6",
            nav_parent="ch14-user-management/_index.md"),
    Section("ch14-perms", "Permission Management and Examples", 403, 408,
            "ch14-user-management/permissions-and-examples.md",
            chapter_num="14", section_prefix="14.7-14.9",
            nav_parent="ch14-user-management/_index.md"),

    # ── Chapter 15: High Availability (subdirectory) ──
    Section("ch15-idx", "High Availability", 409, 409,
            "ch15-high-availability/_index.md",
            chapter_num="15", section_prefix="15",
            see_also=[("ch05-cluster-manager.md", "Cluster Manager"),
                      ("appendix-a-cli/ha-manager.md", "ha-manager CLI Reference")]),
    Section("ch15-overview", "HA Overview and How It Works", 409, 418,
            "ch15-high-availability/overview-and-how-it-works.md",
            chapter_num="15", section_prefix="15.1-15.5",
            nav_parent="ch15-high-availability/_index.md"),
    Section("ch15-config", "HA Configuration", 418, 427,
            "ch15-high-availability/configuration.md",
            chapter_num="15", section_prefix="15.6",
            nav_parent="ch15-high-availability/_index.md"),
    Section("ch15-fence", "Fencing and Recovery", 427, 430,
            "ch15-high-availability/fencing-and-recovery.md",
            chapter_num="15", section_prefix="15.7-15.9",
            nav_parent="ch15-high-availability/_index.md"),
    Section("ch15-maint", "Maintenance and Scheduling", 430, 433,
            "ch15-high-availability/maintenance-and-scheduling.md",
            chapter_num="15", section_prefix="15.10-15.12",
            nav_parent="ch15-high-availability/_index.md"),

    # ── Chapter 16: Backup and Restore (single file) ──
    Section("ch16", "Backup and Restore", 434, 449, "ch16-backup-restore.md",
            chapter_num="16", section_prefix="16",
            see_also=[("ch10-qemu/_index.md", "QEMU/KVM VMs"),
                      ("ch11-containers/_index.md", "Containers"),
                      ("appendix-a-cli/vzdump.md", "vzdump CLI Reference")]),

    # ── Chapter 17: Notifications (single file) ──
    Section("ch17", "Notifications", 450, 460, "ch17-notifications.md",
            chapter_num="17", section_prefix="17"),

    # ── Chapter 18: Service Daemons (single file) ──
    Section("ch18", "Important Service Daemons", 461, 466,
            "ch18-service-daemons.md",
            chapter_num="18", section_prefix="18",
            see_also=[("ch03-host-admin/certificate-management.md", "Certificate Management"),
                      ("appendix-b-service-daemons.md", "Service Daemons (Appendix B)")]),

    # ── Chapter 19: CLI Tools (single file) ──
    Section("ch19", "Useful Command-line Tools", 467, 468,
            "ch19-cli-tools.md",
            chapter_num="19", section_prefix="19",
            see_also=[("appendix-a-cli/_index.md", "CLI Reference (Appendix A)")]),

    # ── Chapter 20: FAQ (single file) ──
    Section("ch20", "Frequently Asked Questions", 469, 471,
            "ch20-faq.md",
            chapter_num="20", section_prefix="20"),

    # ── Chapter 21: Bibliography (single file) ──
    Section("ch21", "Bibliography", 472, 473, "ch21-bibliography.md",
            chapter_num="21", section_prefix="21"),

    # ── Appendix A: CLI Reference (subdirectory) ──
    Section("appA-idx", "Command-line Interface", 474, 474,
            "appendix-a-cli/_index.md",
            chapter_num="A", section_prefix="A",
            see_also=[("ch19-cli-tools.md", "Useful Command-line Tools")]),
    Section("appA-general", "General and Format Options", 474, 475,
            "appendix-a-cli/general-and-format-options.md",
            chapter_num="A", section_prefix="A.1-A.2",
            nav_parent="appendix-a-cli/_index.md"),
    Section("appA-pvesm", "pvesm - Proxmox VE Storage Manager", 475, 489,
            "appendix-a-cli/pvesm.md",
            chapter_num="A", section_prefix="A.3",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch07-storage/_index.md", "Storage")]),
    Section("appA-pvesub", "pvesubscription", 489, 490,
            "appendix-a-cli/pvesubscription.md",
            chapter_num="A", section_prefix="A.4",
            nav_parent="appendix-a-cli/_index.md"),
    Section("appA-pveperf", "pveperf", 490, 491,
            "appendix-a-cli/pveperf.md",
            chapter_num="A", section_prefix="A.5",
            nav_parent="appendix-a-cli/_index.md"),
    Section("appA-pveceph", "pveceph - Manage Ceph Services", 491, 497,
            "appendix-a-cli/pveceph.md",
            chapter_num="A", section_prefix="A.6",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch08-ceph/_index.md", "Ceph Cluster")]),
    Section("appA-pvenode", "pvenode - Node Management", 497, 506,
            "appendix-a-cli/pvenode.md",
            chapter_num="A", section_prefix="A.7",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch03-host-admin/node-management.md", "Node Management")]),
    Section("appA-pvesh", "pvesh - API Shell", 506, 507,
            "appendix-a-cli/pvesh.md",
            chapter_num="A", section_prefix="A.8",
            nav_parent="appendix-a-cli/_index.md"),
    Section("appA-qm", "qm - QEMU/KVM VM Manager", 507, 553,
            "appendix-a-cli/qm.md",
            chapter_num="A", section_prefix="A.9",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch10-qemu/_index.md", "QEMU/KVM VMs")]),
    Section("appA-qmrestore", "qmrestore", 554, 555,
            "appendix-a-cli/qmrestore.md",
            chapter_num="A", section_prefix="A.10",
            nav_parent="appendix-a-cli/_index.md"),
    Section("appA-pct", "pct - Proxmox Container Toolkit", 555, 580,
            "appendix-a-cli/pct.md",
            chapter_num="A", section_prefix="A.11",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch11-containers/_index.md", "Containers")]),
    Section("appA-pveam", "pveam - Appliance Manager", 581, 582,
            "appendix-a-cli/pveam.md",
            chapter_num="A", section_prefix="A.12",
            nav_parent="appendix-a-cli/_index.md"),
    Section("appA-pvecm", "pvecm - Cluster Manager", 582, 586,
            "appendix-a-cli/pvecm.md",
            chapter_num="A", section_prefix="A.13",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch05-cluster-manager.md", "Cluster Manager")]),
    Section("appA-pvesr", "pvesr - Storage Replication", 586, 589,
            "appendix-a-cli/pvesr.md",
            chapter_num="A", section_prefix="A.14",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch09-storage-replication.md", "Storage Replication")]),
    Section("appA-pveum", "pveum - User Manager", 589, 605,
            "appendix-a-cli/pveum.md",
            chapter_num="A", section_prefix="A.15",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch14-user-management/_index.md", "User Management")]),
    Section("appA-vzdump", "vzdump - Backup Utility", 606, 609,
            "appendix-a-cli/vzdump.md",
            chapter_num="A", section_prefix="A.16",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch16-backup-restore.md", "Backup and Restore")]),
    Section("appA-ha", "ha-manager - HA Manager", 609, 615,
            "appendix-a-cli/ha-manager.md",
            chapter_num="A", section_prefix="A.17",
            nav_parent="appendix-a-cli/_index.md",
            see_also=[("ch15-high-availability/_index.md", "High Availability")]),

    # ── Appendix B-H ──
    Section("appB", "Service Daemons", 616, 622,
            "appendix-b-service-daemons.md",
            chapter_num="B", section_prefix="B",
            see_also=[("ch18-service-daemons.md", "Important Service Daemons")]),
    Section("appC", "Configuration Files", 623, 628,
            "appendix-c-config-files.md",
            chapter_num="C", section_prefix="C"),
    Section("appD", "Calendar Events", 629, 631,
            "appendix-d-calendar-events.md",
            chapter_num="D", section_prefix="D"),
    Section("appE", "QEMU vCPU List", 632, 633,
            "appendix-e-vcpu-list.md",
            chapter_num="E", section_prefix="E",
            see_also=[("ch10-qemu/vm-settings-hardware.md", "VM Hardware Settings (CPU)")]),
    Section("appF", "Firewall Macro Definitions", 634, 646,
            "appendix-f-firewall-macros.md",
            chapter_num="F", section_prefix="F",
            see_also=[("ch13-firewall.md", "Firewall")]),
    Section("appG", "Markdown Primer", 647, 650,
            "appendix-g-markdown-primer.md",
            chapter_num="G", section_prefix="G"),
    Section("appH", "GNU Free Documentation License", 651, 657,
            "appendix-h-license.md",
            chapter_num="H", section_prefix="H"),
]


def extract_text(pdf_start: int, pdf_end: int) -> str:
    """Extract text from PDF page range using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-f", str(pdf_start), "-l", str(pdf_end),
         str(PDF_PATH), "-"],
        capture_output=True, text=True
    )
    return result.stdout


def clean_text(text: str) -> str:
    """Clean raw pdftotext output."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        # Remove page header/footer lines
        if re.match(r"^Proxmox VE Administration Guide\s*$", line):
            continue
        if re.match(r"^\s*\d+\s*/\s*635\s*$", line):
            continue
        # Remove roman numeral page numbers (standalone)
        if re.match(r"^\s*(i{1,4}|vi{0,4}|xi{0,4}|xvi{0,4}|xxi{0,4})\s*$", line):
            continue
        # Remove TOC dot-leader lines
        if re.match(r"^\.(\s*\.)+\s*\d+\s*$", line):
            continue
        if ". . . . ." in line:
            continue
        cleaned.append(line)

    text = "\n".join(cleaned)
    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def text_to_markdown(text: str, section: Section) -> str:
    """Convert cleaned text to markdown format."""
    lines = text.split("\n")
    result = []
    in_code_block = False
    code_block_indent = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect "Chapter N" header line followed by title
        chapter_match = re.match(r"^Chapter\s+(\d+)\s*$", line)
        if chapter_match and i + 1 < len(lines):
            # Skip - we add our own heading
            i += 1
            # Skip the title line too (and any blank lines)
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i < len(lines):
                i += 1  # skip the title line
            continue

        # Detect "Appendix X" header
        appendix_match = re.match(r"^Appendix\s+([A-Z])\s*$", line)
        if appendix_match and i + 1 < len(lines):
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i < len(lines):
                i += 1
            continue

        # Convert section headings: "N.N Title" or "N.N.N Title"
        heading_match = re.match(
            r"^(\d+\.\d+(?:\.\d+)*)\s+(.+)$", line
        )
        if heading_match and not in_code_block:
            num = heading_match.group(1)
            title = heading_match.group(2)
            depth = num.count(".")
            level = min(depth + 1, 4)  # ## for N.N, ### for N.N.N, #### for N.N.N.N
            result.append("")
            result.append(f"{'#' * level} {num} {title}")
            result.append("")
            i += 1
            continue

        # Appendix section headings: "A.N Title" or "A.N.N Title"
        app_heading = re.match(
            r"^([A-Z]\.\d+(?:\.\d+)*)\s+(.+)$", line
        )
        if app_heading and not in_code_block:
            num = app_heading.group(1)
            title = app_heading.group(2)
            depth = num.count(".")
            level = min(depth + 1, 4)
            result.append("")
            result.append(f"{'#' * level} {num} {title}")
            result.append("")
            i += 1
            continue

        # Convert Note/Warning/Tip/Important/Caution blocks
        note_match = re.match(r"^\s*(Note|Warning|Tip|Important|Caution)\s*$", line)
        if note_match and not in_code_block:
            note_type = note_match.group(1)
            result.append("")
            result.append(f"> **{note_type}:**")
            i += 1
            # Collect subsequent lines until blank line
            while i < len(lines) and lines[i].strip() != "":
                result.append(f"> {lines[i].strip()}")
                i += 1
            result.append("")
            continue

        # Detect shell commands (lines starting with # or $ that look like commands)
        shell_match = re.match(r"^(#|root@|\$)\s+(.+)$", line)
        if shell_match and not in_code_block and not line.startswith("##"):
            # Check if this is actually a comment line
            if line.startswith("# ") and not re.match(r"^#\s+(apt|pvecm|qm|pct|pvesm|pvenode|pveum|pveceph|pvesh|pvesr|vzdump|ha-manager|systemctl|zpool|zfs|lvs|vgs|lvcreate|pvecm|cat|echo|ls|cp|mv|rm|mkdir|wget|curl|dpkg|ip|brctl|mount|umount|modprobe|sysctl|proxmox-boot-tool|update-grub|blkid|sgdisk|wipefs|dd|openssl|service|nano|vi|vim|sed|awk|grep|find|chmod|chown|lsblk|fdisk|pveperf|corosync|ssh|rsync|tar|gzip|btrfs|mkfs|tune2fs|reboot|shutdown|poweroff|hostname|hostnamectl|timedatectl|chronyc)", line):
                result.append(line)
                i += 1
                continue

            if not in_code_block:
                result.append("")
                result.append("```")
                in_code_block = True

            result.append(line)
            i += 1
            # Continue collecting command output / related lines
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip() == "":
                    # Check if next non-blank line is also a command
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == "":
                        j += 1
                    if j < len(lines) and re.match(r"^(#|root@|\$)\s+", lines[j]):
                        result.append("")
                        i += 1
                        continue
                    break
                # If it looks like continued output
                if not re.match(r"^(\d+\.\d+|\d+\.\d+\.\d+)\s+\S", next_line):
                    result.append(next_line)
                    i += 1
                else:
                    break

            if in_code_block:
                result.append("```")
                result.append("")
                in_code_block = False
            continue

        # Detect indented config/code blocks (4+ spaces or tab)
        if re.match(r"^(\s{4,}|\t)\S", line) and not in_code_block:
            # Look ahead to see if this is a multi-line code block
            block_lines = [line]
            j = i + 1
            while j < len(lines):
                if lines[j].strip() == "":
                    # Check if next non-blank is also indented
                    k = j + 1
                    while k < len(lines) and lines[k].strip() == "":
                        k += 1
                    if k < len(lines) and re.match(r"^(\s{4,}|\t)", lines[k]):
                        block_lines.append("")
                        j += 1
                        continue
                    break
                if re.match(r"^(\s{4,}|\t)", lines[j]):
                    block_lines.append(lines[j])
                    j += 1
                else:
                    break

            if len(block_lines) >= 2:
                result.append("")
                result.append("```")
                for bl in block_lines:
                    result.append(bl.rstrip())
                result.append("```")
                result.append("")
                i = j
                continue

        # Handle CLI reference patterns: "command subcommand <args> [OPTIONS]"
        cli_match = re.match(
            r"^(pvesm|pvesubscription|pveperf|pveceph|pvenode|pvesh|qm|qmrestore|pct|pveam|pvecm|pvesr|pveum|vzdump|ha-manager)\s+\S",
            line
        )
        if cli_match and not in_code_block:
            # This is a CLI command signature
            result.append("")
            result.append(f"```")
            result.append(line)
            i += 1
            result.append("```")
            result.append("")
            continue

        # Replace graphic references with text descriptions
        line = re.sub(
            r"[Ss]creenshot\s+(?:below\s+)?shows?",
            "the interface provides", line
        )
        line = re.sub(r"[Aa]s shown in the (?:image|figure|screenshot)",
                       "as described", line)
        line = re.sub(r"[Ss]ee (?:the )?(?:figure|screenshot|image) (?:below|above)",
                       "see the description", line)

        # Convert option/parameter lines: "--option <type> (default = val)"
        param_match = re.match(r"^--(\w[\w-]*)\s+(.+)$", line)
        if param_match and not in_code_block:
            result.append(f"- `--{param_match.group(1)}` {param_match.group(2)}")
            i += 1
            continue

        result.append(line)
        i += 1

    if in_code_block:
        result.append("```")

    return "\n".join(result)


def resolve_path(from_file: str, to_file: str) -> str:
    """Compute relative path from from_file to to_file."""
    from_dir = os.path.dirname(from_file)
    return os.path.relpath(to_file, from_dir)


def build_navigation(section: Section) -> str:
    """Build navigation breadcrumb line."""
    parts = []
    if section.nav_parent:
        parent_rel = resolve_path(section.output, section.nav_parent)
        parent_name = "Chapter Index"
        parts.append(f"[{parent_name}]({parent_rel})")

    root_rel = resolve_path(section.output, section.nav_root)
    parts.append(f"[Main Index]({root_rel})")

    return "*" + " | ".join(parts) + "*"


def build_see_also(section: Section) -> str:
    """Build ## See also section."""
    if not section.see_also:
        return ""
    lines = ["\n## See also\n"]
    for target, desc in section.see_also:
        rel = resolve_path(section.output, target)
        lines.append(f"- [{desc}]({rel})")
    return "\n".join(lines) + "\n"


def assemble_file(section: Section, content: str) -> str:
    """Assemble final markdown file with heading, nav, content, see_also."""
    parts = []
    parts.append(f"# {section.title}")
    parts.append("")
    parts.append(build_navigation(section))
    parts.append("")
    parts.append(content)
    see_also = build_see_also(section)
    if see_also:
        parts.append(see_also)
    return "\n".join(parts) + "\n"


def build_index_content(section: Section, children: list) -> str:
    """Build _index.md content for a directory section."""
    parts = []
    parts.append(f"# {section.title}")
    parts.append("")
    parts.append(build_navigation(section))
    parts.append("")

    # Add a navigation table
    parts.append("## Contents")
    parts.append("")
    parts.append("| Section | File |")
    parts.append("|---------|------|")
    for child in children:
        rel = resolve_path(section.output, child.output)
        parts.append(f"| {child.section_prefix} {child.title} | [{os.path.basename(child.output)}]({rel}) |")
    parts.append("")

    see_also = build_see_also(section)
    if see_also:
        parts.append(see_also)

    return "\n".join(parts) + "\n"


def write_file(path: str, content: str) -> int:
    """Write file and return size in bytes."""
    full_path = BASE_DIR / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")
    return len(content.encode("utf-8"))


def build_skill_md() -> str:
    """Build the SKILL.md hub file."""
    parts = []
    parts.append("""---
name: proxmox-admin-guide
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

| I need to... | Read |
|------|------|
| Install or upgrade Proxmox VE | `ch02-installation.md` |
| Configure package repositories | `ch03-host-admin/package-repositories.md` |
| Set up networking | `ch03-host-admin/network-configuration.md` |
| Manage ZFS on the host | `ch03-host-admin/zfs.md` |
| Manage LVM on the host | `ch03-host-admin/lvm.md` |
| Configure certificates / ACME | `ch03-host-admin/certificate-management.md` |
| Use the web GUI | `ch04-gui.md` |
| Create or manage a cluster | `ch05-cluster-manager.md` |
| Understand pmxcfs | `ch06-pmxcfs.md` |
| Add or configure storage | `ch07-storage/_index.md` |
| Deploy Ceph | `ch08-ceph/_index.md` |
| Set up storage replication | `ch09-storage-replication.md` |
| Create or manage VMs | `ch10-qemu/_index.md` |
| Create or manage containers | `ch11-containers/_index.md` |
| Configure SDN | `ch12-sdn/_index.md` |
| Configure the firewall | `ch13-firewall.md` |
| Manage users and permissions | `ch14-user-management/_index.md` |
| Set up High Availability | `ch15-high-availability/_index.md` |
| Back up or restore VMs/CTs | `ch16-backup-restore.md` |
| Configure notifications | `ch17-notifications.md` |
| Look up a CLI command | `appendix-a-cli/_index.md` |
| Check firewall macros | `appendix-f-firewall-macros.md` |
| Understand config file format | `appendix-c-config-files.md` |
| Schedule jobs (calendar events) | `appendix-d-calendar-events.md` |

---

## Chapters

| File | Description |
|------|-------------|
| [Introduction](ch01-introduction.md) | PVE overview, features, getting help |
| [Installation](ch02-installation.md) | System requirements, installer, Debian install |
| [Host System Admin](ch03-host-admin/_index.md) | Repos, network, ZFS, LVM, BTRFS, certs, bootloader |
| [Graphical User Interface](ch04-gui.md) | Web GUI features, login, panels, tags |
| [Cluster Manager](ch05-cluster-manager.md) | Create/join clusters, quorum, corosync, migration |
| [Cluster File System](ch06-pmxcfs.md) | pmxcfs, file layout, recovery |
| [Storage](ch07-storage/_index.md) | Storage types, backends (Dir, NFS, CIFS, PBS, ZFS, LVM, iSCSI, Ceph, BTRFS) |
| [Ceph Cluster](ch08-ceph/_index.md) | Ceph installation, monitors, OSDs, pools, CRUSH, CephFS |
| [Storage Replication](ch09-storage-replication.md) | ZFS-based replication, scheduling |
| [QEMU/KVM VMs](ch10-qemu/_index.md) | VM settings, hardware, migration, cloud-init, PCI passthrough |
| [Containers](ch11-containers/_index.md) | LXC containers, images, settings, security, storage |
| [Software-Defined Network](ch12-sdn/_index.md) | Zones, VNets, controllers, fabrics, IPAM, DHCP |
| [Firewall](ch13-firewall.md) | Rules, security groups, IP sets, nftables |
| [User Management](ch14-user-management/_index.md) | Users, groups, auth realms, 2FA, permissions |
| [High Availability](ch15-high-availability/_index.md) | HA resources, fencing, recovery, scheduling |
| [Backup and Restore](ch16-backup-restore.md) | Backup modes, jobs, retention, restore |
| [Notifications](ch17-notifications.md) | Targets, matchers, events, templates |
| [Service Daemons](ch18-service-daemons.md) | pvedaemon, pveproxy, pvestatd, spiceproxy |
| [CLI Tools](ch19-cli-tools.md) | pvesubscription, pveperf, pvesh |
| [FAQ](ch20-faq.md) | Frequently asked questions |
| [Bibliography](ch21-bibliography.md) | Books and references |

---

## CLI Reference (Appendix A)

| File | Tool | Description |
|------|------|-------------|
| [General](appendix-a-cli/general-and-format-options.md) | - | General CLI and format options |
| [pvesm](appendix-a-cli/pvesm.md) | `pvesm` | Storage Manager |
| [pvesubscription](appendix-a-cli/pvesubscription.md) | `pvesubscription` | Subscription Manager |
| [pveperf](appendix-a-cli/pveperf.md) | `pveperf` | Benchmark Script |
| [pveceph](appendix-a-cli/pveceph.md) | `pveceph` | Ceph Services Manager |
| [pvenode](appendix-a-cli/pvenode.md) | `pvenode` | Node Management |
| [pvesh](appendix-a-cli/pvesh.md) | `pvesh` | API Shell |
| [qm](appendix-a-cli/qm.md) | `qm` | QEMU/KVM VM Manager |
| [qmrestore](appendix-a-cli/qmrestore.md) | `qmrestore` | Restore VM Backups |
| [pct](appendix-a-cli/pct.md) | `pct` | Container Toolkit |
| [pveam](appendix-a-cli/pveam.md) | `pveam` | Appliance Manager |
| [pvecm](appendix-a-cli/pvecm.md) | `pvecm` | Cluster Manager |
| [pvesr](appendix-a-cli/pvesr.md) | `pvesr` | Storage Replication |
| [pveum](appendix-a-cli/pveum.md) | `pveum` | User Manager |
| [vzdump](appendix-a-cli/vzdump.md) | `vzdump` | Backup Utility |
| [ha-manager](appendix-a-cli/ha-manager.md) | `ha-manager` | HA Manager |

---

## Appendices

| File | Description |
|------|-------------|
| [Service Daemons](appendix-b-service-daemons.md) | Daemon CLI reference (pve-firewall, pvedaemon, etc.) |
| [Configuration Files](appendix-c-config-files.md) | datacenter.cfg format and options |
| [Calendar Events](appendix-d-calendar-events.md) | Schedule format specification |
| [QEMU vCPU List](appendix-e-vcpu-list.md) | Intel and AMD CPU types |
| [Firewall Macros](appendix-f-firewall-macros.md) | Predefined firewall macro definitions |
| [Markdown Primer](appendix-g-markdown-primer.md) | Markdown syntax for PVE notes |
| [License](appendix-h-license.md) | GNU Free Documentation License |
""")
    return "\n".join(parts) + "\n"


def main():
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)

    # Group sections by directory for _index.md generation
    dir_sections: dict[str, list[Section]] = {}
    index_sections: dict[str, Section] = {}
    for s in SECTIONS:
        dirname = os.path.dirname(s.output)
        if s.output.endswith("_index.md"):
            index_sections[dirname] = s
        elif dirname:
            dir_sections.setdefault(dirname, []).append(s)

    total_files = 0
    total_bytes = 0
    oversized = []

    print("Extracting Proxmox VE Admin Guide...")
    print(f"PDF: {PDF_PATH}")
    print(f"Sections defined: {len(SECTIONS)}")
    print()

    for section in SECTIONS:
        # _index.md files get special treatment
        if section.output.endswith("_index.md"):
            dirname = os.path.dirname(section.output)
            children = dir_sections.get(dirname, [])

            # Extract a small amount of intro text for the index
            raw = extract_text(section.pdf_start, section.pdf_start)
            cleaned = clean_text(raw)
            md = text_to_markdown(cleaned, section)

            # Build index with nav table
            content = build_index_content(section, children)
            # Append any extracted overview text (first ~30 lines)
            intro_lines = md.strip().split("\n")[:30]
            intro = "\n".join(intro_lines)
            if intro.strip():
                content = content.rstrip() + "\n\n## Overview\n\n" + intro + "\n"

            size = write_file(section.output, content)
        else:
            # Regular content section
            print(f"  Extracting: {section.output} (PDF pp {section.pdf_start}-{section.pdf_end})")
            raw = extract_text(section.pdf_start, section.pdf_end)
            cleaned = clean_text(raw)
            md = text_to_markdown(cleaned, section)
            content = assemble_file(section, md)
            size = write_file(section.output, content)

        total_files += 1
        total_bytes += size
        if size > 20480:
            oversized.append((section.output, size))
        print(f"  [{total_files:3d}] {section.output:60s} {size:>7,d} bytes")

    # Write SKILL.md
    skill_content = build_skill_md()
    skill_size = write_file("SKILL.md", skill_content)
    total_files += 1
    total_bytes += skill_size
    print(f"  [{total_files:3d}] {'SKILL.md':60s} {skill_size:>7,d} bytes")

    print()
    print(f"Total: {total_files} files, {total_bytes:,d} bytes ({total_bytes / 1024:.1f} KB)")

    if oversized:
        print()
        print("WARNING: Oversized files (>20KB):")
        for path, size in oversized:
            print(f"  {path}: {size:,d} bytes ({size / 1024:.1f} KB)")
    else:
        print("\nAll files within 20KB limit.")

    print("\nDone.")


if __name__ == "__main__":
    main()
