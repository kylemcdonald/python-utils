from IPython.core.display import display_html, HTML

def pixelate():
    display_html(HTML('<style>img{image-rendering: pixelated}</style>'))