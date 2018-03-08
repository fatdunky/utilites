'''
Created on 12 Dec. 2017

@author: mcrick
'''


from yattag import Doc

def coloured_p_text(message, colour):
    doc, tag, text = Doc().tagtext()
    style = ("color:%s" % colour)
    with tag('p', style=style):
        text(message)
    
    return doc.getvalue()

def coloured_p_text_background(message, colour, bg_colour):
    doc, tag, text = Doc().tagtext()
    style = ("color:%s;background-color:%s" % (colour,bg_colour))
    with tag('p', style=style):
        text(message)
    
    return doc.getvalue()
    

def p_text(message):
    doc, tag, text = Doc().tagtext()
    with tag('p'):
        text(message)
    
    return doc.getvalue()

def h1_text(message):
    doc, tag, text = Doc().tagtext()
    with tag('h1'):
        text(message)
    
    return doc.getvalue()

def h2_text(message):
    doc, tag, text = Doc().tagtext()
    with tag('h2'):
        text(message)
    
    return doc.getvalue()

def h3_text(message):
    doc, tag, text = Doc().tagtext()
    with tag('h3'):
        text(message)
    
    return doc.getvalue()

def table_open():
    return '<table>'

def table_row_open():
    return '<tr>'

def table_row_close():
    return '</tr>'

def table_data_open():
    return '<td>'

def table_data_close():
    return '</td>'

def table_close():
    return '</table>'

def add_body_around_html(existing_html):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('body'):
            for line in existing_html:
                doc.asis(line)
                
    return doc.getvalue()


def br_line():
    doc, tag, text = Doc().tagtext()
    doc.stag('br')
    return doc.getvalue()
