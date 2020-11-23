# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# feel free to contribute on https://github.com/Arthur-Milchior/anki-empty-new-cards
# Anki add-on number: 1402327111

import aqt
from anki.collection import _Collection
from anki.consts import MODEL_STD
from anki.utils import ids2str
from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from aqt import gui_hooks
from anki.consts import CARD_TYPE_NEW

from .config import getUserOption

delete_seen_card = True

def filter(diag: aqt.emptycards.EmptyCardsDialog):
    global delete_seen_card
    if delete_seen_card:
        return
    delete_seen_card = True
    report = diag.report
    notes = report.notes
    seen_cids = []
    for note in notes:
        new_cids = []
        for cid in note.card_ids:
            if mw.col.db.scalar("select type from cards where id = ?", cid) == CARD_TYPE_NEW:
                new_cids.append(cid)
            else:
                seen_cids.append(cid)
        del note.card_ids[:]
        note.card_ids.extend(new_cids)
    for note in diag.report.notes:
    tag(seen_cids)

gui_hooks.empty_cards_will_show.append(filter)


def tag(cids):
    # deleting tags of cards currently having it
    nids_to_tag_to_remove = dict()
    nids_to_tag_to_add = dict()
    nids = mw.col.findNotes("tag:empty_card_*")
    for nid in nids:
        nids_to_tag_to_remove[nid] = set()
        deleted = False
        note = mw.col.getNote(nid)
        for tag in note.tags:
            if tag.startswith("empty_card_"):
                nids_to_tag_to_remove[nid].add(tag)

    toKeepCids = mw.col.db.list(
        "select id from cards where (type!=0 and (id in "+ids2str(cids)+"))")
    for cid in toKeepCids:
        card = mw.col.getCard(cid)
        model = card.model()
        if model["type"] == MODEL_STD:
            tmpls = model["tmpls"]
            tmpl = tmpls[card.ord]
            template_name = tmpl["name"]
        else:
            template_name = f"card_{card.ord + 1}"
        tag = f"empty_card_{template_name}"
        tag = tag.replace(" ", "_")
        tag = tag.lower()  # Assume there is a card type basic and a card type Basic. I can't add empty_card_basic and empty_card_Basic in the collection. So need to normalize
        note = card.note()
        nid = note.id
        if nid in nids_to_tag_to_remove and tag in nids_to_tag_to_remove[nid]:
            nids_to_tag_to_remove[nid].remove(tag)
            if not nids_to_tag_to_remove[nid]:
                del nids_to_tag_to_remove[nid]
        else:
            if nid not in nids_to_tag_to_add:
                nids_to_tag_to_add[nid] = set()
            nids_to_tag_to_add[nid].add(tag)

    nb_added = 0
    for nid in set(nids_to_tag_to_add.keys()) | set(nids_to_tag_to_remove.keys()):
        note = mw.col.getNote(nid)
        for tag in nids_to_tag_to_add.get(nid, []):
            note.addTag(tag)
            nb_added += 1
        for tag in nids_to_tag_to_remove.get(nid, []):
            note.delTag(tag)
        note.flush()
    tooltip(f"Added {nb_added} empty_card_* tags")


def check():
    global delete_seen_card
    delete_seen_card = False
    mw.onEmptyCards()


action = QAction(aqt.mw)
action.setText("Empty new cards")
mw.form.menuTools.addAction(action)
action.triggered.connect(check)
