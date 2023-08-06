# Citation style classifier

Citation style classifier can automatically infer citation style from a reference string. The classifier is a Logistic Regression model trained on 90,000 reference strings. The following citation styles are supported by default:

  * acm-sig-proceedings
  * american-chemical-society
  * american-chemical-society-with-titles
  * american-institute-of-physics
  * american-sociological-association
  * apa
  * bmc-bioinformatics
  * chicago-author-date
  * elsevier-without-titles
  * elsevier-with-titles
  * harvard3
  * ieee
  * iso690-author-date-en
  * modern-language-association
  * springer-basic-author-date
  * springer-lecture-notes-in-computer-science
  * vancouver
  * unknown

The package contains the training data, the classification model, and the code for feature extraction, selection, training and prediction.

## Installation

        pip3 install styleclass

## Classification

From command line:

        styleclass_classify -r "reference string"
        styleclass_classify -i /file/with/reference/strings/one/per/line -o /output/file

In Python code:

        from styleclass.classify import classify
        from styleclass.train import get_default_model

        model = get_default_model()
        prediction = classify("reference string", *model)
        prediction = classify(["reference string #1", "reference string #2", "reference string #3"], *model)

## Data

Styleclass package contains [two datasets](https://gitlab.com/crossref/citation_style_classifier/tree/master/styleclass/datasets): training set and test set. Each of them contains a sample of 5,000 DOIs formatted in 17 citation styles (listed above), which gives 85,000 reference strings. Both datasets were generated automatically using Crossref REST API.

A new dataset can be generated using the script `styleclass_generate_dataset`.

## Models

The [default model](https://gitlab.com/crossref/citation_style_classifier/tree/master/styleclass/models) was trained on the training dataset. Before the training, the dataset was cleaned and enriched with random noise. 5,000 strings with "unknown" style were also generated and added to the dataset.

Script `styleclass_train_model` can be used to train a new model. This is useful especially when you need to operate of a different set of citation styles than our default. The script prepares the data for training in the same was as was done for training of the default model.

## Evaluation

`styleclass_evaluate` script can be used to evaluate exisitng model on a test set, in terms of accuracy.

The accuracy of the default model estimated on our test set is 95%.
