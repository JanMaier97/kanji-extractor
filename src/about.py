import aqt.forms
from aqt.qt import *

class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog, self).__init__()

        self.ui = aqt.forms.about.Ui_About()
        self.ui.setupUi(self)
        self.ui.label.setMinimumWidth(800)
        self.ui.label.setMinimumHeight(600)
        self.ui.label.stdHtml(self.get_about_text(),js=" ")
        self.setWindowTitle("About Kanji-Extractor")

    def get_about_text(self):
        about = '<p>Kanji-Extractor is an add-on for Anki, which creates notes for learning Kanji, which appear in the vocabulary notes. The add-on is open source and can be found on <a href="https://github.com/JanMaier97/kanji-extractor">GitHub</a>. The source code is licenced under the MIT License. Please see the license file in the source repository for more information.</p>'
        about += '<p>The data used to create the kanji notes is mostly provided by the <a href="https://www.edrdg.org/wiki/index.php/KANJIDIC_Project">KANJIDIC2</a> dictionary file. Information about the kanji radicals including their variants and meaning is provided by <a href="https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_stroke_count">Wikipedia</a>. Please see the acknowledgements for more information.</p>'
        about += '<h2>Acknowledgements</h2>'
        about += '<p>This add-on uses the <a href="https://www.edrdg.org/wiki/index.php/KANJIDIC_Project">KANJIDIC2</a> dictionary file. The file is the property of the <a href="https://www.edrdg.org/">Electronic Dictionary Research and Development Group</a>, and are used in conformance with the Group\'s <a href="https://www.edrdg.org/edrdg/licence.html">licence</a>.</p>'
        about += '<p>Information about the kanji radicals (literal, variants and meaning) comes from <a href="https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_stroke_count">Wikipedia</a> and is licenced under the <a href="https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License">Creative Commons Attribution-ShareAlike License</a>.</p>'

        return about
