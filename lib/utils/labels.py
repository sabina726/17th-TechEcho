import json

from lib.constants.choices import label_choices


def parse_labels(request_method):
    labels = request_method.get("labels")
    if not labels:
        return False
    label_list = []
    for label in json.loads(labels):
        label = label["value"]
        if not label_is_valid(label):
            return False
        label_list.append(label)

    return label_list


def label_is_valid(label):
    return label.lower() in label_choices


def parse_form_labels(form):
    labels = form.cleaned_data.get("labels", None)
    if not labels:
        return False

    labels = [label.lower() for label in labels if label.lower() in label_choices]

    if not labels:
        return False

    form.cleaned_data["labels"] = labels
    return True
