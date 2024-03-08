import os
import sys
import json
import time
import networkx as nx
import community as cm
import collections
import csv
import matplotlib.pyplot as plt
G=nx.Graph()
auth_cities={57190883130:set(), 23392711700:set(),8905960300:set(),6603178468:set(),7003638977:set(),24765908100:set(),53880298500:set(),7003954863:set(),55884599100:set(),57200498082:set(),6603550679:set(),55546759400:set(),56613081700:set(),57191622205:set(),56826065900:set(),57190883130:set(),57043755900:set(),57191505920:set()}
trackauth=[57190883130,56826065900,23392711700,8905960300,6603178468,7003638977,24765908100,53880298500,7003954863,55884599100,57200498082,6603550679,55546759400,56613081700,57191622205,56826065900,57190883130,57043755900,57191505920]
authpub={57190883130:0,56826065900:0,23392711700:0,8905960300:0,6603178468:0,7003638977:0,24765908100:0,53880298500:0,7003954863:0,55884599100:0,57200498082:0,6603550679:0,55546759400:0,56613081700:0,57191622205:0,56826065900:0,57190883130:0,57043755900:0,57191505920:0}

authnames={57190883130:set(),23392711700:set(),8905960300:set(),6603178468:set(),7003638977:set(),24765908100:set(),53880298500:set(),7003954863:set(),55884599100:set(),57200498082:set(),6603550679:set(),55546759400:set(),56613081700:set(),57191622205:set(),56826065900:set(),57190883130:set(),57043755900:set(),57191505920:set()}
authpapername={57190883130:set(),23392711700:set(),8905960300:set(),6603178468:set(),7003638977:set(),24765908100:set(),53880298500:set(),7003954863:set(),55884599100:set(),57200498082:set(),6603550679:set(),55546759400:set(),56613081700:set(),57191622205:set(),56826065900:set(),57190883130:set(),57043755900:set(),57191505920:set()}
affiliation_city = {}
auth_pub={}
bothenc=0

def debug(x, end = '\n'):
    sys.stderr.write(x)
    sys.stderr.write(end)



def extract_data_from_json(filename):
    debug("extract_data_from_json('%s')" % (filename))
    # open input json file
    filepath = os.getcwd() + '\\' + filename
    f = open(filepath)

    # parse json file
    data = json.loads(f.read())

    return data

