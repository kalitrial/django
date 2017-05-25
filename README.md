# django

solr-4.10.4 required for the project search engine to work
after unziping solr copy `blog` from includes into solr/example/solr/
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
