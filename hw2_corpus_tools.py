# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 12:30:28 2020

@author: Likhita Suresh
"""

from collections import namedtuple
import csv
import glob
import os

def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

def get_data(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    for dialog_filename in dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple(
    "DialogUtterance", ("act_tag", "speaker", "pos", "text"))

DialogUtterance.__doc__ = """\
An utterance in a dialog. Empty utterances are None.

act_tag - the dialog act associated with this utterance
speaker - which speaker made this utterance
pos - a list of PosTag objects (token and POS)
text - the text of the utterance with only a little bit of cleaning"""

PosTag = namedtuple("PosTag", ("token", "pos"))

PosTag.__doc__ = """\
A token and its part-of-speech tag.

token - the token
pos - the part-of-speech tag"""

def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with 
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)