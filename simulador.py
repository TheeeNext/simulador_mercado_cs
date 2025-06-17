import hashlib
import time
import os
import random

# DADOS DE MERCADO (SIMULAÇÃO)
BASE_PRICES = {
    "AK-47 | Case Hardened": 400, "M4A4 | Howl": 5000, "AWP | Dragon Lore": 10000,
    "AWP | Asiimov": 80, "Karambit | Doppler": 1500, "USP-S | Kill Confirmed": 60,
    "Glock-18 | Fade": 1200, "M4A1-S | Printstream": 300, "AK-47 | Redline": 20
}
STICKER_VALUES = {
    "iBUYPOWER (Holo) | Katowice 2014": 40000, "Titan (Holo) | Katowice 2014": 60000,
    "Crown (Foil)": 500, "Virtus.Pro | Katowice 2014": 1500, "Sticker de Galinha": 0.01,
    "Sticker PGL (Holo)": 15
}
CHARM_VALUES = {
    "Charm Lil SAS": 5, "Charm Big Kev": 20, "Charm Die-Cast": 150
}
PATTERN_BONUSES = {
    ("AK-47 | Case Hardened", 661): 100000, # Blue Gem
    ("AK-47 | Case Hardened", 321): 5000,    # Gold Gem
    ("Karambit | Doppler", 563): 20000      # Ruby
}

# FUNÇÕES E CLASSES AUXILIARES
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class ProvenanceNode:
    def __init__(self, item_type, item_name):
        self.type = item_type
        self.name = item_name
        self.children = []
    def add_child(self, child_node):
        self.children.append(child_node)

class TradeBlock:
    def __init__(self, new_owner, previous_hash):
        self.timestamp = time.time()
        self.owner = new_owner
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    def calculate_hash(self):
        return hashlib.sha256(f"{self.timestamp}{self.owner}{self.previous_hash}".encode('utf-8')).hexdigest()
    def __repr__(self):
        return f"[{time.strftime('%d/%m/%Y', time.localtime(self.timestamp))}] Dono: {self.owner} | Hash: {self.hash[:10]}..."

class DigitalAssetSkin:
    def __init__(self, skin_name, case_name, first_owner, float_value, paint_seed, stickers=None, charms=None):
        self.name = skin_name
        self.float_value = float_value
        self.paint_seed = paint_seed
        self.stickers = stickers if stickers else []
        self.charms = charms if charms else []
        
        self.provenance_tree = ProvenanceNode("Skin", self.name)
        self.provenance_tree.add_child(ProvenanceNode("Caixa", case_name))
        
        for sticker in self.stickers:
            self.provenance_tree.add_child(ProvenanceNode("Adesivo", sticker))
        for charm in self.charms:
            self.provenance_tree.add_child(ProvenanceNode("Charm", charm))

        self.trade_history = [TradeBlock(first_owner, "0" * 64)]

    def trade(self, new_owner_name):
        self.trade_history.append(TradeBlock(new_owner_name, self.trade_history[-1].hash))

    def apply_sticker(self, sticker_name):
        self.stickers.append(sticker_name)
        self.provenance_tree.add_child(ProvenanceNode("Adesivo", sticker_name))

    def attach_charm(self, charm_name):
        self.charms.append(charm_name)
        self.provenance_tree.add_child(ProvenanceNode("Charm", charm_name))

    def estimate_price(self):
        base_price = BASE_PRICES.get(self.name, 10)
        float_multiplier = (1.5 - self.float_value) ** 2
        price_with_float = base_price * float_multiplier
        pattern_bonus = PATTERN_BONUSES.get((self.name, self.paint_seed), 0)
        sticker_bonus = sum(STICKER_VALUES.get(s, 0) for s in self.stickers)
        charm_bonus = sum(CHARM_VALUES.get(c, 0) for c in self.charms)
        return price_with_float + pattern_bonus + sticker_bonus + charm_bonus

    def display_full_details(self):
        title = f"🧐 INSPECIONANDO: {self.name}"
        print("\n"+"="*len(title))
        print(title)
        print("="*len(title))
        print(f"💰 Preço Estimado: US$ {self.estimate_price():,.2f}")
        print(f"Float: {self.float_value:.6f} | Pattern: {self.paint_seed}")
        
        if self.stickers:
            print("Adesivos Aplicados:")
            for s in self.stickers:
                print(f"  - {s} (+US$ {STICKER_VALUES.get(s, 0):,.2f})")
        
        if self.charms:
            print("Charms (Pingentes) Anexados:")
            for c in self.charms:
                print(f"  - {c} (+US$ {CHARM_VALUES.get(c, 0):,.2f})")

        self.display_provenance_tree()
        self.display_trade_history()
        
    def display_provenance_tree(self):
        title="🌳 Árvore de Proveniência e Composição"
        print("\n"+"="*len(title))
        print(title)
        print("="*len(title))
        def print_branch(node, prefix="", is_last=True):
            display_type = node.type
            marker = "❔"
            if node.type == "Skin":
                marker = "🔫"
            elif node.type == "Caixa":
                marker = "📦"
            elif node.type == "Adesivo":
                marker = "✨"
            elif node.type == "Charm":
                marker = "🔑"
                display_type = "Charm (Pingente)"
            
            print(prefix+("└── " if is_last else "├── ")+f"{marker} [{display_type}] {node.name}")
            for i,child in enumerate(node.children):
                print_branch(child,prefix+("    " if is_last else "│   "),i==len(node.children)-1)
        print_branch(self.provenance_tree)
        
    def display_trade_history(self):
        title="⛓️ Histórico de Propriedade"
        print("\n" + "="*len(title))
        print(title)
        print("="*len(title))
        for i,block in enumerate(self.trade_history):
            if i==0:
                print(f"Bloco {i} (Gênesis): {block}")
            else:
                print(f"     ↓")
                print(f"Bloco {i}: {block}")
                print(f"     (Hash Anterior: {block.previous_hash[:10]}...)")

