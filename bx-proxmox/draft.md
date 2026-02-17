Cluster Configuration (auto-detect)
Environment: Run `pveversion --verbose | head -1` to determine PVE version.
Nodes: Run `pvecm nodes` to get node count, names, and IDs. Run `pvecm status` for IPs and quorum details.
Quorum Status: Run `pvecm status` and check the "Quorate" field. Report immediately if "No". Calculate quorum threshold: floor(total_nodes/2) + 1.
API Access: Via pvesh (local) or Proxmox API (remote).
Storage: Run `pvesm status` for active storages and types per node. Run `cat /etc/pve/storage.cfg` for full configuration including node restrictions.

Safety Protocols
No destructive bulk operations: Commands affecting more than one node simultaneously (reboot, shutdown, bulk VM stop) must be explicitly confirmed by the user.
Quorum check: Before every node reboot or maintenance mode, run `pvecm status`. Calculate: if (current_nodes - 1) < floor(total_nodes/2) + 1, abort. On 2-node clusters, check for QDevice (`pvecm qdevice status`).
Backup first: Before changes to VM configurations or upgrades, verify that a current backup exists. Check with `vzdump --list` or `pvesh get /nodes/{node}/storage/{storage}/content --content backup`.
No force delete: Never use --purge or --force without double-validating the resource ID first.
HA status: Before changes to HA-managed resources, run `ha-manager status` and verify no migrations or fencing are in progress.

Management Commands (Cheat Sheet)
Cluster status: pvecm status / pvecm nodes
PVE version: pveversion --verbose
VM/LXC list (global): pvesh get /cluster/resources --type vm --output-format json
Node list (all names): pvesh get /nodes --output-format json
Node metrics: pvesh get /nodes/{node}/status (replace {node} with actual node name from `pvecm nodes`)
Storage overview: pvesm status
Storage config: cat /etc/pve/storage.cfg
Replication status: pvesh get /cluster/replication
HA status: ha-manager status
Service log: journalctl -u pve-cluster -f

Code & Response Style
Responses: Short, technically precise, focus on CLI commands (pvesh, pvecm, pvesm).
Troubleshooting: On errors, always query the affected node's logs first (`journalctl -u pvedaemon -n 50` and `/var/log/pveproxy/access.log`).
JSON preference: For data queries, prefer `--output-format json` to cleanly analyze the data structure.
Rollback plan: Every proposed change must include a rollback step.

Cluster-Size-Aware Workflows
Node count: Detect with `pvecm nodes | grep -c '^\s*[0-9]'`. Adapt all workflows to the actual cluster size.
Updates: Always sequential (rolling updates). One node at a time, verify services after each: `pvecm status && pveversion`.
Migration: Before migrating, check target node capacity: `pvesh get /nodes/{node}/status --output-format json` (inspect cpu/memory utilization).
Network: Always test interface changes first with `ifreload -a --test`, never kill the interface directly.
ID management: Check next free VM ID with `pvesh get /cluster/nextid`. Check existing IDs with `pvesh get /cluster/resources --type vm --output-format json`.

Network Diagnostics (Cluster-Wide)
Interface status (API): pvesh get /nodes/{node}/network (shows bridges, bonds, and IPs)
Bonding check: List bonds with `ls /proc/net/bonding/ 2>/dev/null`, then inspect each with `cat /proc/net/bonding/{name}`
OVS status (if used): ovs-vsctl show
MTU & link speed: ip link show (important for 10G/25G/40G backplane checks)
VLAN bridge check: bridge vlan show
Test network configuration: ifreload -a --test (before activation!)
Corosync links: pvecm status (check all link states for each node)
