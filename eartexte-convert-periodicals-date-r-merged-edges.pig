--Pig script written by Tomasz Neugebauer (tomasz.neugebauer@concordia.ca)
--2017
--MIT license

DEFINE XPath org.apache.pig.piggybank.evaluation.xml.XPath();
DEFINE XPathAll org.apache.pig.piggybank.evaluation.xml.XPathAll();

--REGISTER datafu-pig-incubating-1.3.1.jar;
--define Transpose datafu.pig.util.Transpose();
--define TransposeTupleToBag datafu.pig.util.TransposeTupleToBag();

register 'convert-data.py' using jython as UDFToBagConverter ;
register 'convert-data-name.py' using jython as UDFToStringCleaner ;
-- also uses gml-header-footer.py to output GML results
-- also uses cleanup.py to clean up quotes in GML results

--======================================================================================
--usage: specify datafile from command line
--for example:
--pig -x local -param datafile="XML/data_humanist_photography.xml" eartexte-convert.pig
--======================================================================================
--%declare datafile 'XML/data_humanist_photography.xml';


A = load '$datafile' using org.apache.pig.piggybank.storage.XMLLoader('eprint') as (x:chararray);


--=========================================================================================================
--*********************************************************************************************************
--=========================================================================================================
--========================contributors==============
B2 = FOREACH A GENERATE XPath(x, 'eprint/eprintid') as (eprintid:chararray),
XPath(x, 'eprint/publication') as (title:chararray),
XPathAll(x, 'eprint/contributors/item/name') as (nodeb:tuple()),
CONCAT ('|', XPath(x, 'eprint/publication')) as (separatorPLUStitle:chararray),
XPath(x, 'eprint/date') as (pubDate:chararray);

data2 = FOREACH B2 GENERATE *,CONCAT (eprintid, separatorPLUStitle) as (nodea:chararray);
C2 = FOREACH data2 GENERATE nodea, UDFToBagConverter.convert(nodeb), $4 as (pubDate:chararray);
D2 = FOREACH C2 GENERATE nodea, FLATTEN($1), pubDate;
E2 = FILTER D2 BY TRIM($1) != '';
I2 = FOREACH E2 GENERATE $0,'contributor', REPLACE(TRIM($1), '^, ', ''), pubDate;
I2_1 = FOREACH I2 GENERATE $0,$1, REPLACE(TRIM($2), ',           , ',', '), pubDate;
I2 = FOREACH I2_1 GENERATE $0,$1, REPLACE(TRIM($2), ',$',''), pubDate;
I2 = FILTER I2 BY TRIM($2) != '';
--==========co-contributors========
inpt = foreach I2 generate CONCAT(SUBSTRING($0, 0, 35),'...') as (id:chararray), REPLACE(REPLACE(REPLACE($2,'\\]','_'),'\\[','_'),'"','_') as (val), pubDate;
contributors = foreach inpt generate $0,'contributor',$1, $2;
grp = group inpt by (id);
id_grp = foreach grp generate group as id, inpt.val as value_bag, inpt.pubDate as pubDate;
co_contributor = foreach id_grp generate FLATTEN(value_bag) as v1, id, FLATTEN(value_bag) as v2, pubDate;
co_contributor = filter co_contributor by v1 <= v2;
co_contributor = filter co_contributor by v1 != v2;
--==========co-contributors - edge file output - GML ========
--==== node list=====
node_idA = foreach inpt generate TRIM($1) as name, $2 as years, TRIM($1) as label;
node_idA = filter node_idA by (name) != '';
node_idA = DISTINCT node_idA;
node_idA = group node_idA by (name);
nodelist = foreach node_idA generate 'node','[', 'id', UDFToStringCleaner.convert_name(node_idA.name),'label', UDFToStringCleaner.convert_label(node_idA.label), 'SInterval', UDFToStringCleaner.convert_date(node_idA.years),UDFToStringCleaner.convert_date_r(node_idA.years),']';
nodelist_co = nodelist;
--==== edge list====
edge = foreach co_contributor generate TRIM($0),$1,TRIM($2);
edge = filter edge by $0 != '';
edge = filter edge by $2 != '';
edgelist_withedgelabels = foreach co_contributor generate *;
edgelist_withedgelabels = group edgelist_withedgelabels by ($0,$2);
edgelist_withedgelabels = foreach edgelist_withedgelabels generate 'edge','[', 'source',FLATTEN($0), 'attributes',$1,']';
edgelist_withedgelabels = foreach edgelist_withedgelabels generate 'edge','[', 'source',$3, 'target', $4, 'weight',COUNT($6),'',UDFToStringCleaner.convert_date_merged_edge_r($6),'magazines',UDFToStringCleaner.merged_edge_r_magazines($6),']';
-- edgelist_withedgelabels = foreach edgelist_withedgelabels generate 'edge','[', 'source',$0, 'target',$1,'label',REPLACE(REPLACE(REPLACE(id,'\\]','_'),'\\[','_'),'"','_'), 'SInterval', UDFToStringCleaner.convert_date_edge($3), 'magazine', REGEX_EXTRACT(id, '(\\d*)\\|(.*)\\.\\.\\.', 2), UDFToStringCleaner.convert_date_edge_r($2),']';
edgelist_co_contributors = foreach edgelist_withedgelabels generate $0;

gml_withedgelabels = union nodelist, edgelist_withedgelabels;
gml_withedgelabels = ORDER gml_withedgelabels BY $0 DESC;

rmf TMP/co_contributor-gml-with_edge_labels
STORE gml_withedgelabels INTO 'TMP/co_contributor-gml-with_edge_labels' USING org.apache.pig.piggybank.storage.CSVExcelStorage(' ', 'NO_MULTILINE', 'WINDOWS');
rmf TMP/merged-file-co_contributor-gml-with_edge_labels.gml
fs -getmerge  TMP/co_contributor-gml-with_edge_labels TMP/merged-file-co_contributor-gml-with_edge_labels.gml
sh python cleanup.py -i TMP/merged-file-co_contributor-gml-with_edge_labels.gml -o TMP/merged-file-co_contributor-gml-with_edge_labels-cleaned.gml
sh python gml-header-footer.py -i TMP/merged-file-co_contributor-gml-with_edge_labels-cleaned.gml -o OUTPUT/merged-file-co_contributor-dynamic-gml-with_edge_labels-withheader.gml


rmf TMP/edgelist_co-contributors
STORE edgelist_co_contributors INTO 'TMP/edgelist_co-contributors' USING org.apache.pig.piggybank.storage.CSVExcelStorage('\t', 'NO_MULTILINE', 'WINDOWS');
rmf OUTPUT/EDGELISTS/merged-file-edgelist_co-contributors.csv
fs -getmerge  TMP/edgelist_co-contributors OUTPUT/EDGELISTS/merged-file-edgelist_co-contributors-dynamic.csv




