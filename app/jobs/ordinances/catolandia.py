#coding: utf-8
import json, re, traceback, shutil
from .functions import pdfutils
from .functions.utils import ordinance_type
from ... import publisher
from datetime import datetime, timedelta

class text_processing:
    mask_ordinance = r'\d{3}/\d{4}'
    mask_year = r'\d{4}'
    mask_cpf = r'\d*\s*[,*\.*]\s*\d*\s*[,*\.*]\s*\d*[_|–]\s*\d*|\d*\s*[,*\.*]\s*\d*\s*[,*\.*]\s*\d*/\d*[–|_]\s*\d*'
    mask_process = r'[Pp]rocesso\s*[de\s*Licenga\s*Ambiental]*[SEMMATURH]*\s*[Nn]\s*[\.&°:]*\s*(.+?)[\s,*]'
    mask_deadline = r'(\d{2}?)[(\w) ]*ano[s]*|v[aá]lida\s*por\s*(\d*)'
    mask_area = r'[\d+,]* ha'
    mask_lat = r'Lat.[\d\s]*[°|º][\d\s]*[’ ]*[\d,\s]*["|”]\w'
    mask_longitude = r'Long.[\d\s]*[°|º][\d\s]*[’ ]*[\d,\s]*["|”]\w'
    mask_capture = r'captação [\w\s]*'
    mask_flow = r'vazão [\d.]*'
    
    issuer = 6320804
    issuer_name = 'Catolandia'
    labels = ["ordinance_type", "ordinance_number", "process", "publish_date", "owner_id", "issuer_name", "issuer", "term", "link"]
    
    #licenca simplificada
    def ls(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0][0] #+ ' ano(s)'
        
        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.SIMPLIFIED_ENVIRONMENTAL_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg
    
    # licença unificada
    def lu(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.UNIFIED_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg
    
    # licença de operação
    def lo(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.OPERATION_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg

    # licença de implantação
    def limp(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.IMPLANTATION_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg

    # licença de alteração
    def la(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.ALTERATION_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg

    # licença de instalação
    def linst(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.INSTALLATION_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg

    # licença de localização
    def ll(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.LOCATION_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg

    # licença prévia
    def preliminary_license(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.PRELIMINARY_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg

    # supressão de vegatação nativa
    def asv(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        
        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.VEGETAL_SUPPRESSION, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        return reg

    # licença de localização
    def ll(page_text, search_date, dom_link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, page_text)
        deadline = deadline[0] + ' ano(s)'
        

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.LOCATION_LICENSE, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline,
            text_processing.labels[8]: dom_link
        }))
        
        
        return reg

    # prorrogação de prazo de validade
    def deadline_extension(text, search_date, dom_link):
        process = re.findall(text_processing.mask_process, text)[0]
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, text)[0].replace('–','-')
        
        deadline = re.findall(text_processing.mask_deadline, text)[0][0] + ' anos'
        n_ordinance = re.findall(text_processing.mask_ordinance, text)[0]
        changed_ordinance = re.findall(text_processing.mask_ordinance, text)[1]

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.DEADLINE_EXTENSION, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline, 
            text_processing.labels[8]: dom_link
        }))
       
        reg['details'] = {'changed_ordinance': changed_ordinance}
        
        return reg

    # transferência de titularidade
    def tt(page_text, search_date, link):
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-')
        doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        old_doc = doc_number[1].replace('–','-')
        new_doc = doc_number[2].replace('–','-')
        
        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.OWNERSHIP_TRANSFER, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: old_doc, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: None, 
            text_processing.labels[8]: link
        }))
       
        reg['details'] = {'to': new_doc}
        
        return reg


    def license_renewal(page_text, search_date, dom_link):
        mask_renov_type = r'CONCEDE[R]*[:\s]*RENOVA[GC]AO\s*DE\s*LICEN[GCÇ]A\s*[DE\s](.*?),'
        
        n_ordinance = re.findall(text_processing.mask_ordinance, page_text)[0]
        process = re.findall(text_processing.mask_process, page_text)[0].replace('–','-').replace(' ','')
        
        try:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[1].replace('–','-')
        except:
            doc_number = re.findall(text_processing.mask_cpf, page_text)[0].replace('–','-')

        deadline = re.findall(text_processing.mask_deadline, page_text)[0][0] + ' anos'

        renov_type = re.findall(mask_renov_type, page_text.upper())[0]
        
        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.LICENSE_RENEWAL, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: process, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: doc_number, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: deadline, 
            text_processing.labels[8]: dom_link
        }))
       
        reg['details'] = {'license_type': renov_type}
        
        return reg


    # errata
    def erratum(text, search_date, link):
        mask_ordinance = r'[PORTARIA|EDITAL] N° (\d*/\d{4})'

        try:
            n_ordinance = re.findall(text_processing.mask_ordinance, text)[0]
        except:
            try:
                n_ordinance = re.findall(mask_ordinance, text)[0]
            except:
                n_ordinance = None

        old_text = re.findall(r'ONDE|onde*\s*se*\s*[LlIéeE]*[–SE:]*\s*(.*)Leia', text)[0]
        new_text = re.findall(r'LEIA|eia\s*–\*SE|se:(.*)\.\s*Dé', text)[0]

        reg = json.loads(json.dumps({
            text_processing.labels[0]: ordinance_type.ERRATUM, 
            text_processing.labels[1]: n_ordinance, 
            text_processing.labels[2]: None, 
            text_processing.labels[3]: search_date, 
            text_processing.labels[4]: None, 
            text_processing.labels[5]: text_processing.issuer_name, 
            text_processing.labels[6]: text_processing.issuer, 
            text_processing.labels[7]: None, 
            text_processing.labels[8]: link,
            'details': None
        }))
       
        reg['details'] = {
            'old': old_text,
            'new': new_text
        }
        return reg 
    

