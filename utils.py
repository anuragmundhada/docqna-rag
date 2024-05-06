from bs4 import BeautifulSoup
from llama_index.core.schema import TextNode
from unstructured.partition.docx import partition_docx
import json

def convert_html_table_to_dict(html):
    # returns a table as a list of nested dicts
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    headers = [header.text.lower().strip() for header in table.find_all('th')]
    data = []
    rows = table.find_all('tr')[1:]
    for row in rows:
        row_data = {}
        cells = row.find_all('td')
        for i in range(len(headers)):
            row_data[headers[i]] = cells[i].text.strip()
        data.append(row_data)

    return data


def load_and_chunk_docx(filepath):

    with open(filepath, "rb") as f:
        elements = partition_docx(file=f)

    nodes = []


    for element in elements:
        '''
        For each element, checks if it is table or not. 
        if it is a table, splits each row of the table into its own chunk/node. 
        If it is a text, it is one node
        '''

        if element.category == 'Table':
            text_as_html = element.metadata.text_as_html
            table_rows = convert_html_table_to_dict(text_as_html)

            for row in table_rows:
                node = TextNode(text=json.dumps(row))
                nodes.append(node)
        
        else:
            node = TextNode(text=element.text)
            nodes.append(node)
    
    return nodes
