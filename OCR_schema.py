import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
import argparse

class OCRProcessor:
    def __init__(self):
        self.output_dir = "Saida_Processada"
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """Cria o diretório de saída se não existir"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def parse_ocr_line(self, line: str) -> Dict[str, Any]:
        """Extrai informações de uma linha do OCR"""
        # Padrão para extrair OCR='texto', score=valor, bbox=[coordenadas]
        pattern = r"OCR='([^']*)',\s*score=([0-9.]+),\s*bbox=\[([0-9,\s]+)\]"
        match = re.match(pattern, line.strip())
        
        if match:
            text = match.group(1)
            score = float(match.group(2))
            bbox_coords = [int(x.strip()) for x in match.group(3).split(',')]
            return {
                'text': text,
                'score': score,
                'bbox': bbox_coords,
                'y_position': bbox_coords[1]  # Posição Y para ordenação
            }
        return None
    
    def extract_cnpj(self, ocr_data: List[Dict]) -> Optional[str]:
        """Extrai CNPJ do texto OCR"""
        cnpj_patterns = [
            r'(?:CNPJ?[:\s]*)?(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})',
            r'(?:CHP\.J[:\s]*)?(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})'
        ]
        
        for item in ocr_data:
            text = item['text']
            for pattern in cnpj_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    cnpj = re.sub(r'[^\d]', '', match.group(1))
                    if len(cnpj) == 14:
                        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"
        return None
    
    def extract_date(self, ocr_data: List[Dict]) -> Optional[str]:
        """Extrai data de emissão"""
        date_patterns = [
            r'(\d{2}[-/]\d{2}[-/]\d{4})',
            r'(\d{2}[-/]\d{2}[-/]\d{2})',
            r'(\d{4}[-/]\d{2}[-/]\d{2})'
        ]
        
        for item in ocr_data:
            text = item['text']
            for pattern in date_patterns:
                match = re.search(pattern, text)
                if match:
                    date_str = match.group(1)
                    # Tentar converter para timestamp
                    try:
                        if len(date_str.split('-')[0]) == 2 or len(date_str.split('/')[0]) == 2:
                            # Formato DD/MM/YYYY ou DD-MM-YYYY
                            dt = datetime.strptime(date_str.replace('-', '/'), '%d/%m/%Y')
                        else:
                            # Formato YYYY/MM/DD ou YYYY-MM-DD
                            dt = datetime.strptime(date_str.replace('-', '/'), '%Y/%m/%d')
                        return dt.isoformat()
                    except ValueError:
                        continue
        return None
    
    def extract_establishment_name(self, ocr_data: List[Dict]) -> Optional[str]:
        """Extrai nome do estabelecimento"""
        # Procura por textos que parecem ser nomes de estabelecimentos
        for item in ocr_data:
            text = item['text'].strip()
            # Verifica se contém palavras indicativas de estabelecimento
            if any(keyword in text.lower() for keyword in ['ltda', 'comercio', 'mercado', 'supermercado', 'loja']):
                return text
            # Ou se é um texto longo sem números no início
            if len(text) > 10 and not text[0].isdigit() and 'score' not in text.lower():
                return text
        return None
    
    def is_product_code(self, text: str) -> bool:
        """Verifica se o texto parece ser um código de produto"""
        # Códigos de barras geralmente têm 13 dígitos
        return bool(re.match(r'^\d{13}$', text.replace(' ', '')))
    
    def extract_price(self, text: str) -> Optional[float]:
        """Extrai preço de um texto"""
        # Padrões para preços brasileiros
        price_patterns = [
            r'(\d+[,.]\d{2})',
            r'(\d+,\d{2})',
            r'(\d+\.\d{2})'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '.')
                try:
                    return float(price_str)
                except ValueError:
                    continue
        return None
    
    def extract_quantity(self, text: str) -> Optional[float]:
        """Extrai quantidade de um texto"""
        # Padrões para quantidades
        qty_patterns = [
            r'(\d+[,.]\d+)\s*kg',
            r'(\d+[,.]\d+)\s*Kg',
            r'(\d+)\s*un',
            r'(\d+)\s*Un'
        ]
        
        for pattern in qty_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                qty_str = match.group(1).replace(',', '.')
                try:
                    return float(qty_str)
                except ValueError:
                    continue
        
        # Se não encontrar padrão específico, tentar extrair apenas números
        if text.strip().replace(',', '.').replace('.', '').isdigit():
            return 1.0  # Quantidade padrão
        
        return None
    
    def extract_items(self, ocr_data: List[Dict]) -> List[Dict]:
        """Extrai itens da nota fiscal"""
        items = []
        current_item = {}
        item_number = 1
        
        # Ordena os dados por posição Y para processar em ordem
        sorted_data = sorted(ocr_data, key=lambda x: x['y_position'])
        
        i = 0
        while i < len(sorted_data):
            item = sorted_data[i]
            text = item['text'].strip()
            
            # Se é um código de produto, inicia um novo item
            if self.is_product_code(text):
                if current_item:  # Salva item anterior se existir
                    items.append(current_item)
                
                current_item = {
                    'numero': item_number,
                    'codigo': text,
                    'descricao': None,
                    'quantidade': None,
                    'preco_unitario': None,
                    'preco_total': None,
                    'desconto': None
                }
                item_number += 1
                
                # Procura descrição nas próximas linhas
                j = i + 1
                while j < len(sorted_data) and j < i + 5:  # Limita busca a 5 linhas
                    next_text = sorted_data[j]['text'].strip()
                    if not self.is_product_code(next_text) and not next_text.replace(',', '.').replace('.', '').isdigit():
                        if len(next_text) > 3 and not any(char.isdigit() for char in next_text[:3]):
                            current_item['descricao'] = next_text
                            break
                    j += 1
            
            # Extrai preços
            price = self.extract_price(text)
            if price and current_item:
                if current_item.get('preco_unitario') is None:
                    current_item['preco_unitario'] = price
                elif current_item.get('preco_total') is None:
                    current_item['preco_total'] = price
            
            # Extrai quantidade
            quantity = self.extract_quantity(text)
            if quantity and current_item and current_item.get('quantidade') is None:
                current_item['quantidade'] = int(quantity) if quantity.is_integer() else quantity
            
            i += 1
        
        # Adiciona último item se existir
        if current_item:
            items.append(current_item)
        
        # Limpa itens inválidos
        valid_items = []
        for item in items:
            if item.get('codigo') and (item.get('descricao') or item.get('preco_total')):
                # Define quantidade padrão se não foi encontrada
                if item.get('quantidade') is None:
                    item['quantidade'] = 1
                valid_items.append(item)
        
        return valid_items
    
    def calculate_totals(self, items: List[Dict]) -> Dict[str, Any]:
        """Calcula totais da nota fiscal"""
        total_items = len(items)
        valor_total = sum(item.get('preco_total', 0) or 0 for item in items)
        valor_total_desconto = sum(item.get('desconto', 0) or 0 for item in items)
        valor_total_pago = valor_total - valor_total_desconto
        
        return {
            'total_itens': total_items,
            'valor_total': round(valor_total, 2),
            'valor_total_desconto': round(valor_total_desconto, 2),
            'valor_total_pago': round(valor_total_pago, 2)
        }
    
    def process_ocr_file(self, file_path: str) -> Dict[str, Any]:
        """Processa arquivo de OCR e retorna dados estruturados"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Parse das linhas do OCR
        ocr_data = []
        for line in lines:
            parsed = self.parse_ocr_line(line)
            if parsed:
                ocr_data.append(parsed)
        
        if not ocr_data:
            raise ValueError("Nenhum dado válido encontrado no arquivo OCR")
        
        # Extrai informações principais
        cnpj = self.extract_cnpj(ocr_data)
        data_emissao = self.extract_date(ocr_data)
        nome_estabelecimento = self.extract_establishment_name(ocr_data)
        items = self.extract_items(ocr_data)
        totals = self.calculate_totals(items)
        
        # Estrutura conforme schema
        result = {
            'chave_acesso': None,  # Não identificado no OCR atual
            'cnpj_estabelecimento': cnpj,
            'cpf': None,  # Não identificado no OCR atual
            'data_emissao': data_emissao,
            'itens': items,
            'nome_estabelecimento': nome_estabelecimento,
            **totals
        }
        
        return result
    
    def save_json(self, data: Dict[str, Any], output_filename: str):
        """Salva dados em arquivo JSON"""
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Arquivo salvo: {output_path}")
    
    def process_file(self, input_file: str, output_file: str = None):
        """Processa um arquivo de OCR"""
        try:
            print(f"Processando arquivo: {input_file}")
            data = self.process_ocr_file(input_file)
            
            if output_file is None:
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_file = f"{base_name}_processado.json"
            
            self.save_json(data, output_file)
            print("Processamento concluído com sucesso!")
            
        except Exception as e:
            print(f"Erro ao processar arquivo: {e}")

def main():
    parser = argparse.ArgumentParser(description='Processa todos os arquivos .txt da pasta Resultados_OCR')
    parser.add_argument('-i', '--input_dir', default='Resultados_OCR', help='Diretório de entrada com arquivos .txt')
    parser.add_argument('-o', '--output_dir', default='Saida_Processada', help='Diretório de saída dos arquivos JSON')
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    output_dir = args.output_dir
    
    processor = OCRProcessor()
    processor.output_dir = output_dir  # Garante que use o output informado
    processor.ensure_output_dir()
    
    # Itera por todos os arquivos .txt no diretório
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_name = f"{os.path.splitext(filename)[0]}_processado.json"
            processor.process_file(input_path, output_name)

if __name__ == "__main__":
    main()
