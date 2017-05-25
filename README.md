# django

solr-4.10.4 required for the project search engine to work
after unziping solr 
Inside the example directory within the solr-4.10.4/
directory, create a new directory and name it blog . Then create the following empty
files and directories inside it:
blog/
-data/
-conf/
-protwords.txt
-schema.xml
-solrconfig.xml
-stopwords.txt
-synonyms.txt
-lang/
--stopwords_en.txt
replace schema.xml and solrconfig.xml from includes with those in solr/example/solr/
start solr 
  cd solr-4.10.4/example
  java -jar start.jar
  
go to http://127.0.0.1:8983/solr/#/
  go to `Core admin ` and `add Core`
    name : blog
    instanceDir : blog
    dataDir : data
    config: solrconfig.xml
    schema : schema.xml
    
  add core
  
the project solr search engine will be functional after successful configuration