def create_skin_database():
    db = {}
    skin_data_list = [{"id": 1, "nome": "AK-47 | Case Hardened", "caixa": "Caixa de Armas do CS:GO", "dono": "Pro_Player1", "float": 0.187, "seed": 661, "stickers": ["iBUYPOWER (Holo) | Katowice 2014"]}, {"id": 2, "nome": "AK-47 | Case Hardened", "caixa": "Caixa de Armas do CS:GO", "dono": "Trader_Rico", "float": 0.654, "seed": 321}, {"id": 3, "nome": "M4A4 | Howl", "caixa": "Caixa do Caçador", "dono": "Investidor_Antigo", "float": 0.012, "seed": 112, "charms": ["Charm Die-Cast"]}, {"id": 4, "nome": "AWP | Dragon Lore", "caixa": "Pacote Cobblestone", "dono": "CS_Legend", "float": 0.055, "seed": 488, "stickers": ["Titan (Holo) | Katowice 2014"]*4}, {"id": 5, "nome": "AWP | Asiimov", "caixa": "Caixa da Operação Fênix", "dono": "Streamer_Famoso", "float": 0.213, "seed": 989, "charms": ["Charm Big Kev"]}, {"id": 6, "nome": "AWP | Asiimov", "caixa": "Caixa da Operação Fênix", "dono": "Jogador_Casual", "float": 0.998, "seed": 101, "stickers": ["Sticker de Galinha"]}, {"id": 7, "nome": "Karambit | Doppler", "caixa": "Caixa Chroma 2", "dono": "Sortudo", "float": 0.007, "seed": 412}, {"id": 8, "nome": "Karambit | Doppler", "caixa": "Caixa Chroma", "dono": "Entusiasta", "float": 0.021, "seed": 563, "stickers": ["Crown (Foil)"]}, {"id": 9, "nome": "USP-S | Kill Confirmed", "caixa": "Caixa do Desbravamento", "dono": "Jogador1", "float": 0.111, "seed": 734}, {"id": 10, "nome": "Glock-18 | Fade", "caixa": "Pacote de Mapas Assault", "dono": "Jogador2", "float": 0.009, "seed": 22}, {"id": 11, "nome": "M4A1-S | Printstream", "caixa": "Caixa da Operação Broken Fang", "dono": "Designer", "float": 0.0001, "seed": 777}, {"id": 12, "nome": "AK-47 | Redline", "caixa": "Caixa da Operação Fênix", "dono": "Veterano", "float": 0.101, "seed": 123, "stickers": ["Virtus.Pro | Katowice 2014"]*2}]
    for d in skin_data_list:
        db[d["id"]] = DigitalAssetSkin(d["nome"], d["caixa"], d["dono"], d["float"], d["seed"], d.get("stickers"), d.get("charms"))
    return db

# FUNÇÕES DE MENU 

def display_skin_list(skin_dict):
    if not skin_dict:
        print("Nenhuma skin encontrada.")
    else:
        print(f"{'ID':<4} | {'Float':<10} | {'Pattern':<8} | {'Dono Atual':<18} | {'Skin'}")
        print("-" * 75)
        for id_skin, skin in skin_dict.items():
            current_owner = skin.trade_history[-1].owner
            print(f"{id_skin:<4} | {skin.float_value:<10.6f} | {skin.paint_seed:<8} | {current_owner:<18} | {skin.name}")
        print("\nUse o ID acima nas outras opções do menu para inspecionar ou negociar.")
    input("\n--- Pressione Enter para voltar ao menu ---")

def list_all_skins(database):
    clear_console()
    print("--- 📜 Todas as Skins no Database ---")
    display_skin_list(database)

def search_by_name(database):
    clear_console()
    print("--- 🔎 Pesquisar Skin por Nome ---")
    query = input("Digite o nome (ou parte do nome) da skin: ").lower()
    results = {id: skin for id, skin in database.items() if query in skin.name.lower()}
    print("\n--- Resultados da Pesquisa ---")
    display_skin_list(results)