def extract_edges(papers):
    global bothenc
    debug("extract_edges()")

    #retrieve nodes
    for paper in papers:
        if (not paper.get('affiliation')):
            continue
        aff = paper['affiliation']
        if (type(aff) is list):
            for a in aff:
                if(a.get('afid') and a.get('affiliation-city') and a.get('affiliation-country')):
                    affid = int(a['afid'])
                    affiliation_city[affid] = a['affiliation-city'].lower()+' '+a['affiliation-country'].lower()
        else:
            if(aff.get('afid') and aff.get('affiliation-city') and aff.get('affiliation-country') ):
                affid = int(aff['afid'])
                affiliation_city[affid] = aff['affiliation-city'].lower()+' '+aff['affiliation-country'].lower()
        if (not paper.get('author')):
            continue
        if(paper.get('prism:publicationName') and paper.get('prism:coverDate')):
            papername=paper['prism:publicationName']+paper['prism:coverDate']
        else:
            papername='false'
        print(papername)
        author = paper['author']
        # if there are many authors, iterate through all of them and add them to the list
        if (type(author) is list):
            for a in author:

                idauth=int(a['authid'])
                if (auth_pub.get(idauth)):
                    auth_pub[idauth] += 1
                else:
                    auth_pub[idauth] = 1


                if(idauth in authnames.keys() and a.get('authname')):
                    authnames[idauth].add(a['authname'])
                    authpub[idauth]+=1
                    if(papername!='false'):
                        authpapername[idauth].add(papername)
                G.add_node(idauth)
        else:
            # if there is only 1 author, just add him directly to the list
            idauth = int(author['authid'])
            if (auth_pub.get(idauth)):
                auth_pub[idauth] += 1
            else:
                auth_pub[idauth] = 1
            if (idauth in authnames.keys() and author.get('authname')):
                authnames[idauth].add(author['authname'])
                authpub[idauth] += 1

            G.add_node(int(author['authid']))
    # retrieve edges
    for paper in papers:
        # if that entry doesn't have an author ==> it's not a paper
        unique = set()
        if (not paper.get('author')):
            continue
        else:
            authors = paper['author']

        # if there is only 1 author, ignore this paper
        if (not type(authors) is list):

            if(authors.get('afid')):
                afids=authors['afid']
                if(type(afids) is not list):
                    if (affiliation_city.get(int(afids)) and int(authors['authid']) in auth_cities.keys()):
                        auth_cities[int(authors['authid'])].add(affiliation_city[int(afids)])
                else:
                    for afid in afids:
                        if (affiliation_city.get(int(afid)) and  int(authors['authid']) in auth_cities.keys()):
                            auth_cities[int(authors['authid'])].add(affiliation_city[int(afid)])

            continue
        else:
            for U in authors:
                if (U.get('afid')):
                    afids = U['afid']
                    if (type(afids) is not list):
                        if (affiliation_city.get(int(afids)) and int(U['authid']) in auth_cities.keys()):
                            auth_cities[int(U['authid'])].add(affiliation_city[int(afids)])
                    else:
                        for afid in afids:
                            if (affiliation_city.get(int(afid)) and int(U['authid']) in auth_cities.keys()):
                                auth_cities[int(U['authid'])].add(affiliation_city[int(afid)])
                for V in authors:
                    # get author ids
                    u = int(U['authid'])
                    v = int(V['authid'])
                    t=u^v

                    # since we are looping over the same array, we should skip this case
                    if (u == v or t in unique):
                        continue

                    # undirected graph ==> (u,v) == (v, u)
                    # to store only 1/2 of the memory
                    # we will always use key (u,v) such as u is smaller than v
                    x, y = min(u, v), max(u, v)
                    u, v = x, y

                    # checking if dictionary keys exist before accessing them
                    if G.has_edge(u,v):
                        # increment nbr of collabs by 1
                        G[u][v]['weight']+=1

                        # add the corresponding paper id
                       # edges[u][v][1].append(paper['dc:identifier'][10:])  # the [10:] is just to delete the
                     # "SCOPUS_ID:" part
                    else:
                        G.add_edge(u,v,weight=1)
                    unique.add(u ^ v)

def extract_all():
    path = 'D:\ourPFEstatistics\json\COMP'

    folder = os.fsencode(path)

    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.json')):
            data = extract_data_from_json(filename)
            papers = data['search-results']['entry']
            extract_edges(papers)


def export_degree_hist(filename):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    # ax.set_xticks([d + 0.4 for d in deg])
    # ax.set_xticklabels(deg)
    plt.savefig(filename + '.png')
    plt.clf()


