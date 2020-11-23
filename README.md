# Delete empty cards only if they are new
## Rationale
I do not like to delete cards. If some cards where reviewed and no
longer exists, it is probably a sign that I made something wrong. When
I correct this error, those empty cards will still be here with their
review history. Great !

However, I sometime create thoushands of new cards by accident, when I
edit a card type. I want to be able to delete those card.

The tradeoff I found is deleting cards only when they are new.
If, sometime, I find and empty card, already seen, and it's not a
mistake, I just have to suspend it, and everything is all right.

I also tag notes which should have been deleted. This can be turned
of in the configuration.

## Usage
From main window, select "Tools">"Empty new cards". It acts similarly
to "Empty cards".

## Internal
This add-on redefine anki.collection._Collection.genCards during the
process. The new method call the previous one.

The previous method is set back once the action is done.

## Warning concerning the list of notes

For technical reason, it's hard to change the list of note and card that will be deleted without a lot of work. So the
list of cards to be deleted is not changed and contains cards already seen that won't actually be deleted. Furthermore,
for each note with no valid card, if you decide to keep those notes, then both the first card and all seen cards will be
kept. This is not an ideal solution, but I've not enough time and interest to improve it.



## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-empty-new-cards
Addon number| [1402327111](https://ankiweb.net/shared/info/1402327111)
