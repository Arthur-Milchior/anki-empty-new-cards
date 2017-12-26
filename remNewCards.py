# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# feel free to contribute on https://github.com/Arthur-Milchior/anki-empty-new-cards

import aqt
from aqt import mw
from aqt.qt import *
from anki.collection import _Collection
from anki.utils import ids2str

oldGenCards= _Collection.genCards
def genCards(self,nids):
    cids = oldGenCards(self,nids)
    cids=ids2str(cids)
    command="select id from cards where (type=0 and (id in "+ cids+"))"
    print command
    cids=self.db.list(command)
    print cids
    #todo: tagger
    return cids

def check():
    _Collection.genCards=genCards
    mw.onEmptyCards()
    _Collection.genCards=oldGenCards

action = QAction(aqt.mw)
action.setText("Empty new cards")
mw.form.menuTools.addAction(action)
action.triggered.connect(check)

