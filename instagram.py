from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from bs4 import BeautifulSoup
import io

instagram_bp = Blueprint('instagram', __name__)

def parse_html_content(html_content):
    """
    Extrai usernames do Instagram de conteúdo HTML.
    """
    usernames = set()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Procura por links do Instagram
    for a_tag in soup.find_all('a', target='_blank'):
        href = a_tag.get('href')
        if href and 'instagram.com' in href:
            # Extrai o username da URL
            username = href.split('/')[-1]
            if username:  # Verifica se não está vazio
                usernames.add(username)
    
    return usernames

@instagram_bp.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_followers():
    """
    Analisa arquivos HTML de seguidores e seguindo para encontrar quem não segue de volta.
    """
    try:
        # Verifica se os arquivos foram enviados
        if 'following_file' not in request.files or 'followers_file' not in request.files:
            return jsonify({
                'error': 'Ambos os arquivos (following_file e followers_file) são obrigatórios'
            }), 400
        
        following_file = request.files['following_file']
        followers_file = request.files['followers_file']
        
        # Verifica se os arquivos não estão vazios
        if following_file.filename == '' or followers_file.filename == '':
            return jsonify({
                'error': 'Nenhum arquivo foi selecionado'
            }), 400
        
        # Lê o conteúdo dos arquivos
        following_content = following_file.read().decode('utf-8')
        followers_content = followers_file.read().decode('utf-8')
        
        # Extrai os usernames de cada arquivo
        following_users = parse_html_content(following_content)
        followers_users = parse_html_content(followers_content)
        
        # Encontra quem não segue de volta
        not_following_back = following_users - followers_users
        
        # Prepara a resposta
        result = {
            'total_following': len(following_users),
            'total_followers': len(followers_users),
            'not_following_back_count': len(not_following_back),
            'not_following_back': sorted(list(not_following_back))
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar os arquivos: {str(e)}'
        }), 500

@instagram_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """
    Endpoint simples para verificar se a API está funcionando.
    """
    return jsonify({
        'status': 'ok',
        'message': 'Instagram Follower Checker API está funcionando!'
    })

