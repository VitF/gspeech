from difflib import HtmlDiff
import pathlib
import re
import webbrowser

from karen import *


SRC_FILE    =   "./texts/source.txt"
IN_FILE     =   "./texts/input.txt"
REV_FILE    =   "./texts/revised.txt"
CHG_FILE    =   "./output/changes"
TEMPLATE    =   "./template.html"


def cleanup():

    filenames = ['./output/changes_raw.html']

    for name in filenames:
        pathlib.Path(name).unlink(missing_ok=True)


def view_html():

    html_file = pathlib.Path(f'{CHG_FILE}.html').resolve()   # full path
    webbrowser.open(html_file.as_uri())


def text_breakdown(text: str) -> list:

    # Split the text keeping the punctuation
    parts  = [s.strip() for s in re.split(r'([.!?]+)\s+', text) if s.strip()]
    sentences, ii = [], 0
    while ii < len(parts):
        sentence = parts[ii]
        if ii+1 < len(parts) and parts[ii+1] in {'.', '!', '?', '...'}:
            sentence += parts[ii+1]
            ii += 1
        sentences.append(sentence)
        ii += 1
    
    return sentences


def main():

    with open(SRC_FILE, "r", encoding='utf-8') as f:
        src_ = f.read()
    
    with open(IN_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(text_breakdown(src_)))
    
    with open(IN_FILE, "r", encoding='utf-8') as f:
        in_ = f.read()

    # Sentence-by-sentence text revision
    sentences = []
    rev_ = []
    for sentence in text_breakdown(src_):
        sentences.append(sentence)
        rev_.append(karen_correct(text=sentence, standalone=False))
    
    with open("./output/sentences.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(sentences))

    with open(REV_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rev_))

    with open(REV_FILE, "r", encoding='utf-8') as f:
        rev_ = f.read()
    
    # Changes inspection and HTML file preparation
    delta = HtmlDiff().make_file(in_.splitlines(), rev_.splitlines())
    with open(f"{CHG_FILE}_raw.html", "w", encoding="utf-8") as f:
        f.write(delta)

    with open(f"{CHG_FILE}_raw.html", "r", encoding="utf-8") as f:
        html_ = f.read()
        html_ = re.sub(r'cellpadding="0"', 'cellpadding="5"', html_, flags=re.S|re.I)
        html_ = re.sub(r'<a\b[^>]*>.*?</a>', '', html_, flags=re.S|re.I)
        html_ = re.sub(r'Legends', 'Legend', html_, flags=re.S|re.I)
        html_ = re.sub(r'(?s)<td> <table\b[^>]*\bsummary="Links"[^>]*>.*?</table></td> </tr>', '', html_, flags=re.S|re.I)

    legend_idx = html_.find('<table class="diff" summary="Legend">')

    with open(f"{CHG_FILE}_raw.html", "w", encoding="utf-8") as f:
        f.write(html_[:legend_idx] +\
                '<p>' + '&nbsp;' + '</p>' + "\n\t" +\
                html_[legend_idx:])
    
    raw_ = pathlib.Path(f"{CHG_FILE}_raw.html")
    template_ = pathlib.Path(TEMPLATE)
    out_ = pathlib.Path(f"{CHG_FILE}.html")
    
    START   = '<table class="diff" id="difflib_chg_to0__top"'
    END     = '</table>'
    MARKER  = '[TABLE OF CHANGES]'
    
    block = re.search(f'{re.escape(START)}(.*?){re.escape(END)}',
                      raw_.read_text(encoding='utf-8'),
                      flags=re.S).group(0)
    
    html2 = template_.read_text(encoding='utf-8')
    new   = html2.replace(MARKER, block)
    out_.write_text(new, encoding='utf-8')


if __name__ == "__main__":

    main()

    cleanup()

    view_html()