def export_graphml(filename):
    debug("export_graphml('%s')" % filename)
    # create a file .graphml to output the graph coded in graphml
    output_file = open(filename, "w+")

    debug("---- file created : %s" % filename)
    sys.stdout = output_file

    # graphml format is structured as follows :
    #     - xml_header
    #     - nodes declarations
    #     - edges declarations
    #     - xml_footer

    res = ""

    xml_header = "<?xml version='1.0' encoding='utf-8'?>"
    xml_header += '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">'
    xml_header += '<graph edgedefault="undirected">\n'  # undirected graph

    sys.stdout.write(xml_header)

    debug("---- xml_header : done.")

    # res += xml_header

    sys.stdout.write('<key id="d1" for="edge" attr.name="weight" attr.type="int"/>')

    # node ids declaration as graphml format : <node id="#node" />
    nd=G.nodes
    for node in nd:
        sys.stdout.write('<node id="%d"/>\n' % (node))

    debug("%d nodes added." % len(nd))



    # edges declaration as graphml format : <edge source="src" target="tgt" />
    cnt = 1
    for e in G.edges.data(data='weight', default=1):
        sys.stdout.write('<edge id="e%d" source="%d" target="%d">' % (cnt, e[0], e[1]))
        sys.stdout.write('<data key="d1">%d</data>' % e[2])
        sys.stdout.write('</edge>')
        cnt += 1
    # xml_footerx
    sys.stdout.write('</graph></graphml>\n')
    #res += '</graph></graphml>'

    debug("---- xml_footer : done.")

    sys.stdout.write(res)
    debug("---- file exported successfully : %s" % filename)
    debug("")

    # close file now that we are done
    output_file.close()




def main():
   # global filename

    # nb_pub_fr=0
    # c=0
    # filename = "ARTS-1990"

    # parse json file
    #global data
   # data = extract_data_from_json(filename + ".json")

    # entries mostly represents papers and their informations, so we are only interested in exploring through papers informations
    #global papers
    #papers = data['search-results']['entry']

    # set of authors
    global nodes
    global nbr_fr_pub
    global nbr_papers


    extract_all()


    distpub = list(auth_pub.values())
    print(distpub)
    plt.hist(distpub);
    # ax.set_title('Distribution of number of publications:COMP')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("number of publications")
    plt.xlim(left=0, right=150)
    plt.savefig('Distribution of number of publicationsCOMP.png')
    plt.clf()
    plt.close()

# plt.subplot()
    # nx.draw(G, node_size=10)
    # # pos = nx.spring_layout(G)
    # # # nx.draw_networkx_nodes(G, pos, node_size=20)
    # # #
    # # # nx.draw_networkx_edges(G, pos)
    # # nx.draw_networkx_edge_labels(G, pos, font_size=8, font_family='sans-serif')
    # #
    # # plt.axis('off')
    # plt.show()


    # export_graphml("allFinal.graphml")
    # for u,v,w in G.edges(data=True):
    #     print(u,v,w,G.degree[u])
    #     print("`\n")
    # print("number of nodes : %d"  %(len(G)))
    # print("number of edges : %d" %(G.number_of_edges()))

    #
    # here
    nn = G.number_of_nodes()
    ne = G.number_of_edges()


    sys.stdout = open("statsFile.log", "w+")
    print("number of connected components: %d" %(nx.number_connected_components(G)))
    print("Number of nodes : %d" % (nn))
    print("Number of edges : %d" % (ne))
    Gc = max(nx.connected_components(G), key=len)
    S = G.subgraph(Gc).copy()
    print("Number of nodes in the largest connected components: %d" % (S.number_of_nodes()))
    print("Number of edges in the largest connected components: %d" % (S.number_of_edges()))
    # partition = cm.best_partition(S)
    # np = max([v for u, v in partition.items()]) + 1
    # print("Number of partitions: %d" % (np))
    # mod = cm.modularity(partition, S)
    # print("modularity:", mod)
    # with open('outputpartitionsFile.csv', 'w+') as output:
    #     for key in partition.keys():
    #         output.write("%s,%s\n" % (key, partition[key]))
    # export_degree_hist("degree_distri")
    print(authnames)
    print(auth_cities)
    print(authpub)


    sys.stdout = open("statsFileJrn.log", "w+")
    print(authpapername)
    #



    # values = [partition.get(node) for node in S.nodes]
    #
    # nx.draw_spring(S, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=False)
    # plt.savefig("Clusters")
    # plt.show()
    # plt.clf()
    # plt.close()






if __name__ == '__main__':

    start = time.perf_counter()
    main()
    end = time.perf_counter()
    execution_time = end - start

    print("execution time : %0.2f seconds" % (execution_time))

