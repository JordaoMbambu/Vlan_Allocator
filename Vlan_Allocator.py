import ipaddress
from typing import List, Dict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print

class VLANAllocator:
    def __init__(self):
        self.network = None
        self.vlans = []
        self.subnets = []
        self.available_networks = []
        self.console = Console()

    def get_network_input(self) -> None:
        """Demande à l'utilisateur l'adresse réseau et le masque."""
        while True:
            try:
                input_str = input("Entrez l'adresse réseau principale avec le masque (ex: 192.168.1.0/24): ")
                if '/' not in input_str:
                    print("[bold red]Erreur: La notation CIDR (ex: /24) est requise.[/bold red]")
                    continue
                self.network = ipaddress.IPv4Network(input_str, strict=False)
                if self.network.prefixlen >= 30:
                    print(f"[bold red]Erreur: Le réseau {self.network} est trop petit pour être divisé en sous-réseaux avec des hôtes.[/bold red]")
                    print("[yellow]Veuillez choisir un réseau plus grand (ex: /29 ou moins).[/yellow]")
                    continue
                self.available_networks = [self.network]
                break
            except ValueError:
                print("[bold red]Erreur: Format invalide. Utilisez le format CIDR (ex: 192.168.1.0/24).[/bold red]")

    def get_vlan_info(self) -> None:
        """Demande les infos pour chaque VLAN de manière interactive."""
        self.console.print("\n[bold cyan]Configuration des VLANs (laissez le nom vide pour terminer)[/bold cyan]")
        vlan_counter = 1
        while True:
            print(f"\n--- VLAN/LAN #{vlan_counter} ---")
            vlan_name = input(f"Nom du LAN (ex: Serveurs, Marketing): ").strip()
            if not vlan_name:
                if not self.vlans:
                    confirm_exit = input("Aucun VLAN configuré. Voulez-vous vraiment continuer sans VLAN ? (o/N): ").lower()
                    if confirm_exit == 'o':
                        break
                    else:
                        continue
                break
            while True:
                try:
                    hosts_str = input(f"Nombre d'hôtes pour le LAN '{vlan_name}': ")
                    hosts = int(hosts_str)
                    if hosts <= 0:
                        print("[yellow]Erreur: Le nombre d'hôtes doit être supérieur ou égal à 1.[/yellow]")
                        continue
                    needed_size = hosts + 2
                    prefix = 32 - (needed_size - 1).bit_length()
                    self.vlans.append({'id': vlan_counter, 'name': vlan_name, 'hosts_needed': hosts, 'needed_prefix': prefix})
                    vlan_counter += 1
                    break
                except ValueError:
                    print("[bold red]Erreur: Entrez un nombre valide.[/bold red]")

    def check_capacity(self) -> bool:
        """Vérifie si tous les besoins en VLANs peuvent tenir dans le réseau principal."""
        if not self.vlans:
            return True
        total_required_addresses = sum(2**(32 - vlan['needed_prefix']) for vlan in self.vlans)
        available_addresses = self.network.num_addresses
        if total_required_addresses > available_addresses:
            self.console.print("\n" + "="*70, style="bold red")
            self.console.print("[bold red]ERREUR DE CAPACITÉ : L'espace total requis dépasse la taille du réseau principal.[/bold red]")
            self.console.print(f"  - Espace disponible dans {self.network}: [yellow]{available_addresses}[/yellow] adresses.")
            self.console.print(f"  - Espace total requis pour les VLANs: [yellow]{total_required_addresses}[/yellow] adresses.")
            self.console.print("[bold red]Veuillez choisir un réseau principal plus grand ou réduire le nombre d'hôtes.[/bold red]")
            self.console.print("="*70, style="bold red")
            return False
        return True

    def allocate_subnets(self) -> None:
        """Alloue les sous-réseaux de manière optimisée (VLSM)."""
        self.vlans.sort(key=lambda x: x['hosts_needed'], reverse=True)
        for vlan in self.vlans:
            prefix = vlan['needed_prefix']
            allocated = False
            self.available_networks.sort(key=lambda x: x.prefixlen, reverse=True)
            for i, net in enumerate(self.available_networks):
                if net.prefixlen <= prefix:
                    try:
                        subnet_generator = net.subnets(new_prefix=prefix)
                        allocated_subnet = next(subnet_generator)
                        remaining_subnets = list(subnet_generator)
                        self.subnets.append({'vlan_name': vlan['name'], 'hosts_needed': vlan['hosts_needed'], 'subnet': allocated_subnet})
                        self.available_networks.pop(i)
                        self.available_networks.extend(remaining_subnets)
                        allocated = True
                        break
                    except ValueError:
                        continue
            if not allocated:
                self.console.print(f"[bold red]Attention: Espace insuffisant pour allouer un sous-réseau pour {vlan['name']} ({vlan['hosts_needed']} hôtes).[/bold red]")

    def display_results(self) -> None:
        """Affiche les résultats dans des tableaux clairs avec 'rich'."""
        summary_panel = Panel(f"[bold]RÉSUMÉ DE L'ALLOCATION POUR LE RÉSEAU {self.network}[/bold]", expand=False, border_style="blue")
        self.console.print(summary_panel)
        if not self.subnets:
            self.console.print("\nAucun sous-réseau n'a été alloué.", style="yellow")
            return
        
        table = Table(title="Sous-réseaux Alloués (VLSM)", show_header=True, header_style="bold magenta")
        table.add_column("Nom du LAN", style="cyan", no_wrap=True)
        table.add_column("Hôtes Requis", justify="right")
        table.add_column("Hôtes Alloués", justify="right")
        table.add_column("Adresse Réseau", style="yellow", no_wrap=True)
        table.add_column("Masque (CIDR)", style="green", no_wrap=True)
        table.add_column("Plage Utilisable", style="green", no_wrap=True)
        table.add_column("Broadcast", style="yellow", no_wrap=True)

        self.subnets.sort(key=lambda x: x['subnet'].network_address)
        
        num_subnets = len(self.subnets)
        for i, sub in enumerate(self.subnets):
            s = sub['subnet']
            hosts_allocated = s.num_addresses - 2
            plage = f"{s.network_address + 1} - {s.broadcast_address - 1}"
            table.add_row(
                sub['vlan_name'], 
                str(sub['hosts_needed']), 
                str(hosts_allocated if hosts_allocated > 0 else 0), 
                str(s.network_address), 
                f"{s.netmask} (/{s.prefixlen})", 
                plage, 
                str(s.broadcast_address)
            )
            
            if i < num_subnets - 1:
                table.add_section()
                
        self.console.print(table)

    def run(self) -> None:
        """Exécute le processus complet."""
        main_title_panel = Panel("[bold]CALCULATEUR DE SOUS-RÉSEAUX VLSM[/bold]", expand=False, border_style="green")
        self.console.print(main_title_panel)
        
        self.get_network_input()
        self.get_vlan_info()
        
        if self.vlans and self.check_capacity():
            self.allocate_subnets()
            self.display_results()
        elif not self.vlans:
            self.console.print("\n[yellow]Aucun VLAN n'a été configuré. Fin du programme.[/yellow]")

        input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    allocator = VLANAllocator()
    allocator.run()