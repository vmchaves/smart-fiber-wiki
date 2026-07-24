import os
import sys
import re
from argparse import Namespace

# Garante que possamos importar md2conf a partir do mesmo diretório
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
from md2conf import MD2Confluence

def run_md2conf(file_path, space_key, parent_id, username, password, org_name):
    args = Namespace(
        markdownFile=file_path,
        spacekey=space_key,
        username=username,
        password=password,
        orgname=org_name,
        ancestor=parent_id,
        attachments=None,
        contents=False,
        nossl=False,
        delete=False
    )
    print(f"\n[SYNC] Sincronizando: {file_path}")
    print(f"       Espaço: {space_key} | Ancestral ID: {parent_id}")
    try:
        client = MD2Confluence(args)
        print(f"       Sucesso! ID da página: {client.page_id}")
        return client.page_id
    except Exception as e:
        print(f"       Erro ao sincronizar '{file_path}': {e}")
        return None

def sync_directory(dir_path, parent_id, space_key, username, password, org_name):
    dir_name = os.path.basename(os.path.abspath(dir_path))
    print(f"\n[DIR] Processando diretório: {dir_path}")
    
    files = os.listdir(dir_path)
    main_file = None
    
    # 1. Procurar por index.md (case-insensitive)
    for f in files:
        if f.lower() == 'index.md':
            main_file = os.path.join(dir_path, f)
            break
            
    # 2. Procurar por <dirname>.md (case-insensitive)
    if not main_file:
        for f in files:
            if f.lower() == f"{dir_name.lower()}.md":
                main_file = os.path.join(dir_path, f)
                break
                
    # 3. Se não houver arquivo principal, cria um placeholder
    temp_file = None
    if not main_file:
        title = dir_name.replace('-', ' ').replace('_', ' ').title()
        print(f"      Nenhum index.md ou {dir_name}.md encontrado. Criando placeholder para '{title}'...")
        temp_file = os.path.join(dir_path, f".tmp_placeholder_{dir_name}.md")
        with open(temp_file, 'w', encoding='utf-8') as pf:
            pf.write(f"# {title}\n\n_Pasta de documentação para {title}._\n")
        main_file = temp_file

    # Publicar a página correspondente ao diretório
    dir_page_id = run_md2conf(main_file, space_key, parent_id, username, password, org_name)
    
    # Apagar o placeholder se foi criado
    if temp_file and os.path.exists(temp_file):
        try:
            os.remove(temp_file)
        except Exception as e:
            print(f"      Aviso: Não foi possível apagar o placeholder {temp_file}: {e}")
            
    if not dir_page_id:
        print(f"      Aviso: Não foi possível obter o ID da página para o diretório '{dir_path}'. Abortando subpáginas.")
        return

    # 4. Publicar os outros arquivos Markdown deste nível
    for f in files:
        full_path = os.path.join(dir_path, f)
        if os.path.isfile(full_path) and f.endswith('.md'):
            # Ignorar o arquivo principal que já foi publicado
            if main_file and os.path.abspath(full_path) == os.path.abspath(main_file):
                continue
            # Ignorar arquivos temporários/ocultos
            if f.startswith('.'):
                continue
            run_md2conf(full_path, space_key, dir_page_id, username, password, org_name)
            
    # 5. Processar subpastas recursivamente
    for f in files:
        full_path = os.path.join(dir_path, f)
        if os.path.isdir(full_path):
            # Ignorar pastas ocultas ou especiais (ex: .git, __pycache__)
            if f.startswith('.') or f.startswith('__') or f.startswith('README.md') or f.startswith('log.md') or f.startswith('OKF_STYLE_GUIDE'):
                continue
            sync_directory(full_path, dir_page_id, space_key, username, password, org_name)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sincroniza recursivamente uma pasta de Markdown com o Confluence.")
    parser.add_argument("wikiDir", help="Diretório da Wiki local (ex: ./wiki)")
    parser.add_argument("spaceKey", help="Space Key do Confluence")
    parser.add_argument("-a", "--ancestor", required=True, help="ID da página Confluence ancestral raiz")
    
    # Configurações de ambiente opcionais por flags (priorizam as variáveis de ambiente)
    parser.add_argument("-u", "--username", default=os.getenv('CONFLUENCE_USERNAME'), help="E-mail de login")
    parser.add_argument("-p", "--password", default=os.getenv('CONFLUENCE_PASSWORD'), help="API Token")
    parser.add_argument("-o", "--orgname", default=os.getenv('CONFLUENCE_ORGNAME'), help="Subdomínio do confluence (ex: padtec-tec)")
    
    args = parser.parse_args()
    
    if not all([args.username, args.password, args.orgname]):
        print("Erro: As credenciais do Confluence (username, password, orgname) precisam ser definidas")
        print("via variáveis de ambiente (CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD, CONFLUENCE_ORGNAME)")
        print("ou passadas pelas flags -u, -p, -o.")
        sys.exit(1)
        
    if not os.path.exists(args.wikiDir):
        print(f"Erro: O diretório '{args.wikiDir}' não existe.")
        sys.exit(1)
        
    print("==================================================")
    print("Iniciando Sincronização de Wiki para o Confluence")
    print(f"Diretório Local: {args.wikiDir}")
    print(f"Space Key: {args.spaceKey}")
    print(f"ID Ancestral Raiz: {args.ancestor}")
    print("==================================================")
    
    sync_directory(args.wikiDir, args.ancestor, args.spaceKey, args.username, args.password, args.orgname)
    print("\nSincronização concluída com sucesso!")

if __name__ == "__main__":
    main()
