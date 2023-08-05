# Domain Network
A package to create a domain network of the URLs mentioned in a dataset of texts. 
In the current version it works for tweets. It may process any kind of text in the future versions.
##Installation
The easiest way to install the domain_network package is to use the following command in a terminal:

``` bash
pip install domain-network

```
## Usage

To run the module using Command Line Interface (CLI) run the following:

- For the whole process starting with raw tweets:

``` bash
python -m domainNetwork  --input_dir ["data/twitterAPI_lang_en/*/*.json"] --conf_dir  [‘config/sample_config.ini’] --min_edge_weight [20] --min_node_size [20] \
--min_stand_alone_size [50]   --urls_file_name  ["output/urls.csv"] \
--network_output_file_name  ["output/network.csv"] --netloc_output_file_name ["output/netloc.csv"] \
--netloc_origin_output_file_name  ["output/netloc_origin.csv"] 
```

- For making domain network of a pre-processed file which includes extracted netlocs: 
``` bash
python -m domainNetwork  --conf_dir  [‘config/sample_config.ini’] --min_edge_weight [20] --min_node_size [20] \
--min_stand_alone_size [50]  --network_only true  --urls_file_name  ["data/urls.csv"] \
--network_output_file_name  ["output/network.csv"] --netloc_output_file_name ["output/netloc.csv"] \
--netloc_origin_output_file_name  ["output/netloc_origin.csv"] 
```
### Parameters:

--input_dir : Directory of tweet files

--conf_dir : File path of the config file. Read Config file section for more details.

--min_edge_weight : Min number of users that mentioned both source and target of the edge in their tweets.

--min_node_size : Min number of times that a web page is mentioned in total, for connected nodes.

--min_stand_alone_size: Min number of times that a web page is mentioned in total, for stand-alone nodes.

--network_only : If you want to use a preprocessed file which includes the netlocs

--urls_file_name : File path of preprocessed tweets with netlocs. Can be output/input file in the above mentioned situations.

--network_output_file_name: File path of the generated network, in .csv format.

--netloc_output_file_name : File path of the list of web sites, after filtering, in .csv format.

--netloc_origin_output_file_name : File path of the original list of web sites, in .csv format.

### Output
The main output of this package is network.csv which includes source, target and the weight.
Output file can be given to a visualization tool, e.g. networkx in python for the visualization