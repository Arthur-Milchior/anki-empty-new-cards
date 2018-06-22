# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""I do not like to delete cards. If some cards where reviewed and no longer exists, it is probably a sign that I made something wrong.
However, I sometime create thoushands of new cards by accident, when I edit a card type. And I want to delete those cards without deleted the one viewed at least once.
Hence, this add-on."""

import aqt
from aqt import mw
from aqt.qt import *
from anki.collection import _Collection
from anki.utils import ids2str

oldGenCards= _Collection.genCards
def genCards(self,nids):
    col = mw.col
    cids = oldGenCards(self,nids)
    cids=ids2str(cids)
    toDeleteCids=col.db.list("select id from cards where (type=0 and (id in "+cids+"))")
    #l =[]
    #for id in toDeleteCids:
    print ("genCards: %s" %str(toDeleteCids))
    return toDeleteCids

def check():
    _Collection.genCards=genCards
    mw.onEmptyCards()
    _Collection.genCards=oldGenCards

action = QAction(aqt.mw)
action.setText("Empty new cards")
mw.form.menuTools.addAction(action)
action.triggered.connect(check)