def inspect_player_inventory(database):
    clear_console()
    print("--- 🧐 Inspecionar Inventário de Jogador ---")
    owners = sorted(list(set(s.trade_history[-1].owner for s in database.values())))
    print("Jogadores no database:", ", ".join(owners))
    target_player = input("\nDigite o nome do jogador para ver o inventário: ")
    if target_player not in owners:
        print("\n[ERRO] Jogador não encontrado.")
    else:
        portfolio_skins = [s for s in database.values() if s.trade_history[-1].owner == target_player]
        total_value = sum(s.estimate_price() for s in portfolio_skins)
        clear_console()
        print(f"--- Inventário de {target_player} ---")
        print("-" * 50)
        for skin in sorted(portfolio_skins, key=lambda s: s.estimate_price(), reverse=True):
            print(f"${skin.estimate_price():<12,.2f} | {skin.name}")
        print("-" * 50)
        print(f"VALOR TOTAL ESTIMADO: US$ {total_value:,.2f}")
    input("\n--- Pressione Enter para continuar ---")

def inspect_skin_by_id(database):
    try:
        skin_id = int(input("  Digite o ID da skin para inspecionar: "))
        if skin_id in database:
            clear_console()
            database[skin_id].display_full_details()
        else:
            print("\n[ERRO] ID não encontrado.")
    except ValueError:
        print("\n[ERRO] ID inválido.")
    input("\n--- Pressione Enter para continuar ---")

def apply_sticker_to_skin(database):
    try:
        skin_id = int(input("  Digite o ID da skin para aplicar o adesivo: "))
        if skin_id in database:
            sticker_name = input("  Digite o nome do adesivo: ")
            if sticker_name:
                database[skin_id].apply_sticker(sticker_name)
                print(f"\n[SUCESSO] Adesivo '{sticker_name}' aplicado na skin {skin_id}!")
            else:
                print("\n[ERRO] Nome do adesivo não pode ser vazio.")
        else:
            print("\n[ERRO] ID não encontrado.")
    except ValueError:
        print("\n[ERRO] ID inválido.")
    input("\n--- Pressione Enter para continuar ---")

def attach_charm_to_skin(database):
    try:
        skin_id = int(input("  Digite o ID da skin para anexar o charm (pingente): "))
        if skin_id in database:
            charm_name = input("  Digite o nome do charm (pingente): ")
            if charm_name:
                database[skin_id].attach_charm(charm_name)
                print(f"\n[SUCESSO] Charm (pingente) '{charm_name}' anexado na skin {skin_id}!")
            else:
                print("\n[ERRO] Nome do charm não pode ser vazio.")
        else:
            print("\n[ERRO] ID não encontrado.")
    except ValueError:
        print("\n[ERRO] ID inválido.")
    input("\n--- Pressione Enter para continuar ---")

def trade_skin_by_id(database):
    try:
        skin_id = int(input("  Digite o ID da skin para negociar: "))
        if skin_id in database:
            skin_to_trade = database[skin_id]
            current_owner = skin_to_trade.trade_history[-1].owner
            new_owner = input(f"  Para quem enviar a '{skin_to_trade.name}'? (Dono Atual: {current_owner}): ")
            if new_owner and new_owner.lower() != current_owner.lower():
                skin_to_trade.trade(new_owner)
                print(f"\n[SUCESSO] Negociado!")
            else:
                print("\n[ERRO] Nome inválido ou igual ao do dono atual.")
        else:
            print("\n[ERRO] ID não encontrado.")
    except ValueError:
        print("\n[ERRO] ID inválido.")
    input("\n--- Pressione Enter para continuar ---")

def main_menu():
    skin_database = create_skin_database()
    while True:
        clear_console()
        print("====== 🔫 SIMULADOR DE MERCADO DE SKINS ======")
        print("Use a lista ou a pesquisa para encontrar IDs e depois modifique ou negocie.")
        
        print("\n--- MENU PRINCIPAL ---")
        print("1. 📜 Listar Todas as Skins")
        print("2. 🔎 Pesquisar Skin por Nome")
        print("3. 🧐 Inspecionar Inventário de Jogador")
        print("4. ✨ Inspecionar Skin Específica (por ID)")
        print("5. 🤝 Negociar Skin (por ID)")
        print("\n--- Ações de Modificação ---")
        print("6. 🎨 Aplicar Adesivo em uma Skin")
        print("7. 🔑 Anexar Charm (Pingente)")
        print("8. 🚪 Sair")
        choice = input("\n>> Escolha uma opção: ")

        if choice == '1':
            list_all_skins(skin_database)
        elif choice == '2':
            search_by_name(skin_database)
        elif choice == '3':
            inspect_player_inventory(skin_database)
        elif choice == '4':
            inspect_skin_by_id(skin_database)
        elif choice == '5':
            trade_skin_by_id(skin_database)
        elif choice == '6':
            apply_sticker_to_skin(skin_database)
        elif choice == '7':
            attach_charm_to_skin(skin_database)
        elif choice == '8':
            print("\nSaindo...")
            break
        else:
            print("\n[ERRO] Opção inválida.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()