def _import_date(search_date):
    type_list = [
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL]*\s*SIMPLIFICADA',
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL]*\s*UNIFICADA',
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL DE]*\s*OPERA[GCÇ][AÃ]O',
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL DE]*\s*IMPLANTA[GCÇ][AÃ]O',
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL DE]*\s*INSTALA[GCÇ][AÃ]O',
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL DE]*\s*LOCALIZA[GCÇ][AÃ]O',
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL DE]*\s*ALTERA[GCÇ][AÃ]O',
        r'CONCEDE[R]*\s*LICEN[GCÇ]*A\s*[AMBIENTAL]*\s*PR[EÉ]VIA',
        r'CONCEDE[R]*\s*AUTORIZA[GÇC]*[AÃ]O\s*PARA\s*SUPRESS[AÃ]O\s*D[EA]\s*VEGETA[CÇG]*[AÃ]O\s*NATIVA',
        r'CONCEDER[R]*\s*[A ]*PRORROGA[GC]AO\s*D[EO]\s*PRAZO\s*D[AE]\s*VALIDADE',
        r'CONCEDER[R]*\s*[A ]*TRANSFER[ÊE]NCIA\s*DE\s*TITULARIDADE',
        r'RENOVA[GÇC][ÃA]O\s*DE*\s*LICEN[GCÇ]A',
        r'REVIS[AÃ]O\s*DO\s*CONDICIONANTE'        
    ]

    type2function = {
        type_list[0]: 'ls',
        type_list[1]: 'lu',
        type_list[2]: 'lo',
        type_list[3]: 'limp',
        type_list[4]: 'linst',
        type_list[5]: 'll',
        type_list[6]: 'la',
        type_list[7]: 'preliminary_license',
        type_list[8]: 'asv',
        type_list[9]: 'deadline_extension',
        type_list[10]: 'tt',
        type_list[11]: 'license_renewal',
        type_list[12]: 'condition_review'              
    }

    files, links, folder = pdfutils.dom_catolandia(search_date)

    regs = [] 
    
    # verifica se o documento foi encontrado
    for filename, link in zip(files, links):
        pages = pdfutils.ocr_extract_page_text(filename)
        print("Reading file")

        for page in pages:
            ordinance_text = page.replace('-','–')
            for ord_type in type_list:
                # print(ordinance_text)

                # verifica se o tipo da portaria é conhecido de acordo com o vetor "type_list"
                if len(re.findall(ord_type, ordinance_text.upper())) > 0:

                    try:
                        # chama a função que irá processar a portaria de acordo com o dicionário "type2function"
                        reg = getattr(text_processing, type2function[ord_type])(ordinance_text, search_date, link)
                        
                        # print(reg)

                        regs.append(reg)

                        publisher.publish('NEW_ORDINANCE', reg)
                    except:
                        print(ordinance_text)
                        traceback.print_exc()

                    print('')

    try:
        shutil.rmtree(folder)
    except FileNotFoundError:
        pass
    
    print(f'{ len(regs) } ordinance(s) imported')

    return regs
    
def import_news():
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    _import_date(yesterday)
    