#! /usr/bin/bash

psql -q -h usdf-prompt-processing-dev.slac.stanford.edu lsst-devl rubin -c "set search_path to tasso; COPY (select classification.*, subject.dia_source_id from classification INNER JOIN subject on classification.subject_id = subject.subject_id where classification.run_id = '$1') To STDOUT With CSV HEADER DELIMITER ',';" > classifications_$1.csv
